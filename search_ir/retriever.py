import logging
import time
import json
import uuid
import asyncio
import dataclasses
from typing import List, Dict, Any, Optional, Tuple
from clients.embedder import EmbedderClient
from search_ir.qdrant_store import QdrantStore
from qdrant_client.models import Prefetch, SparseVector, FusionQuery, Fusion, PointStruct, Filter, FieldCondition, MatchValue, Range, FilterSelector
from models.eval_result import FirecrawlSearchResult

logger = logging.getLogger(__name__)

class Retriever:
    def __init__(self, qdrant: QdrantStore, embedder: EmbedderClient):
        self.qdrant = qdrant
        self.embedder = embedder

    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        if not self.qdrant.config.qdrant_url:
            return []

        dense_vecs, sparse_vecs = await self.embedder.get_embeddings([query])
        dense_vector = dense_vecs[0]
        sparse_vector = sparse_vecs[0] if sparse_vecs else None
        
        prefetch = [
            Prefetch(query=dense_vector, using="dense", limit=limit * 3)
        ]
        if sparse_vector:
            prefetch.append(
                Prefetch(
                    query=SparseVector(
                        indices=list(sparse_vector.keys()),
                        values=list(sparse_vector.values())
                    ),
                    using="sparse",
                    limit=limit * 3
                )
            )
            
        search_result = await self.qdrant.client.query_points(
            collection_name=self.qdrant.config.qdrant_collection,
            prefetch=prefetch,
            query=FusionQuery(fusion=Fusion.RRF),
            limit=limit,
            with_payload=True
        )
        
        results = []
        for point in search_result.points:
            results.append({
                "score": point.score,
                "url": point.payload.get("url"),
                "content": point.payload.get("content")
            })
            
        return results

    async def lookup_by_url(self, url: str) -> Optional[Dict]:
        """Check if KB already has content for this exact URL (exact URL match, no semantic scoring)."""
        if not self.qdrant.config.qdrant_url:
            return None
            
        results, _ = await self.qdrant.client.scroll(
            collection_name=self.qdrant.config.qdrant_collection,
            scroll_filter=Filter(must=[
                FieldCondition(key="url", match=MatchValue(value=url))
            ]),
            limit=1,
            with_payload=True
        )
        if results:
            point = results[0]
            return {
                "content": point.payload.get("content"),
                "scrape_timestamp": point.payload.get("scrape_timestamp", 0),
                "content_hash": point.payload.get("content_hash"),
                "url": point.payload.get("url"),
                "score": 1.0
            }
        return None

    async def _get_kb_content_for_url_with_vectors(
        self, dense_vector: List[float], sparse_vector: Optional[Dict[int, float]], url: str, score_threshold: float = 0.45
    ) -> Optional[Dict]:
        """Core hybrid BM25+vector search for a URL using pre-computed vectors."""
        url_filter = Filter(must=[FieldCondition(key="url", match=MatchValue(value=url))])

        prefetch = [Prefetch(query=dense_vector, using="dense", limit=10, filter=url_filter)]
        if sparse_vector:
            prefetch.append(
                Prefetch(
                    query=SparseVector(
                        indices=list(sparse_vector.keys()),
                        values=list(sparse_vector.values())
                    ),
                    using="sparse",
                    limit=10,
                    filter=url_filter
                )
            )

        search_result = await self.qdrant.client.query_points(
            collection_name=self.qdrant.config.qdrant_collection,
            prefetch=prefetch,
            query=FusionQuery(fusion=Fusion.RRF),
            limit=10,
            with_payload=True
        )

        if not search_result.points:
            return None

        # Filter to points actually belonging to this URL and above score threshold
        matching = [
            p for p in search_result.points
            if p.payload.get("url") == url and p.score >= score_threshold
        ]
        if not matching:
            return None

        best_score = max(p.score for p in matching)
        
        # We have a semantic hit! Now retrieve ALL chunks for this URL to reconstruct the FULL document.
        # We cannot rely on `search_result` because it was limited to 10 chunks and ranked by relevance.
        scroll_res, _ = await self.qdrant.client.scroll(
            collection_name=self.qdrant.config.qdrant_collection,
            scroll_filter=url_filter,
            limit=10000,
            with_payload=True
        )
        
        if not scroll_res:
            return None

        # Reassemble all chunks in original page order via chunk_index
        all_chunks_sorted = sorted(scroll_res, key=lambda p: p.payload.get("chunk_index", 0))
        full_content = "\n\n".join(p.payload.get("content", "") for p in all_chunks_sorted)
        oldest_ts = min(p.payload.get("scrape_timestamp", 0) for p in all_chunks_sorted)
        doc_hash = all_chunks_sorted[0].payload.get("doc_content_hash", all_chunks_sorted[0].payload.get("content_hash", ""))

        return {
            "content": full_content,
            "scrape_timestamp": oldest_ts,
            "content_hash": doc_hash,
            "url": url,
            "score": best_score,
            "num_chunks": len(all_chunks_sorted)
        }

    async def get_kb_content_for_url(self, query: str, url: str, score_threshold: float = 0.45) -> Optional[Dict]:
        """Hybrid BM25+vector search restricted to a specific URL.
        If any chunk scores above the threshold, fetches and reconstructs the FULL document.
        This is the semantic Layer 2: query-aware hit detection, followed by full document retrieval.
        """
        if not self.qdrant.config.qdrant_url:
            return None

        dense_vecs, sparse_vecs = await self.embedder.get_embeddings([query])
        dense_vector = dense_vecs[0]
        sparse_vector = sparse_vecs[0] if sparse_vecs else None

        return await self._get_kb_content_for_url_with_vectors(
            dense_vector, sparse_vector, url, score_threshold
        )

    async def get_kb_coverage_for_urls(
        self, query: str, urls: List[str], score_threshold: float = 0.45,
        precomputed_dense_vec: Optional[List[float]] = None,
        precomputed_sparse_vec: Optional[Dict[int, float]] = None
    ) -> Dict[str, Optional[Dict]]:
        """Run get_kb_content_for_url for a list of URLs concurrently.
        Returns a dict of url → result (or None if no qualifying content).
        """
        if not self.qdrant.config.qdrant_url or not urls:
            return {url: None for url in urls}

        if precomputed_dense_vec is not None:
            dense_vector = precomputed_dense_vec
            sparse_vector = precomputed_sparse_vec
        else:
            dense_vecs, sparse_vecs = await self.embedder.get_embeddings([query])
            dense_vector = dense_vecs[0]
            sparse_vector = sparse_vecs[0] if sparse_vecs else None

        tasks = [
            self._get_kb_content_for_url_with_vectors(dense_vector, sparse_vector, url, score_threshold)
            for url in urls
        ]
        results = await asyncio.gather(*tasks)
        return {url: result for url, result in zip(urls, results)}

    async def find_similar_query(
        self, query: str, threshold: float = 0.92, max_age_seconds: int = 120
    ) -> Tuple[Optional[Dict], Optional[List[float]], Optional[Dict[int, float]]]:
        """Check if we've searched a near-identical query recently.
        Returns a tuple of (hit_dict_or_None, query_dense_vector, query_sparse_vector).
        """
        if not self.qdrant.config.qdrant_url:
            return None, None, None
            
        dense_vecs, sparse_vecs = await self.embedder.get_embeddings([query])
        dense_vec = dense_vecs[0]
        sparse_vec = sparse_vecs[0] if sparse_vecs else None
        
        results = await self.qdrant.client.query_points(
            collection_name="firecrawl_query_cache",
            query=dense_vec,
            using="dense",
            limit=1,
            with_payload=True,
            score_threshold=threshold
        )
        
        if results.points:
            point = results.points[0]
            age = time.time() - point.payload.get("timestamp", 0)
            if age < max_age_seconds:
                # deserialize results
                results_data = json.loads(point.payload.get("results", "[]"))
                fc_results = []
                for rd in results_data:
                    fc_results.append(FirecrawlSearchResult(**rd))
                    
                return {
                    "original_query": point.payload.get("query"),
                    "results": fc_results,
                    "similarity": point.score,
                    "age_seconds": age
                }, dense_vec, sparse_vec
        return None, dense_vec, sparse_vec

    async def store_search_results(
        self, query: str, results: List[FirecrawlSearchResult], precomputed_dense_vec: Optional[List[float]] = None
    ):
        """Cache search results for future query dedup."""
        if not self.qdrant.config.qdrant_url:
            return
            
        if precomputed_dense_vec is not None:
            dense_vector = precomputed_dense_vec
        else:
            dense_vecs, _ = await self.embedder.get_embeddings([query])
            dense_vector = dense_vecs[0]
        
        # Serialize without massive markdown to save payload space
        results_clean = []
        for r in results:
            d = dataclasses.asdict(r)
            d["full_markdown"] = None # don't cache scrape content here, that's Layer 2
            results_clean.append(d)
            
        await self.qdrant.client.upsert(
            collection_name="firecrawl_query_cache",
            points=[PointStruct(
                id=str(uuid.uuid4()),
                vector={"dense": dense_vector},
                payload={
                    "query": query,
                    "results": json.dumps(results_clean),
                    "timestamp": time.time()
                }
            )]
        )

    async def evict_stale_query_cache(self, max_age_seconds: int) -> int:
        """Evict query cache entries older than max_age_seconds."""
        if not self.qdrant.config.qdrant_url:
            return 0
            
        now = time.time()
        cutoff = now - max_age_seconds
        
        logger.info(f"[Retriever] Scanning query cache for entries older than {max_age_seconds} seconds (cutoff timestamp < {cutoff:.0f})...")
        
        try:
            res = await self.qdrant.client.delete(
                collection_name="firecrawl_query_cache",
                points_selector=FilterSelector(
                    filter=Filter(
                        must=[
                            FieldCondition(
                                key="timestamp",
                                range=Range(lt=cutoff)
                            )
                        ]
                    )
                )
            )
            logger.info(f"[Retriever] Query cache eviction complete. Status: {res}")
            return 1
        except Exception as e:
            logger.warning(f"[Retriever] Failed to evict stale query cache: {e}")
            return 0
