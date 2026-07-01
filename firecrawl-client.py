# pip install firecrawl-py
from firecrawl import Firecrawl

app = Firecrawl(api_key="fc-086a1637d6e94eb6b7040655bc9bab4d")

# Scrape a website:
print(app.scrape('firecrawl.dev'))
