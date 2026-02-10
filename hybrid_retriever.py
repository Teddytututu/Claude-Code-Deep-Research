"""
GraphRAG Hybrid Retrieval System v9.0

Based on:
- Benchmarking Vector, Graph and Hybrid Retrieval (arXiv:2507.03608)
- GraphRAG: Graph-Based Retrieval Augmentation
- RRF (Reciprocal Rank Fusion) for hybrid ranking

This module implements hybrid retrieval combining:
1. Vector-based semantic search (dense retrieval)
2. Knowledge graph traversal (structural retrieval)
3. Reciprocal Rank Fusion (RRF) for result combination
4. Agentic RAG for intelligent retrieval method selection

Author: Deep Research System
Date: 2026-02-09
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path
from collections import defaultdict
import hashlib

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

from memory_graph import SemanticMemory, NodeType, EdgeType


class RetrievalMethod(Enum):
    """Retrieval methods"""
    VECTOR = "vector"  # Dense semantic search
    GRAPH = "graph"  # Knowledge graph traversal
    KEYWORD = "keyword"  # Sparse keyword search
    HYBRID = "hybrid"  # Combined methods


@dataclass
class RetrievalResult:
    """Result from a retrieval operation"""
    id: str
    content: Dict[str, Any]
    score: float
    method: RetrievalMethod
    rank: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "score": round(self.score, 4),
            "method": self.method.value,
            "rank": self.rank,
            "metadata": self.metadata
        }


class VectorStore:
    """
    Vector-based retrieval using embeddings.

    In production, this would use:
    - OpenAI embeddings (text-embedding-3-large)
    - Sentence Transformers
    - Vector database (Pinecone, Weaviate, Milvus)
    """

    def __init__(self, embedding_model: str = "text-embedding-3-large"):
        """
        Initialize vector store.

        Args:
            embedding_model: Name of embedding model to use
        """
        self.embedding_model = embedding_model
        self._embeddings: Dict[str, List[float]] = {}
        self._documents: Dict[str, Dict[str, Any]] = {}

    def add_document(self, doc_id: str, content: Dict[str, Any]) -> None:
        """
        Add a document to the vector store.

        Args:
            doc_id: Document ID
            content: Document content with 'text' field for embedding
        """
        self._documents[doc_id] = content

        # Generate embedding (in production, call embedding API)
        text = content.get("text", content.get("title", content.get("abstract", "")))
        embedding = self._generate_embedding(text)
        self._embeddings[doc_id] = embedding

    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text.

        In production, call embedding API.
        Here we use a simple hash-based fallback.
        """
        # Simple hash-based embedding for demo (NOT production quality)
        text_bytes = text.encode('utf-8')
        hash_obj = hashlib.sha256(text_bytes)

        # Convert hash to 128-dimensional vector
        hash_digest = hash_obj.digest()
        embedding = []
        for i in range(128):
            byte_idx = (i * 2) % len(hash_digest)
            val = hash_digest[byte_idx] / 255.0
            embedding.append(val)

        return embedding

    def search(
        self,
        query: str,
        top_k: int = 10,
        min_score: float = 0.0
    ) -> List[RetrievalResult]:
        """
        Search for similar documents.

        Args:
            query: Search query
            top_k: Number of results to return
            min_score: Minimum similarity score

        Returns:
            List of retrieval results
        """
        if not self._embeddings:
            return []

        # Generate query embedding
        query_embedding = self._generate_embedding(query)

        # Calculate cosine similarity
        similarities = []
        for doc_id, doc_embedding in self._embeddings.items():
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            if similarity >= min_score:
                similarities.append((doc_id, similarity))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Create results
        results = []
        for rank, (doc_id, score) in enumerate(similarities[:top_k], 1):
            results.append(RetrievalResult(
                id=doc_id,
                content=self._documents.get(doc_id, {}),
                score=score,
                method=RetrievalMethod.VECTOR,
                rank=rank,
                metadata={"similarity_metric": "cosine"}
            ))

        return results

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if not NUMPY_AVAILABLE:
            return self._cosine_similarity_python(vec1, vec2)

        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2) + 1e-8)

    def _cosine_similarity_python(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity without numpy"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        return dot_product / (norm1 * norm2 + 1e-8)


class GraphRetriever:
    """
    Knowledge graph-based retrieval.

    Uses the semantic memory graph for:
    - Citation network traversal
    - Multi-hop reasoning
    - Concept-based search
    """

    def __init__(self, semantic_memory: SemanticMemory):
        """
        Initialize graph retriever.

        Args:
            semantic_memory: The semantic memory graph
        """
        self.memory = semantic_memory

    def search(
        self,
        query: str,
        top_k: int = 10,
        search_depth: int = 2
    ) -> List[RetrievalResult]:
        """
        Search using knowledge graph traversal.

        Args:
            query: Search query
            top_k: Number of results to return
            search_depth: Depth for graph traversal

        Returns:
            List of retrieval results
        """
        # Extract concepts from query
        query_concepts = self._extract_concepts(query)

        # Find relevant nodes
        relevant_nodes = self._find_relevant_nodes(query_concepts, search_depth)

        # Score and rank
        scored_results = []
        for node_id, relevance in relevant_nodes.items():
            node = self.memory._nodes.get(node_id)
            if node:
                scored_results.append((node_id, node, relevance))

        scored_results.sort(key=lambda x: x[2], reverse=True)

        # Create results
        results = []
        for rank, (node_id, node, score) in enumerate(scored_results[:top_k], 1):
            results.append(RetrievalResult(
                id=node_id,
                content=node.attributes,
                score=score,
                method=RetrievalMethod.GRAPH,
                rank=rank,
                metadata={"search_depth": search_depth, "concepts_matched": query_concepts}
            ))

        return results

    def _extract_concepts(self, query: str) -> List[str]:
        """Extract key concepts from query"""
        # Simple keyword extraction (in production, use NER)
        words = query.lower().split()
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for"}
        concepts = [w for w in words if len(w) > 3 and w not in stop_words]
        return concepts

    def _find_relevant_nodes(
        self,
        concepts: List[str],
        search_depth: int
    ) -> Dict[str, float]:
        """
        Find nodes relevant to the concepts.

        Args:
            concepts: List of concepts to search for
            search_depth: Depth for graph traversal

        Returns:
            Dictionary of node_id to relevance score
        """
        relevance = defaultdict(float)

        # Direct concept matches
        for concept in concepts:
            concept_id = f"concept_{concept.lower().replace(' ', '_')}"
            if concept_id in self.memory._nodes:
                # Papers that introduce this concept
                for node_id in self.memory.get_neighbors(concept_id, max_depth=1):
                    if node_id.startswith("paper_"):
                        relevance[node_id] += 1.0

        # Traverse citations
        for node_id in list(relevance.keys()):
            # Papers cited by relevant papers
            cited = self.memory.get_neighbors(node_id, EdgeType.CITES, max_depth=1)
            for cited_id in cited[:3]:  # Top 3 citations
                relevance[cited_id] += 0.5

            # Papers that cite this paper
            for edge in self.memory._edges:
                if edge.target == node_id and edge.type == EdgeType.CITES:
                    relevance[edge.source] += 0.3

        return relevance


class HybridRetriever:
    """
    Hybrid retrieval combining vector and graph search.

    Uses Reciprocal Rank Fusion (RRF) to combine results.
    Based on research showing RRF improves recall and hit rate.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        graph_retriever: GraphRetriever,
        rrf_k: int = 60
    ):
        """
        Initialize hybrid retriever.

        Args:
            vector_store: Vector-based retriever
            graph_retriever: Graph-based retriever
            rrf_k: RRF constant (default 60)
        """
        self.vector_store = vector_store
        self.graph_retriever = graph_retriever
        self.rrf_k = rrf_k

    def search(
        self,
        query: str,
        top_k: int = 10,
        vector_weight: float = 0.5,
        graph_weight: float = 0.5
    ) -> List[RetrievalResult]:
        """
        Hybrid search combining vector and graph results.

        Args:
            query: Search query
            top_k: Number of results to return
            vector_weight: Weight for vector results (default 0.5)
            graph_weight: Weight for graph results (default 0.5)

        Returns:
            List of ranked retrieval results
        """
        # Get results from both methods
        vector_results = self.vector_store.search(query, top_k=top_k * 2)
        graph_results = self.graph_retriever.search(query, top_k=top_k * 2)

        # Apply RRF
        rrf_scores = self._reciprocal_rank_fusion(
            vector_results,
            graph_results,
            vector_weight,
            graph_weight
        )

        # Sort by RRF score
        sorted_results = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

        # Create final results
        final_results = []
        for rank, (doc_id, rrf_score) in enumerate(sorted_results[:top_k], 1):
            # Get content from whichever source has it
            content = None
            method = RetrievalMethod.HYBRID
            metadata = {"rrf_score": rrf_score}

            for result in vector_results:
                if result.id == doc_id:
                    content = result.content
                    metadata["vector_score"] = result.score
                    metadata["vector_rank"] = result.rank
                    break

            if not content:
                for result in graph_results:
                    if result.id == doc_id:
                        content = result.content
                        metadata["graph_score"] = result.score
                        metadata["graph_rank"] = result.rank
                        break

            if content:
                final_results.append(RetrievalResult(
                    id=doc_id,
                    content=content,
                    score=rrf_score,
                    method=method,
                    rank=rank,
                    metadata=metadata
                ))

        return final_results

    def _reciprocal_rank_fusion(
        self,
        vector_results: List[RetrievalResult],
        graph_results: List[RetrievalResult],
        vector_weight: float,
        graph_weight: float
    ) -> Dict[str, float]:
        """
        Apply Reciprocal Rank Fusion (RRF).

        RRF formula: score = sum(weight / (k + rank))

        Args:
            vector_results: Results from vector search
            graph_results: Results from graph search
            vector_weight: Weight for vector results
            graph_weight: Weight for graph results

        Returns:
            Dictionary of doc_id to RRF score
        """
        scores = defaultdict(float)

        # Add vector scores
        for result in vector_results:
            rrf_score = vector_weight / (self.rrf_k + result.rank)
            scores[result.id] += rrf_score

        # Add graph scores
        for result in graph_results:
            rrf_score = graph_weight / (self.rrf_k + result.rank)
            scores[result.id] += rrf_score

        return dict(scores)


class AgenticRAG:
    """
    Agentic RAG - Intelligent retrieval method selection.

    An agent that decides which retrieval method to use based on:
    - Query type (factual vs. exploratory)
    - Data availability (vector vs. graph coverage)
    - Performance requirements (speed vs. accuracy)
    """

    def __init__(
        self,
        vector_store: VectorStore,
        graph_retriever: GraphRetriever,
        hybrid_retriever: HybridRetriever
    ):
        """
        Initialize agentic RAG.

        Args:
            vector_store: Vector-based retriever
            graph_retriever: Graph-based retriever
            hybrid_retriever: Hybrid retriever
        """
        self.vector_store = vector_store
        self.graph_retriever = graph_retriever
        self.hybrid_retriever = hybrid_retriever
        self.decision_history: List[Dict[str, Any]] = []

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
        method_hint: Optional[str] = None
    ) -> Tuple[List[RetrievalResult], Dict[str, Any]]:
        """
        Intelligently retrieve based on query analysis.

        Args:
            query: Search query
            top_k: Number of results to return
            method_hint: Optional hint for which method to use

        Returns:
            Tuple of (results, decision_info)
        """
        # Analyze query to determine best method
        decision = self._decide_method(query, method_hint)

        # Execute retrieval
        if decision["method"] == RetrievalMethod.VECTOR:
            results = self.vector_store.search(query, top_k=top_k)
        elif decision["method"] == RetrievalMethod.GRAPH:
            results = self.graph_retriever.search(query, top_k=top_k)
        else:  # HYBRID
            results = self.hybrid_retriever.search(
                query,
                top_k=top_k,
                vector_weight=decision.get("vector_weight", 0.5),
                graph_weight=decision.get("graph_weight", 0.5)
            )

        # Record decision
        self.decision_history.append({
            "query": query,
            "decision": decision,
            "results_count": len(results),
            "timestamp": self._get_timestamp()
        })

        decision_info = {
            "method_used": decision["method"].value,
            "reasoning": decision["reasoning"],
            "confidence": decision.get("confidence", 0.5)
        }

        return results, decision_info

    def _decide_method(self, query: str, hint: Optional[str]) -> Dict[str, Any]:
        """
        Decide which retrieval method to use.

        Args:
            query: Search query
            hint: Optional method hint

        Returns:
            Decision dictionary with method and reasoning
        """
        if hint:
            return {
                "method": RetrievalMethod(hint),
                "reasoning": f"User specified method: {hint}",
                "confidence": 1.0
            }

        # Analyze query characteristics
        query_lower = query.lower()

        # Check for citation/explored queries (favor graph)
        if any(kw in query_lower for kw in ["cite", "citation", "reference", "related to"]):
            return {
                "method": RetrievalMethod.GRAPH,
                "reasoning": "Query asks for citation relationships",
                "confidence": 0.8
            }

        # Check for specific paper names (favor vector)
        if "arxiv" in query_lower or "paper:" in query_lower:
            return {
                "method": RetrievalMethod.VECTOR,
                "reasoning": "Query targets specific papers",
                "confidence": 0.9
            }

        # Check for comparative queries (favor hybrid)
        if any(kw in query_lower for kw in ["vs", "versus", "compare", "difference"]):
            return {
                "method": RetrievalMethod.HYBRID,
                "reasoning": "Comparative query benefits from both methods",
                "vector_weight": 0.5,
                "graph_weight": 0.5,
                "confidence": 0.7
            }

        # Check for exploratory queries (favor hybrid)
        if any(kw in query_lower for kw in ["overview", "survey", "state of the art", "recent advances"]):
            return {
                "method": RetrievalMethod.HYBRID,
                "reasoning": "Exploratory query needs breadth and depth",
                "vector_weight": 0.4,
                "graph_weight": 0.6,
                "confidence": 0.75
            }

        # Default: hybrid with balanced weights
        return {
            "method": RetrievalMethod.HYBRID,
            "reasoning": "Default: use hybrid for comprehensive results",
            "vector_weight": 0.5,
            "graph_weight": 0.5,
            "confidence": 0.5
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

    def get_decision_stats(self) -> Dict[str, Any]:
        """Get statistics about retrieval decisions"""
        method_counts = defaultdict(int)
        for decision in self.decision_history:
            method = decision["decision"]["method"]
            method_counts[method.value] += 1

        return {
            "total_decisions": len(self.decision_history),
            "method_distribution": dict(method_counts),
            "recent_decisions": self.decision_history[-10:] if self.decision_history else []
        }


class GraphRAGSystem:
    """
    Complete GraphRAG system with all retrieval components.

    Integrates:
    - Vector store for semantic search
    - Graph retriever for structural search
    - Hybrid retriever with RRF
    - Agentic RAG for intelligent selection
    """

    def __init__(self, semantic_memory: Optional[SemanticMemory] = None):
        """
        Initialize GraphRAG system.

        Args:
            semantic_memory: Optional existing semantic memory
        """
        self.semantic_memory = semantic_memory or SemanticMemory()

        # Initialize components
        self.vector_store = VectorStore()
        self.graph_retriever = GraphRetriever(self.semantic_memory)
        self.hybrid_retriever = HybridRetriever(
            self.vector_store,
            self.graph_retriever
        )
        self.agentic_rag = AgenticRAG(
            self.vector_store,
            self.graph_retriever,
            self.hybrid_retriever
        )

        # Index existing data
        self._index_existing_data()

    def _index_existing_data(self):
        """Index existing documents in semantic memory"""
        # Index papers
        for node_id, node in self.semantic_memory._nodes.items():
            if node.type == NodeType.ACADEMIC_PAPER:
                text = f"{node.attributes.get('title', '')} {node.attributes.get('abstract', '')}"
                self.vector_store.add_document(node_id, {
                    "text": text,
                    **node.attributes
                })

    def add_research_findings(self, findings: Dict[str, Any]) -> None:
        """
        Add research findings to the system.

        Args:
            findings: Research findings data
        """
        # Add to semantic memory
        for paper in findings.get("academic_papers", []):
            paper_id = self.semantic_memory.add_paper(paper)
            text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
            self.vector_store.add_document(paper_id, {
                "text": text,
                **paper
            })

        for project in findings.get("github_projects", []):
            project_id = self.semantic_memory.add_project(project)
            text = f"{project.get('name', '')} {project.get('description', '')}"
            self.vector_store.add_document(project_id, {
                "text": text,
                **project
            })

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
        method: str = "agentic"
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Retrieve relevant documents.

        Args:
            query: Search query
            top_k: Number of results
            method: Retrieval method (agentic, vector, graph, hybrid)

        Returns:
            Tuple of (results, metadata)
        """
        if method == "agentic":
            results, decision_info = self.agentic_rag.retrieve(query, top_k)
        elif method == "vector":
            results = self.vector_store.search(query, top_k)
            decision_info = {"method_used": "vector", "reasoning": "Direct vector search"}
        elif method == "graph":
            results = self.graph_retriever.search(query, top_k)
            decision_info = {"method_used": "graph", "reasoning": "Direct graph search"}
        else:  # hybrid
            results = self.hybrid_retriever.search(query, top_k)
            decision_info = {"method_used": "hybrid", "reasoning": "Direct hybrid search"}

        # Convert to dict format
        results_dict = [r.to_dict() for r in results]

        return results_dict, decision_info

    def save(self, filepath: str) -> None:
        """Save GraphRAG system state"""
        self.semantic_memory.save(filepath)

    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            "semantic_memory": self.semantic_memory.to_dict()["stats"],
            "vector_store": {
                "documents_indexed": len(self.vector_store._documents),
                "embedding_model": self.vector_store.embedding_model
            },
            "agentic_rag": self.agentic_rag.get_decision_stats()
        }


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="GraphRAG Hybrid Retrieval v9.0")
    parser.add_argument("--query", type=str, help="Search query")
    parser.add_argument("--method", type=str, default="agentic",
                       choices=["agentic", "vector", "graph", "hybrid"],
                       help="Retrieval method")
    parser.add_argument("--top-k", type=int, default=10, help="Number of results")
    parser.add_argument("--load", type=str, help="Load research findings from file")
    parser.add_argument("--stats", action="store_true", help="Show system statistics")

    args = parser.parse_args()

    system = GraphRAGSystem()

    if args.load:
        with open(args.load, 'r', encoding='utf-8') as f:
            findings = json.load(f)
        system.add_research_findings(findings)
        print(f"Loaded findings from {args.load}")

    if args.stats:
        stats = system.get_stats()
        print(json.dumps(stats, indent=2))

    elif args.query:
        results, metadata = system.retrieve(args.query, args.top_k, args.method)
        print(json.dumps({
            "metadata": metadata,
            "results": results
        }, indent=2))

    else:
        print("GraphRAG Hybrid Retrieval v9.0")
        print("Use --query to search or --stats to see statistics")
