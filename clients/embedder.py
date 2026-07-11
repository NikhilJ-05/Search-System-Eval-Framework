import asyncio
import logging
from typing import List, Tuple, Dict
import threading

logger = logging.getLogger(__name__)

class BGEm3Embedder:
    def __init__(self):
        self._model = None
        self._lock = threading.Lock()

    def _get_model(self):
        if self._model is None:
            with self._lock:
                if self._model is None:
                    try:
                        import os
                        import tqdm.std
                        
                        _tqdm_orig = tqdm.std.tqdm
                        class _TqdmSilent(_tqdm_orig):
                            def __init__(self, *a, **k):
                                k["disable"] = True
                                super().__init__(*a, **k)
                        tqdm.std.tqdm = _TqdmSilent
                        import tqdm as _tqdm_mod
                        _tqdm_mod.tqdm = _TqdmSilent
                        
                        os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"
                        from FlagEmbedding import BGEM3FlagModel
                    except ImportError:
                        raise ImportError("FlagEmbedding is not installed.")
                        
                    import torch
                    use_fp16 = torch.cuda.is_available()
                    logger.info(f"Loading BAAI/bge-m3 locally via FlagEmbedding (use_fp16={use_fp16})...")
                    self._model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=use_fp16)
        return self._model

    def embed(self, texts: List[str], max_length: int = 512) -> Tuple[List[List[float]], List[Dict[int, float]]]:
        model = self._get_model()
        output = model.encode(
            texts,
            batch_size=12,
            max_length=max_length,
            return_dense=True,
            return_sparse=True,
            return_colbert_vecs=False,
        )

        dense_vecs = [v.tolist() for v in output["dense_vecs"]]

        tokenizer = model.tokenizer
        sparse_vecs = []
        for lw in output["lexical_weights"]:
            token_id_weights = {}
            for token_str, weight in lw.items():
                token_id = tokenizer.convert_tokens_to_ids(token_str)
                if isinstance(token_id, int) and token_id >= 0:
                    token_id_weights[token_id] = float(weight)
            sparse_vecs.append(token_id_weights)

        return dense_vecs, sparse_vecs

_bge_m3_embedder = BGEm3Embedder()
# Semaphore prevents concurrent model calls (PyTorch model is not thread-safe for
# concurrent asyncio.to_thread calls — they'd share the same thread pool and contend).
_embed_semaphore = asyncio.Semaphore(1)

class EmbedderClient:
    async def warmup(self) -> None:
        logger.info("Warming up local BGE-M3 embedder...")
        try:
            async with _embed_semaphore:
                await asyncio.to_thread(_bge_m3_embedder.embed, ["warmup"])
            logger.info("BGE-M3 embedder ready.")
        except Exception as e:
            logger.error(f"BGE-M3 embedder warm-up failed: {e}")
            raise

    async def get_embeddings(self, texts: List[str], max_length: int = 1024) -> Tuple[List[List[float]], List[Dict[int, float]]]:
        async with _embed_semaphore:
            return await asyncio.to_thread(_bge_m3_embedder.embed, texts, max_length)

    async def embed_batched(self, texts: List[str], batch_size: int = 4, max_length: int = 8192) -> Tuple[List[List[float]], List[Dict[int, float]]]:
        """Embed all texts in small serialized mini-batches, logging progress and yielding control."""
        if not texts:
            return [], []

        dense_results = []
        sparse_results = []
        total = len(texts)

        logger.info(f"Starting batch embedding of {total} items (mini-batch size: {batch_size})")

        for i in range(0, total, batch_size):
            chunk_slice = texts[i:i+batch_size]
            logger.info(f"Embedding items {i+1} to {min(i+batch_size, total)} of {total}...")
            
            async with _embed_semaphore:
                dense, sparse = await asyncio.to_thread(_bge_m3_embedder.embed, chunk_slice, max_length)
                
            dense_results.extend(dense)
            sparse_results.extend(sparse)
            await asyncio.sleep(0.02) # Yield control to let event loop tick

        logger.info(f"Successfully embedded all {total} items.")
        return dense_results, sparse_results
