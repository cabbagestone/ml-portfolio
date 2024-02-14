import os
import sys
from dotenv import load_dotenv
from redis import Redis
from wikifetcher import WikiFetcher
from pagetools import redis_index_pipeline, link_generator

def main():
  load_dotenv()

  redis_host = os.getenv("REDIS_HOST")
  redis_port = os.getenv("REDIS_PORT")

  redis_client = Redis(host=redis_host, port=redis_port)

  try:
    redis_client.ping()
    print("Connected to Redis successfully!")
  except Exception as e:
    print("Failed to connect to Redis." + str(e))
    return
  
  fetcher = WikiFetcher()

  searchTerm = sys.argv[1]
  searchURL = "https://en.wikipedia.org/wiki/Special:Search?go=Go&search="+searchTerm+"&ns0=1"

  page = fetcher.fetch_wikipedia(searchURL)

  redis_index_pipeline(page, searchURL, redis_client)

  for pageURL in link_generator(page):
    print("https://en.wikipedia.org" + pageURL.get('href'))


if __name__ == "__main__":
  main()