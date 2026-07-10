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

class Indexer:
    def __init__(self, qdrant: QdrantStore, embedder: EmbedderClient):
        self.qdrant = qdrant
        self.embedder = embedder

    def _chunk_markdown(self, markdown: str, overlap_ratio: float = 0.15) -> List[str]:
        """Adaptive chunker: no hard truncation. Chunk size scales with document length.
        Overlap: ~15% of target chunk size carried over to the next chunk.
        """
        if not markdown:
            return []

        doc_len = len(markdown)
        # Scales target chunk size based on document length to keep chunk count reasonable:
        # starts at 1500, adds 500 for every 10k characters, capped at 5000 chars.
        target_chunk_size = min(5000, 1500 + (doc_len // 10000) * 500)
        overlap_size = int(target_chunk_size * overlap_ratio)

        lines = markdown.split('\n')
        chunks = []
        current_lines = []
        current_len = 0
        overlap_tail = ""

        for line in lines:
            line_len = len(line) + 1  # +1 for \n

            # Heading boundary: flush if current chunk is substantial (> 40% of target)
            if line.startswith('#') and current_len > target_chunk_size * 0.4:
                chunk_text = overlap_tail + '\n'.join(current_lines)
                chunks.append(chunk_text)
                overlap_tail = chunk_text[-overlap_size:] if len(chunk_text) > overlap_size else chunk_text
                current_lines = [line]
                current_len = line_len
                continue

            current_lines.append(line)
            current_len += line_len

            if current_len >= target_chunk_size:
                chunk_text = overlap_tail + '\n'.join(current_lines)
                chunks.append(chunk_text)
                overlap_tail = chunk_text[-overlap_size:] if len(chunk_text) > overlap_size else chunk_text
                current_lines = []
                current_len = 0

        if current_lines or overlap_tail:
            # Avoid writing an empty or duplicate chunk if nothing new was added
            chunk_text = overlap_tail + '\n'.join(current_lines)
            if chunk_text.strip() and chunk_text != overlap_tail:
                chunks.append(chunk_text)

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
            doc_hash = hashlib.sha256(result.full_markdown.encode()).hexdigest()
            total_chunks = len(chunks)
            for idx, chunk in enumerate(chunks):
                chunks_to_embed.append(chunk)
                chunk_metadata.append((chunk, result, idx, total_chunks, doc_hash))

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
        for i, (chunk, result, chunk_idx, total_chunks, doc_hash) in enumerate(chunk_metadata):
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
                        "doc_content_hash": doc_hash,
                        "content": chunk,
                        "chunk_index": chunk_idx,
                        "total_chunks": total_chunks,
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
        point_metadata = [] # stores (chunk_text, url, query_origin, content_hash, doc_content_hash, chunk_index, total_chunks)
        
        logger.info(f"[Indexer] Processing batch of {len(new_entries)} new entries for dedup and indexing...")
        
        # 1. Chunk all documents and compute hashes first
        prepared_entries = []
        all_chunk_hashes = []
        for url, markdown, query in new_entries:
            chunks = self._chunk_markdown(markdown)
            if not chunks:
                continue
            doc_hash = hashlib.sha256(markdown.encode()).hexdigest()
            total_chunks = len(chunks)
            stats.total_chunks += total_chunks
            
            doc_chunks = []
            for idx, chunk in enumerate(chunks):
                content_hash = hashlib.sha256(chunk.encode()).hexdigest()
                all_chunk_hashes.append(content_hash)
                doc_chunks.append((chunk, content_hash, idx, total_chunks, doc_hash))
            prepared_entries.append((url, query, doc_chunks))

        # 2. Bulk retrieve existing hashes from Qdrant in a single scroll
        existing_hashes = set()
        if all_chunk_hashes:
            try:
                should_conditions = [FieldCondition(key="content_hash", match=MatchValue(value=h)) for h in all_chunk_hashes]
                scroll_res, _ = await self.qdrant.client.scroll(
                    collection_name=self.qdrant.config.qdrant_collection,
                    scroll_filter=Filter(should=should_conditions),
                    limit=len(all_chunk_hashes),
                    with_payload=True,
                    with_vectors=False
                )
                for point in scroll_res:
                    if point.payload and "content_hash" in point.payload:
                        existing_hashes.add(point.payload["content_hash"])
            except Exception as e:
                logger.warning(f"[Indexer] Batch dedup scroll failed: {e}. Falling back to full local scroll.")
                try:
                    scroll_res, _ = await self.qdrant.client.scroll(
                        collection_name=self.qdrant.config.qdrant_collection,
                        limit=1000,
                        with_payload=True,
                        with_vectors=False
                    )
                    for point in scroll_res:
                        if point.payload and "content_hash" in point.payload:
                            existing_hashes.add(point.payload["content_hash"])
                except Exception as ex:
                    logger.error(f"[Indexer] Critical: fallback scroll failed: {ex}")

        # 3. Filter out existing chunks locally
        for url, query, doc_chunks in prepared_entries:
            for chunk, content_hash, idx, total_chunks, doc_hash in doc_chunks:
                if content_hash in existing_hashes:
                    stats.deduped += 1
                else:
                    chunks_to_embed.append(chunk)
                    point_metadata.append((chunk, url, query, content_hash, doc_hash, idx, total_chunks))
                    
        if chunks_to_embed:
            logger.info(f"[Indexer] Batch embedding {len(chunks_to_embed)} new deduplicated chunks...")
            t0 = time.time()
            dense_vecs, sparse_vecs = await self.embedder.embed_batched(chunks_to_embed)
            elapsed = time.time() - t0
            logger.info(f"[Indexer] Batch embeddings done in {elapsed:.1f}s")
            
            points = []
            for i, (chunk, url, query, content_hash, doc_hash, idx, total_chunks) in enumerate(point_metadata):
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
                            "doc_content_hash": doc_hash,
                            "content": chunk,
                            "chunk_index": idx,
                            "total_chunks": total_chunks,
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
