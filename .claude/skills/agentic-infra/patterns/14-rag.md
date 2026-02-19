# Pattern 14: Retrieval-Augmented Generation (RAG)

## Intent
Ground agent responses in verifiable, up-to-date external knowledge by retrieving relevant documents at query time and including them in the LLM's context, rather than relying solely on parametric knowledge.

## Context
Use when the agent needs domain-specific knowledge not in the model's training data, when answers must be traceable to specific source documents, when knowledge changes frequently, or when hallucination on factual queries is unacceptable.

## Forces / Tradeoffs
- **Retrieval quality vs. generation quality**: The best generation cannot compensate for poor retrieval — garbage in, garbage out.
- **Chunk size tradeoff**: Small chunks improve retrieval precision but lose surrounding context; large chunks preserve context but dilute relevance scores.
- **Latency**: Retrieval adds a round-trip before generation; vector search at scale requires careful indexing.

## Solution
Core RAG pipeline (p. 217):
1. **Ingestion**: Split documents into chunks → embed → store in vector DB.
2. **Retrieval**: Embed the query → find top-K nearest chunks by cosine similarity.
3. **Augmentation**: Prepend retrieved chunks to the LLM prompt.
4. **Generation**: LLM generates an answer grounded in retrieved context.

**Vector databases** (p. 220): Pinecone, Weaviate, ChromaDB, FAISS — each with different trade-offs (hosted vs. local, scale, filtering capabilities).

**Hybrid search** (p. 222): BM25 (keyword) + vector (semantic) search → re-rank combined results. Outperforms either alone.

**Agentic RAG** (p. 227): Agent decides what to retrieve (query reformulation), when to retrieve (iteratively), and from which source:
```python
# Agent uses retrieval as a tool
tools = [
    search_knowledge_base,   # Vector search over internal docs
    search_web,              # Real-time web search
    query_sql_database,      # Structured data retrieval
]
# Agent selects and combines sources based on the query
```

**GraphRAG** (p. 224): Build a knowledge graph from documents; retrieve both nodes (facts) and edges (relationships) for relational queries. Better than flat vector search for "how does X relate to Y" queries.

**Key rules:**
1. Chunk documents at natural boundaries (sentence/paragraph), not fixed character counts (p. 218).
2. Include source metadata (document title, page, timestamp) in each chunk — enables citations in answers (p. 219).
3. Use hybrid search (BM25 + vector) for production retrieval — significantly better recall than either alone (p. 222).
4. Implement a re-ranker (cross-encoder) after initial retrieval to improve relevance of top-K results (p. 223).
5. Set a relevance threshold — if no chunk exceeds the threshold, acknowledge the knowledge gap rather than hallucinating (p. 225).

## Variants
- **Naive RAG**: Single-round retrieval at query time (simplest, baseline).
- **Advanced RAG**: Query expansion, re-ranking, hybrid search.
- **Agentic RAG**: Agent controls retrieval strategy (iterative, multi-source) (p. 227).
- **GraphRAG**: Knowledge graph + vector retrieval for relational queries (p. 224).
- **VertexAiRagMemoryService**: Managed Google Cloud RAG for agent long-term memory (p. 155, Ch 8).

## Failure Modes
- **Retrieval failure**: Top-K chunks are irrelevant → model hallucinates without grounding. Mitigation: relevance threshold; fallback to "I don't know."
- **Chunk boundary truncation**: Answer spans two chunks; neither chunk individually contains the full answer. Mitigation: overlapping chunks (e.g., 50-token overlap).
- **Stale knowledge**: Document corpus not updated → outdated answers. Mitigation: incremental indexing pipeline with freshness metadata.
- **Context window overflow**: Too many retrieved chunks overflow the context window. Mitigation: set max_chunks; compress/summarize retrieved context.

## Instrumentation
- Log: query, retrieved chunk IDs, relevance scores, generated answer.
- Track: retrieval precision (% of retrieved chunks used in final answer), recall (% of queries with relevant chunks in top-K).
- Alert: if mean relevance score drops below threshold (corpus/query distribution shift).

## Eval
- Build a QA dataset with (question, ground-truth document) pairs.
- Measure: Recall@K (is the ground-truth chunk in top-K?), Precision@K.
- Measure end-to-end: answer correctness against ground truth (with and without RAG).

## Related Patterns
- **Memory Management** (p. 141): RAG for external knowledge; Memory for agent-specific state.
- **Tool Use** (p. 81): In Agentic RAG, retrieval is a tool the agent can invoke.
- **Multi-Agent Collaboration** (p. 121): Specialized retrieval agents can serve knowledge to a generation agent.

## Evidence
- p. 215-228: RAG chapter. Pipeline, chunking, vector DBs, hybrid search, GraphRAG, Agentic RAG.
- p. 217: Core RAG pipeline: Ingestion → Retrieval → Augmentation → Generation.
- p. 220: Vector database options: Pinecone, Weaviate, ChromaDB, FAISS.
- p. 222: Hybrid search: BM25 + vector → re-rank.
- p. 224: GraphRAG for relational queries.
- p. 227: Agentic RAG — agent controls retrieval strategy.
