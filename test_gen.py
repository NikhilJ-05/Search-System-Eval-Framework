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
        print(f"--- TestCase: {c.id} ---")
        print(f"Query: {c.query}")
        print(f"Domain/Category: {c.category}")
        print(f"Intent: {c.intent}")
        print(f"Difficulty: {c.difficulty}")
        print(f"Chaos Archetype: {c.chaos_archetype}")
        print(f"Cache Relationship: {c.cache_relationship}")
        if c.rubric:
            print("Rubric Dimensions:")
            for idx, dim in enumerate(c.rubric.dimensions):
                print(f"  {idx+1}. {dim.name} (wt: {dim.weight})")
                print(f"     Criteria: {dim.criteria}")
                print(f"     Fail if: {dim.contrastive_fail}")
            print(f"Grading Notes: {c.rubric.grading_notes}")
        print()
    await or_pool.aclose()

if __name__ == "__main__":
    asyncio.run(main())
