"""
Vector Store Module v10.0
向量存储模块

Implements ChromaDB-based vector storage for semantic search capabilities.
Supports optional sentence-transformers embeddings for local embedding generation.

Features:
- Dual backend: in-memory (default) or persistent ChromaDB
- Automatic embedding generation (if sentence-transformers available)
- Semantic similarity search
- Metadata filtering
- Collection management

Author: Deep Research System
Date: 2026-02-18
"""

from typing import List, Optional, Dict, Any, Literal
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime
import uuid
import json

# Optional imports with graceful fallback
try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False


@dataclass
class Document:
    """
    Document representation for vector storage.

    Attributes:
        id: Unique document identifier
        content: Text content for embedding
        metadata: Additional metadata dict
        embedding: Optional pre-computed embedding vector
    """
    id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Document':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class SearchResult:
    """
    Search result from vector store.

    Attributes:
        document: The matching document
        score: Similarity score (higher is better)
        distance: Distance metric (lower is better for some metrics)
    """
    document: Document
    score: float = 1.0
    distance: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "document": self.document.to_dict(),
            "score": self.score,
            "distance": self.distance
        }


class VectorStore:
    """
    Vector Store with ChromaDB backend.

    Supports both in-memory (ephemeral) and persistent storage modes.
    Automatically handles embedding generation if sentence-transformers is available.

    Usage:
        # In-memory mode (default)
        store = VectorStore()

        # Persistent mode
        store = VectorStore(persist_dir="./chroma_data", backend="chroma")

        # Add documents
        store.add_finding(Document(
            id="paper_1",
            content="This paper discusses multi-agent systems...",
            metadata={"type": "paper", "arxiv_id": "2308.00352"}
        ))

        # Semantic search
        results = store.search("agent coordination", n_results=5)
    """

    def __init__(
        self,
        persist_dir: str = ".chroma",
        backend: Literal["memory", "chroma"] = "memory",
        collection_name: str = "research_findings",
        use_embeddings: bool = True,
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize vector store.

        Args:
            persist_dir: Directory for persistent storage (chroma backend)
            backend: Storage backend - "memory" (ephemeral) or "chroma" (persistent)
            collection_name: Name of the collection to use
            use_embeddings: Whether to generate embeddings (requires sentence-transformers)
            embedding_model: Name of the sentence-transformers model to use
        """
        self.backend = backend
        self.collection_name = collection_name
        self.use_embeddings = use_embeddings and EMBEDDING_AVAILABLE
        self.embedding_model_name = embedding_model

        # Initialize embedding model
        self.encoder: Optional[SentenceTransformer] = None
        if self.use_embeddings:
            try:
                self.encoder = SentenceTransformer(embedding_model)
                print(f"[VectorStore] Loaded embedding model: {embedding_model}")
            except Exception as e:
                print(f"[VectorStore] Warning: Failed to load embedding model: {e}")
                self.use_embeddings = False

        # Initialize ChromaDB
        self.client: Optional[chromadb.Client] = None
        self.collection: Optional[chromadb.Collection] = None

        if not CHROMADB_AVAILABLE:
            print("[VectorStore] Warning: ChromaDB not available, using in-memory fallback")
            self._memory_store: Dict[str, Document] = {}
            self.backend = "memory_fallback"
        else:
            self._init_chroma(persist_dir)

    def _init_chroma(self, persist_dir: str) -> None:
        """Initialize ChromaDB client and collection."""
        if self.backend == "chroma":
            # Persistent mode
            persist_path = Path(persist_dir)
            persist_path.mkdir(parents=True, exist_ok=True)

            self.client = chromadb.PersistentClient(
                path=str(persist_path),
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
        else:
            # In-memory mode
            self.client = chromadb.EphemeralClient()

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        print(f"[VectorStore] Initialized {self.backend} backend with {self.collection.count()} documents")

    def add_finding(self, doc: Document) -> None:
        """
        Add a document to the vector store.

        Args:
            doc: Document to add
        """
        if not doc.id:
            doc.id = str(uuid.uuid4())

        if self.backend == "memory_fallback":
            self._memory_store[doc.id] = doc
            return

        # Generate embedding if needed and available
        embedding = None
        if self.use_embeddings and self.encoder:
            try:
                embedding = self.encoder.encode(doc.content).tolist()
            except Exception as e:
                print(f"[VectorStore] Warning: Failed to generate embedding: {e}")

        # Add to collection
        self.collection.add(
            ids=[doc.id],
            documents=[doc.content],
            metadatas=[doc.metadata],
            embeddings=[embedding] if embedding else None
        )

    def add_findings(self, docs: List[Document]) -> None:
        """
        Add multiple documents to the vector store.

        Args:
            docs: List of documents to add
        """
        if not docs:
            return

        if self.backend == "memory_fallback":
            for doc in docs:
                if not doc.id:
                    doc.id = str(uuid.uuid4())
                self._memory_store[doc.id] = doc
            return

        # Generate embeddings in batch
        embeddings = None
        if self.use_embeddings and self.encoder:
            try:
                embeddings = self.encoder.encode([d.content for d in docs]).tolist()
            except Exception as e:
                print(f"[VectorStore] Warning: Failed to generate batch embeddings: {e}")

        # Prepare data
        ids = [doc.id or str(uuid.uuid4()) for doc in docs]
        documents = [doc.content for doc in docs]
        metadatas = [doc.metadata for doc in docs]

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

    def search(
        self,
        query: str,
        n_results: int = 10,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Semantic search for similar documents.

        Args:
            query: Search query text
            n_results: Maximum number of results
            where: Metadata filter (e.g., {"type": "paper"})
            where_document: Document content filter

        Returns:
            List of SearchResult objects
        """
        if self.backend == "memory_fallback":
            return self._memory_search(query, n_results)

        # Generate query embedding if available
        query_embedding = None
        if self.use_embeddings and self.encoder:
            try:
                query_embedding = self.encoder.encode(query).tolist()
            except Exception as e:
                print(f"[VectorStore] Warning: Failed to generate query embedding: {e}")

        # Perform search
        if query_embedding:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where,
                where_document=where_document
            )
        else:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where,
                where_document=where_document
            )

        # Convert to SearchResult objects
        search_results = []
        if results['ids'] and results['ids'][0]:
            for i, doc_id in enumerate(results['ids'][0]):
                doc = Document(
                    id=doc_id,
                    content=results['documents'][0][i] if results['documents'] else "",
                    metadata=results['metadatas'][0][i] if results['metadatas'] else {}
                )

                # Calculate score from distance (cosine distance -> similarity)
                distance = results['distances'][0][i] if results.get('distances') else 0.0
                score = 1.0 - distance if distance else 1.0

                search_results.append(SearchResult(
                    document=doc,
                    score=score,
                    distance=distance
                ))

        return search_results

    def _memory_search(self, query: str, n_results: int) -> List[SearchResult]:
        """Fallback search for memory-only mode (simple keyword matching)."""
        query_words = set(query.lower().split())
        results = []

        for doc_id, doc in self._memory_store.items():
            doc_words = set(doc.content.lower().split())
            overlap = len(query_words & doc_words)
            if overlap > 0:
                score = overlap / max(len(query_words), 1)
                results.append(SearchResult(document=doc, score=score))

        # Sort by score descending
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:n_results]

    def get(self, doc_id: str) -> Optional[Document]:
        """
        Get a document by ID.

        Args:
            doc_id: Document ID

        Returns:
            Document if found, None otherwise
        """
        if self.backend == "memory_fallback":
            return self._memory_store.get(doc_id)

        results = self.collection.get(ids=[doc_id])

        if results['ids']:
            return Document(
                id=results['ids'][0],
                content=results['documents'][0] if results['documents'] else "",
                metadata=results['metadatas'][0] if results['metadatas'] else {}
            )
        return None

    def delete(self, doc_id: str) -> None:
        """
        Delete a document by ID.

        Args:
            doc_id: Document ID to delete
        """
        if self.backend == "memory_fallback":
            self._memory_store.pop(doc_id, None)
            return

        self.collection.delete(ids=[doc_id])

    def delete_where(self, where: Dict[str, Any]) -> int:
        """
        Delete documents matching metadata filter.

        Args:
            where: Metadata filter

        Returns:
            Number of documents deleted
        """
        if self.backend == "memory_fallback":
            count = 0
            to_delete = [
                doc_id for doc_id, doc in self._memory_store.items()
                if all(doc.metadata.get(k) == v for k, v in where.items())
            ]
            for doc_id in to_delete:
                del self._memory_store[doc_id]
                count += 1
            return count

        # Get IDs to delete
        results = self.collection.get(where=where)
        if results['ids']:
            self.collection.delete(ids=results['ids'])
            return len(results['ids'])
        return 0

    def count(self) -> int:
        """
        Get total number of documents in store.

        Returns:
            Document count
        """
        if self.backend == "memory_fallback":
            return len(self._memory_store)
        return self.collection.count()

    def clear(self) -> None:
        """Clear all documents from the collection."""
        if self.backend == "memory_fallback":
            self._memory_store.clear()
            return

        # Delete and recreate collection
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store.

        Returns:
            Dictionary with stats
        """
        stats = {
            "backend": self.backend,
            "collection_name": self.collection_name,
            "document_count": self.count(),
            "embedding_enabled": self.use_embeddings,
            "embedding_model": self.embedding_model_name if self.use_embeddings else None,
        }

        if self.backend == "memory_fallback":
            stats["chromadb_available"] = False
        else:
            stats["chromadb_available"] = True
            # Count by type
            results = self.collection.get()
            type_counts: Dict[str, int] = {}
            for metadata in (results.get('metadatas') or []):
                doc_type = metadata.get('type', 'unknown')
                type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
            stats["documents_by_type"] = type_counts

        return stats


class VectorStoreManager:
    """
    Manager for multiple vector store collections.

    Provides a unified interface for managing different types of
    research data (papers, projects, discussions) in separate collections.
    """

    def __init__(
        self,
        persist_dir: str = ".chroma",
        backend: Literal["memory", "chroma"] = "memory"
    ):
        """
        Initialize vector store manager.

        Args:
            persist_dir: Directory for persistent storage
            backend: Storage backend
        """
        self.persist_dir = persist_dir
        self.backend = backend

        # Initialize collections for different data types
        self.stores: Dict[str, VectorStore] = {}
        self._init_default_collections()

    def _init_default_collections(self) -> None:
        """Initialize default collections for research data types."""
        for collection_name in ["papers", "projects", "discussions", "concepts"]:
            self.stores[collection_name] = VectorStore(
                persist_dir=self.persist_dir,
                backend=self.backend,
                collection_name=collection_name
            )

    def get_store(self, collection_name: str) -> VectorStore:
        """
        Get or create a vector store for a collection.

        Args:
            collection_name: Name of the collection

        Returns:
            VectorStore instance
        """
        if collection_name not in self.stores:
            self.stores[collection_name] = VectorStore(
                persist_dir=self.persist_dir,
                backend=self.backend,
                collection_name=collection_name
            )
        return self.stores[collection_name]

    def add_paper(self, paper_data: Dict[str, Any]) -> str:
        """
        Add a paper to the papers collection.

        Args:
            paper_data: Paper data dictionary

        Returns:
            Document ID
        """
        doc = Document(
            id=paper_data.get("arxiv_id", str(uuid.uuid4())),
            content=self._paper_to_text(paper_data),
            metadata={
                "type": "paper",
                "arxiv_id": paper_data.get("arxiv_id", ""),
                "title": paper_data.get("title", ""),
                "authors": paper_data.get("authors", []),
                "year": paper_data.get("year", ""),
                "categories": paper_data.get("categories", []),
                "timestamp": datetime.now().isoformat()
            }
        )
        self.stores["papers"].add_finding(doc)
        return doc.id

    def add_project(self, project_data: Dict[str, Any]) -> str:
        """
        Add a project to the projects collection.

        Args:
            project_data: Project data dictionary

        Returns:
            Document ID
        """
        doc = Document(
            id=project_data.get("full_name", str(uuid.uuid4())),
            content=self._project_to_text(project_data),
            metadata={
                "type": "project",
                "name": project_data.get("name", ""),
                "full_name": project_data.get("full_name", ""),
                "stars": project_data.get("stars", 0),
                "language": project_data.get("language", ""),
                "timestamp": datetime.now().isoformat()
            }
        )
        self.stores["projects"].add_finding(doc)
        return doc.id

    def add_discussion(self, discussion_data: Dict[str, Any]) -> str:
        """
        Add a discussion to the discussions collection.

        Args:
            discussion_data: Discussion data dictionary

        Returns:
            Document ID
        """
        doc = Document(
            id=discussion_data.get("id", str(uuid.uuid4())),
            content=self._discussion_to_text(discussion_data),
            metadata={
                "type": "discussion",
                "platform": discussion_data.get("platform", ""),
                "title": discussion_data.get("title", ""),
                "url": discussion_data.get("url", ""),
                "timestamp": datetime.now().isoformat()
            }
        )
        self.stores["discussions"].add_finding(doc)
        return doc.id

    def search_all(
        self,
        query: str,
        n_results: int = 5,
        collections: Optional[List[str]] = None
    ) -> Dict[str, List[SearchResult]]:
        """
        Search across all or specified collections.

        Args:
            query: Search query
            n_results: Results per collection
            collections: List of collection names (None = all)

        Returns:
            Dictionary mapping collection names to search results
        """
        results = {}
        target_collections = collections or list(self.stores.keys())

        for name in target_collections:
            if name in self.stores:
                results[name] = self.stores[name].search(query, n_results)

        return results

    def _paper_to_text(self, paper: Dict[str, Any]) -> str:
        """Convert paper data to searchable text."""
        parts = [
            paper.get("title", ""),
            paper.get("abstract", ""),
            " ".join(paper.get("authors", [])),
            " ".join(paper.get("categories", [])),
            paper.get("summary", "")
        ]
        return " ".join(p for p in parts if p)

    def _project_to_text(self, project: Dict[str, Any]) -> str:
        """Convert project data to searchable text."""
        parts = [
            project.get("name", ""),
            project.get("description", ""),
            project.get("language", ""),
            " ".join(project.get("topics", [])),
            project.get("architecture_description", "")
        ]
        return " ".join(p for p in parts if p)

    def _discussion_to_text(self, discussion: Dict[str, Any]) -> str:
        """Convert discussion data to searchable text."""
        parts = [
            discussion.get("title", ""),
            discussion.get("summary", ""),
            " ".join(q.get("quote", "") for q in discussion.get("key_quotes", [])),
            discussion.get("platform", "")
        ]
        return " ".join(p for p in parts if p)

    def get_global_stats(self) -> Dict[str, Any]:
        """Get statistics for all collections."""
        return {
            name: store.get_stats()
            for name, store in self.stores.items()
        }


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Vector Store Module")
    parser.add_argument("--test", action="store_true", help="Run test with sample data")
    parser.add_argument("--stats", action="store_true", help="Show store statistics")
    parser.add_argument("--search", type=str, help="Search query")
    parser.add_argument("--backend", type=str, default="memory", choices=["memory", "chroma"])
    parser.add_argument("--persist-dir", type=str, default=".chroma")

    args = parser.parse_args()

    if args.test:
        print("Testing Vector Store...")

        store = VectorStore(
            persist_dir=args.persist_dir,
            backend=args.backend
        )

        # Add sample documents
        sample_docs = [
            Document(
                id="paper_1",
                content="Multi-agent systems enable complex task decomposition through parallel execution.",
                metadata={"type": "paper", "arxiv_id": "2308.00352"}
            ),
            Document(
                id="paper_2",
                content="LangGraph provides state management for multi-step AI workflows.",
                metadata={"type": "paper", "arxiv_id": "2401.15884"}
            ),
            Document(
                id="project_1",
                content="CrewAI orchestrates AI agents for collaborative task completion.",
                metadata={"type": "project", "name": "crewai"}
            ),
        ]

        store.add_findings(sample_docs)
        print(f"Added {len(sample_docs)} documents")

        # Test search
        results = store.search("multi-agent orchestration", n_results=3)
        print(f"\nSearch results for 'multi-agent orchestration':")
        for r in results:
            print(f"  - [{r.score:.3f}] {r.document.id}: {r.document.content[:60]}...")

    if args.stats:
        store = VectorStore(
            persist_dir=args.persist_dir,
            backend=args.backend
        )
        stats = store.get_stats()
        print(json.dumps(stats, indent=2))

    if args.search:
        store = VectorStore(
            persist_dir=args.persist_dir,
            backend=args.backend
        )
        results = store.search(args.search, n_results=5)
        print(f"Search results for '{args.search}':")
        for r in results:
            print(f"  - [{r.score:.3f}] {r.document.id}")
            print(f"    {r.document.content[:100]}...")
