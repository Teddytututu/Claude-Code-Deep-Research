# Hybrid Retrieval (GraphRAG) / 混合检索

## Overview / 概述

GraphRAG Hybrid Retrieval System combining vector, graph, and keyword search with Reciprocal Rank Fusion (RRF).

Based on:
- [Benchmarking Vector, Graph and Hybrid Retrieval](https://arxiv.org/abs/2507.03608) [arXiv:2507.03608](https://arxiv.org/abs/2507.03608)
- GraphRAG: Graph-Based Retrieval Augmentation

---

## Retrieval Methods / 检索方法

### 1. Vector Retrieval (Dense) / 向量检索（稠密）

**Purpose**: Semantic similarity search using embeddings

**How It Works**:
```python
class VectorStore:
    def search(query: str, top_k: int = 10) -> List[RetrievalResult]:
        # Generate query embedding
        query_embedding = self._generate_embedding(query)

        # Calculate cosine similarity
        similarities = [
            cosine_similarity(query_embedding, doc_embedding)
            for doc_embedding in self.embeddings
        ]

        # Return top-k by similarity
        return sorted_results[:top_k]
```

**Embedding Models** (Production):
- OpenAI: `text-embedding-3-large`
- Sentence Transformers
- Vector databases: Pinecone, Weaviate, Milvus

---

### 2. Graph Retrieval (Structural) / 图检索（结构）

**Purpose**: Knowledge graph traversal for multi-hop reasoning

**How It Works**:
```python
class GraphRetriever:
    def search(query: str, top_k: int = 10, search_depth: int = 2):
        # Extract concepts from query
        concepts = self._extract_concepts(query)

        # Find papers that introduce concepts
        for concept in concepts:
            concept_id = f"concept_{concept}"
            papers = memory.get_neighbors(concept_id)
            relevance[papers] += 1.0

        # Traverse citations (2-hop)
        cited = memory.get_neighbors(paper_id, EdgeType.CITES)
        relevance[cited] += 0.5

        return ranked_results
```

**Graph Traversal**:
- Direct concept matches
- Citation network traversal
- Multi-hop reasoning (configurable depth)

---

### 3. Keyword Retrieval (Sparse) / 关键词检索（稀疏）

**Purpose**: Exact term matching for specific queries

**Use Cases**:
- Specific paper names
- ArXiv IDs
- Author names
- Framework names

---

## Reciprocal Rank Fusion (RRF) / 倒数排名融合

**Purpose**: Combine results from multiple retrieval methods

**Formula**:
```python
RRF_score(d) = Σ (weight / (k + rank(d)))
```

Where:
- `k` = constant (typically 60)
- `weight` = method weight (e.g., 0.5 for vector, 0.5 for graph)
- `rank(d)` = rank of document in method's results

**Example**:
```python
# Document appears at rank 1 in vector, rank 3 in graph
rrf_score = 0.5/(60+1) + 0.5/(60+3) = 0.0082 + 0.0081 = 0.0163
```

---

## Agentic RAG / 智能体 RAG

**Purpose**: Intelligently select retrieval method based on query analysis

**Decision Logic**:
```python
def decide_method(query: str) -> RetrievalMethod:
    # Citation queries → Graph
    if "cite" in query or "reference" in query:
        return RetrievalMethod.GRAPH

    # Specific papers → Vector
    if "arxiv" in query or "paper:" in query:
        return RetrievalMethod.VECTOR

    # Comparative queries → Hybrid
    if "vs" in query or "compare" in query:
        return RetrievalMethod.HYBRID

    # Exploratory queries → Hybrid
    if "overview" in query or "survey" in query:
        return RetrievalMethod.HYBRID

    # Default: Balanced hybrid
    return RetrievalMethod.HYBRID
```

---

## GraphRAG System / GraphRAG 系统

**Complete System**:
```python
class GraphRAGSystem:
    def __init__(self, semantic_memory: SemanticMemory):
        self.vector_store = VectorStore()
        self.graph_retriever = GraphRetriever(semantic_memory)
        self.hybrid_retriever = HybridRetriever(vector_store, graph_retriever)
        self.agentic_rag = AgenticRAG(vector_store, graph_retriever, hybrid_retriever)
```

**Retrieval Options**:
- `agentic`: Intelligent method selection
- `vector`: Pure vector search
- `graph`: Pure graph traversal
- `hybrid`: Combined RRF

---

## CLI Usage / 命令行使用

```bash
# Agentic retrieval (auto-select method)
python "tools\hybrid_retriever.py" --query "multi-agent timeout mechanisms" --method agentic

# Vector search
python "tools\hybrid_retriever.py" --query "LangGraph vs CrewAI" --method vector

# Graph search
python "tools\hybrid_retriever.py" --query "citation network" --method graph

# Load findings and retrieve
python "tools\hybrid_retriever.py" --load research_data/academic_research_output.json --query "orchestration patterns"

# Show system statistics
python "tools\hybrid_retriever.py" --stats
```

---

## Performance Considerations / 性能考虑

| Method | Speed | Accuracy | Use Case |
|--------|-------|----------|----------|
| **Vector** | Fast | Semantic similarity | Content-based queries |
| **Graph** | Medium | Structural relationships | Citation/concept queries |
| **Hybrid** | Slower | Best of both | Complex queries |
| **Agentic** | Variable | Optimized per query | General purpose |

---

## Indexing / 索引

**Document Indexing**:
```python
# Index paper
system.add_research_findings({
    "academic_papers": [{
        "arxiv_id": "2501.03236",
        "title": "MAGMA Memory",
        "abstract": "..."
    }]
})

# Index project
system.add_research_findings({
    "github_projects": [{
        "name": "langchain-ai/langgraph",
        "description": "..."
    }]
})
```

---

## Related Modules / 相关模块

- **memory_graph.py**: SemanticMemory for graph retrieval
- **memory_system.py**: MAGMAMemory integration
- **cross_domain_tracker.py**: Cross-domain relationships

---

## Research Integration / 研究集成

**Phase 1 Research Output** → **GraphRAG Index**:
```python
# After academic-researcher completes
graphrag.add_research_findings(academic_research_output)

# After github-watcher completes
graphrag.add_research_findings(github_research_output)

# Retrieve across domains
results, metadata = graphrag.retrieve("orchestration patterns", method="agentic")
```

---

## Fallback Implementations / 后备实现

**Without Dependencies**:
- **Embeddings**: Hash-based fallback (NOT production quality)
- **NetworkX**: Adjacency list fallback
- **Numpy**: Pure Python cosine similarity

**Production Recommendations**:
- Use OpenAI/SentenceTransformer embeddings
- Use NetworkX for graph operations
- Use dedicated vector database (Pinecone, Weaviate)
