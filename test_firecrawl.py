import asyncio
import logging
from config import EvalConfig
from clients.firecrawl_client import FirecrawlClientPool

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    config = EvalConfig.from_env()
    fc_pool = FirecrawlClientPool(config)

    query = "best python web scraping libraries 2025"
    print(f"\n[TEST] Testing Firecrawl Search Endpoint...")
    print(f"Query: '{query}'\n")

    try:
        # Test 1: Search Endpoint
        results, latency = await fc_pool.search(query, limit=3)
        print(f"[OK] Search successful! (Latency: {latency:.2f}ms)")
        print(f"Found {len(results)} results:")
        
        for idx, res in enumerate(results):
            print(f"\n--- Result {idx + 1} ---")
            print(f"Title:   {res.title}")
            print(f"URL:     {res.url}")
            print(f"Snippet: {res.snippet[:100]}...")

        # Test 2: Scrape Endpoint
        if results:
            first_url = results[0].url
            print(f"\n[TEST] Testing Firecrawl Scrape Endpoint on top result...")
            print(f"URL: {first_url}\n")
            
            markdown, scrape_latency, status = await fc_pool.scrape(first_url)
            
            if markdown:
                print(f"[OK] Scrape successful! (Latency: {scrape_latency:.2f}ms)")
                print(f"Content Length: {len(markdown)} characters")
                print("Preview:")
                print(markdown[:300] + "...\n")
            else:
                print(f"[FAIL] Scrape failed. Status: {status}")

    except Exception as e:
        print(f"\n[FAIL] Error during testing: {e}")

if __name__ == "__main__":
    asyncio.run(main())
