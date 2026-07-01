import asyncio
from config import EvalConfig
from clients.openrouter import OpenRouterClientPool
from eval.test_generator import TestGenerator

async def main():
    config = EvalConfig.from_env()
    or_pool = OpenRouterClientPool(config)
    gen = TestGenerator(config, or_pool)
    cases = await gen.generate(4, ['old query 1', 'old query 2'])
    for c in cases:
        print(f"{c.cache_intent}: {c.query} ({c.category})")
    await or_pool.aclose()

if __name__ == "__main__":
    asyncio.run(main())
