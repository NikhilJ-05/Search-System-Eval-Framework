import hashlib
import time
import uuid
import logging
from typing import List, Tuple
from dataclasses import dataclass
from models.eval_result import FirecrawlSearchResult
from clients.embedder import EmbedderClient
from search_ir.qdrant_store import QdrantStore
from qdrant_client.models import PointStruct, SparseVector, Filter, FieldCondition, MatchValue, FilterSelector

logger = logging.getLogger(__name__)

@dataclass
class IndexStats:
    new_indexed: int
    updated: int
    deduped: int
    total_chunks: int

# Max chunks per document to keep indexing fast on CPU
MAX_CHUNKS_PER_DOC = 5
# Max chars of markdown to embed per document
MAX_MARKDOWN_CHARS = 8000

class Indexer:
    def __init__(self, qdrant: QdrantStore, embedder: EmbedderClient):
        self.qdrant = qdrant
        self.embedder = embedder

    def _chunk_markdown(self, markdown: str) -> List[str]:
        """Split markdown into chunks of ~2000 chars, capped at MAX_CHUNKS_PER_DOC."""
        if not markdown:
            return []

        # Truncate early to avoid enormous embedding jobs
        markdown = markdown[:MAX_MARKDOWN_CHARS]

        chunks = []
        current_chunk = ""
        for line in markdown.split('\n'):
            if line.startswith('#') and len(current_chunk) > 500:
                chunks.append(current_chunk)
                current_chunk = line + "\n"
            else:
                current_chunk += line + "\n"

            if len(current_chunk) > 2000:
                chunks.append(current_chunk)
                current_chunk = ""

        if current_chunk:
            chunks.append(current_chunk)

        if len(chunks) > MAX_CHUNKS_PER_DOC:
            logger.debug(f"[Indexer] Capping {len(chunks)} chunks → {MAX_CHUNKS_PER_DOC}")
            chunks = chunks[:MAX_CHUNKS_PER_DOC]

        return chunks

    async def index_results(self, query: str, results: List[FirecrawlSearchResult]):
        if not self.qdrant.config.qdrant_url:
            logger.debug("[Indexer] No Qdrant URL configured, skipping indexing.")
            return

        chunks_to_embed = []
        chunk_metadata = []

        for result in results:
            if not result.full_markdown:
                continue
            chunks = self._chunk_markdown(result.full_markdown)
            for chunk in chunks:
                chunks_to_embed.append(chunk)
                chunk_metadata.append((chunk, result))

        if not chunks_to_embed:
            logger.info(f"[Indexer] No chunks to index for query: {repr(query[:60])}")
            return

        logger.info(
            f"[Indexer] Embedding {len(chunks_to_embed)} chunk(s) across {len(results)} URL(s) "
            f"for query: {repr(query[:60])}"
        )
        t0 = time.time()
        dense_vecs, sparse_vecs = await self.embedder.embed_batched(chunks_to_embed)
        elapsed = time.time() - t0
        logger.info(f"[Indexer] Embeddings done in {elapsed:.1f}s")

        points = []
        for i, (chunk, result) in enumerate(chunk_metadata):
            content_hash = hashlib.sha256(chunk.encode()).hexdigest()
            point_id = str(uuid.uuid4())
            points.append(
                PointStruct(
                    id=point_id,
                    vector={
                        "dense": dense_vecs[i],
                        "sparse": SparseVector(
                            indices=list(sparse_vecs[i].keys()),
                            values=list(sparse_vecs[i].values())
                        )
                    },
                    payload={
                        "url": result.url,
                        "query_origin": query,
                        "content_hash": content_hash,
                        "content": chunk,
                        "scrape_timestamp": time.time()
                    }
                )
            )

        if points:
            logger.info(f"[Indexer] Upserting {len(points)} points to Qdrant...")
            t0 = time.time()
            await self.qdrant.client.upsert(
                collection_name=self.qdrant.config.qdrant_collection,
                points=points
            )
            elapsed = time.time() - t0
            logger.info(f"[Indexer] Upsert done in {elapsed:.1f}s — {len(points)} chunks indexed for query: {repr(query[:60])}")

    async def update_existing(self, url: str, new_markdown: str, old_content_hash: str, query_origin: str = "refreshed") -> IndexStats:
        """Replace stale KB entry with fresh content."""
        if not self.qdrant.config.qdrant_url:
            return IndexStats(0, 0, 0, 0)
            
        logger.info(f"[Indexer] Updating stale content for {url}")
        
        # Delete old points matching this URL
        await self.qdrant.client.delete(
            collection_name=self.qdrant.config.qdrant_collection,
            points_selector=FilterSelector(filter=Filter(must=[
                FieldCondition(key="url", match=MatchValue(value=url))
            ]))
        )
        
        # Re-chunk + re-embed + re-index the new content
        fake_result = FirecrawlSearchResult(query=query_origin, firecrawl_rank=1, url=url, title="", snippet="", full_markdown=new_markdown)
        await self.index_results(query_origin, [fake_result])
        return IndexStats(new_indexed=0, updated=1, deduped=0, total_chunks=len(self._chunk_markdown(new_markdown)))

    async def index_batch_deduped(self, new_entries: List[Tuple[str, str, str]]) -> IndexStats:
        """Index only genuinely new URLs, skip existing based on content hash.
        new_entries: List of (url, markdown, query_origin)
        """
        if not self.qdrant.config.qdrant_url or not new_entries:
            return IndexStats(0, 0, 0, 0)
            
        stats = IndexStats(0, 0, 0, 0)
        chunks_to_embed = []
        point_metadata = [] # stores (chunk_text, url, query_origin, content_hash)
        
        logger.info(f"[Indexer] Processing batch of {len(new_entries)} new entries for dedup and indexing...")
        
        for url, markdown, query in new_entries:
            chunks = self._chunk_markdown(markdown)
            if not chunks:
                continue
                
            stats.total_chunks += len(chunks)
            for chunk in chunks:
                content_hash = hashlib.sha256(chunk.encode()).hexdigest()
                
                # Check if hash already exists in Qdrant
                existing, _ = await self.qdrant.client.scroll(
                    collection_name=self.qdrant.config.qdrant_collection,
                    scroll_filter=Filter(must=[FieldCondition(key="content_hash", match=MatchValue(value=content_hash))]),
                    limit=1
                )
                
                if existing:
                    stats.deduped += 1
                else:
                    chunks_to_embed.append(chunk)
                    point_metadata.append((chunk, url, query, content_hash))
                    
        if chunks_to_embed:
            logger.info(f"[Indexer] Batch embedding {len(chunks_to_embed)} new deduplicated chunks...")
            t0 = time.time()
            dense_vecs, sparse_vecs = await self.embedder.embed_batched(chunks_to_embed)
            elapsed = time.time() - t0
            logger.info(f"[Indexer] Batch embeddings done in {elapsed:.1f}s")
            
            points = []
            for i, (chunk, url, query, content_hash) in enumerate(point_metadata):
                points.append(
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector={
                            "dense": dense_vecs[i],
                            "sparse": SparseVector(
                                indices=list(sparse_vecs[i].keys()),
                                values=list(sparse_vecs[i].values())
                            )
                        },
                        payload={
                            "url": url,
                            "query_origin": query,
                            "content_hash": content_hash,
                            "content": chunk,
                            "scrape_timestamp": time.time()
                        }
                    )
                )
            
            logger.info(f"[Indexer] Upserting {len(points)} deduplicated points to Qdrant...")
            await self.qdrant.client.upsert(
                collection_name=self.qdrant.config.qdrant_collection,
                points=points
            )
            stats.new_indexed += len(points)
            
        return stats
