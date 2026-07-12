import asyncio
import os
from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient

load_dotenv()

async def main():
    url = os.environ.get("QDRANT_URL")
    api_key = os.environ.get("QDRANT_API_KEY")
    print(f"Connecting to Qdrant at {url}")
    
    client = AsyncQdrantClient(url=url, api_key=api_key, timeout=10.0)
    
    try:
        collections = await client.get_collections()
        print("Success:", collections)
    except Exception as e:
        print("Failed:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
