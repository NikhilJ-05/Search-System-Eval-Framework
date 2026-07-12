from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance, SparseVectorParams, SparseIndexParams, PayloadSchemaType
import logging
import asyncio
from config import EvalConfig

logger = logging.getLogger(__name__)

class SafeAsyncQdrantClient:
    def __init__(self, *args, **kwargs):
        self._client = AsyncQdrantClient(*args, **kwargs)
        
    async def _retry(self, func, *args, **kwargs):
        for attempt in range(5):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == 4:
                    raise
                if attempt == 0:
                    logger.debug(f"Qdrant connection dropped/cold. Waking up server... (error: {e})")
                await asyncio.sleep(1)
                
    async def collection_exists(self, *args, **kwargs):
        return await self._retry(self._client.collection_exists, *args, **kwargs)

    async def create_collection(self, *args, **kwargs):
        return await self._retry(self._client.create_collection, *args, **kwargs)

    async def create_payload_index(self, *args, **kwargs):
        return await self._retry(self._client.create_payload_index, *args, **kwargs)

    async def get_collection(self, *args, **kwargs):
        return await self._retry(self._client.get_collection, *args, **kwargs)

    async def query_points(self, *args, **kwargs):
        return await self._retry(self._client.query_points, *args, **kwargs)

    async def scroll(self, *args, **kwargs):
        return await self._retry(self._client.scroll, *args, **kwargs)

    async def upsert(self, *args, **kwargs):
        return await self._retry(self._client.upsert, *args, **kwargs)

    async def delete(self, *args, **kwargs):
        return await self._retry(self._client.delete, *args, **kwargs)

class QdrantStore:
    def __init__(self, config: EvalConfig):
        self.config = config
        self.client = SafeAsyncQdrantClient(
            url=self.config.qdrant_url,
            api_key=self.config.qdrant_key,
            timeout=10.0
        )

    async def init_collection(self):
        if not self.config.qdrant_url:
            logger.warning("No Qdrant URL provided. Skipping collection init.")
            return

        exists = False
        try:
            exists = await self.client.collection_exists(self.config.qdrant_collection)
        except Exception as e:
            logger.warning(f"Error inspecting Qdrant collection {self.config.qdrant_collection}: {e}.")

        if not exists:
            logger.info(f"Creating Qdrant collection: {self.config.qdrant_collection}")
            try:
                await self.client.create_collection(
                    collection_name=self.config.qdrant_collection,
                    vectors_config={
                        "dense": VectorParams(
                            size=1024,
                            distance=Distance.COSINE
                        )
                    },
                    sparse_vectors_config={
                        "sparse": SparseVectorParams(
                            index=SparseIndexParams(on_disk=False)
                        )
                    }
                )
            except Exception as e:
                if "already exists" in str(e):
                    logger.info(f"Collection {self.config.qdrant_collection} already exists, ignoring creation error.")
                else:
                    raise
        else:
            logger.info(f"Qdrant collection {self.config.qdrant_collection} verified and ready.")
            
        # Always ensure payload indexes exist on main collection
        indexes = ["url", "query_origin", "content_hash", "doc_content_hash", "chunk_index"]
        for field in indexes:
            try:
                await self.client.create_payload_index(
                    collection_name=self.config.qdrant_collection,
                    field_name=field,
                    field_schema=PayloadSchemaType.INTEGER if field == "chunk_index" else PayloadSchemaType.KEYWORD,
                )
            except Exception as e:
                logger.debug(f"Payload index already exists or failed for {field}: {e}")

    async def init_query_cache_collection(self):
        if not self.config.qdrant_url:
            return
            
        cache_coll = "firecrawl_query_cache"
        exists = False
        try:
            exists = await self.client.collection_exists(cache_coll)
        except Exception as e:
            logger.warning(f"Error inspecting Qdrant cache collection {cache_coll}: {e}.")

        if not exists:
            logger.info(f"Creating Qdrant collection: {cache_coll}")
            try:
                await self.client.create_collection(
                    collection_name=cache_coll,
                    vectors_config={
                        "dense": VectorParams(
                            size=1024,
                            distance=Distance.COSINE
                        )
                    }
                )
            except Exception as e:
                if "already exists" in str(e):
                    logger.info(f"Collection {cache_coll} already exists, ignoring creation error.")
                else:
                    raise
        else:
            logger.info(f"Qdrant collection {cache_coll} verified and ready.")

        # Always ensure payload indexes exist on query cache
        for field, schema in [("query", PayloadSchemaType.KEYWORD), ("timestamp", PayloadSchemaType.FLOAT)]:
            try:
                await self.client.create_payload_index(
                    collection_name=cache_coll,
                    field_name=field,
                    field_schema=schema,
                )
            except Exception as e:
                logger.debug(f"Payload index already exists or failed for cache {field}: {e}")

    async def get_collection_stats(self) -> dict:
        if not self.config.qdrant_url:
            return {"points_count": 0, "vectors_count": 0, "status": "local/in-memory"}
        try:
            info = await self.client.get_collection(self.config.qdrant_collection)
            return {
                "points_count": getattr(info, "points_count", 0) or 0,
                "vectors_count": getattr(info, "vectors_count", 0) or 0,
                "status": str(getattr(info, "status", "ok"))
            }
        except Exception as e:
            logger.warning(f"Failed to fetch Qdrant stats: {e}")
            return {"points_count": 0, "vectors_count": 0, "status": "offline"}
