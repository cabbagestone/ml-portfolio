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
  
  while True:
    fetcher = WikiFetcher()

    searchTerm = input("Enter a search term or !help: ")

    if searchTerm.startswith("!"):
      if searchTerm == "!help":
        print("type !exit to exit the program.")
        print("type !help to see this message.")
        continue
      elif searchTerm == "!exit":
        print("Exiting program.")
        sys.exit()
      else:
        print("Unknown command. Type !help for help.")
        continue

    searchURL = "https://en.wikipedia.org/wiki/Special:Search?go=Go&search="+searchTerm+"&ns0=1"

    page = fetcher.fetch_wikipedia(searchURL)

    redis_index_pipeline(page, searchURL, redis_client)

    # the end result should be that I have a list of urls sorted by the index of the page and the quality of the links to the page
    # I need to figure out how to sort the links by the quality of the links to the page
    # I need to create a graph that connects the pages to each other
    # also need some way to store the graph in redis
    # there's also the index of the page to consider
    # maybe I'll take the top ten index pages and then sort the links by the quality of the links to the page
    # the problem there is that the quality measurement cannot be taken from that sample.
    # so perhaps I take make a hash representing the URL, and then I store connected urls in there?
    # doesn't sound terrible... but I feel like it's not quite there yet.

    # For each search term, I need to do the following:
    # 1. Fetch the search page
    # 2. Perform page functionality
    # 3. Return the top 10 pages

    # For every page I search, I need to do the following:
    # 0. Check to see if the page already has an index, and therefore a pagerank
    # 1. Create the page index
    # 2. Update relevant pagerank scores
    # 3. Follow connected pages if max number of pages is not reached 
    #    (don't count pages that already have an index)

    # In order to create a list of results:
    # 1. Get the top index-scoring pages
    # 2. Get the top page-rank scoring pages from the top index-scoring pages
    # 3. Get the hybrid scores of these pages
    # 4. return the list

    for pageURL in link_generator(page):
      print("https://en.wikipedia.org" + pageURL.get('href'))

if __name__ == "__main__":
  main()