"""
Module name: main

Author: Cabbage Stone

Date: 02-24-2024

This module is responsible for interacting with a Redis database 
and handling user search terms. 

Example usage:

    python main.py

"""

import sys
from collections import deque

from pagetools import link_generator, iterate_words
from redistools import connect_to_redis, redis_index_pipeline
from wikifetcher import WikiFetcher


def main():
    """
    Main function that connects to Redis, prompts the user for a search term,
    and handles the search term by fetching the search page, creating the page index,
    and updating relevant pagerank scores, and then returning the relevant links
    sorted by a hybrid scoring system
    """
    redis_client = connect_to_redis()

    while True:

        search_term = input("Enter a search term or !help: ")

        if handle_command(search_term):
            continue

        handle_search_term(redis_client, search_term)


def handle_command(search_term):
    """
    Function that checks to see if the search_term is a command,
    and if so, executes the command.

    Parameters:
    - search_term: The search term entered by the user.

    Returns:
    - True if the search term was a command, False otherwise.
    """
    if search_term.startswith("!"):
        if search_term == "!help":
            print("type !exit to exit the program.")
            print("type !help to see this message.")
            return True
        if search_term == "!exit":
            print("Exiting program.")
            sys.exit()
        else:
            print("Unknown command. Type !help for help.")
            return True

    return False


def handle_search_term(redis_client, search_term):
    """
    Function that handles the given search term by fetching the search page,
    creating the page index, and updating relevant pagerank scores.

    Parameters:
    - redis_client: Redis client object used to interact with Redis.
    - searchTerm: The search term entered by the user.
    """
    fetcher = WikiFetcher()
    search_url = (
        "https://en.wikipedia.org/wiki/Special:Search?go=Go&search="
        + search_term
        + "&ns0=1"
    )

    # push the page onto the deque
    page_queue = deque([search_url])
    max_page_searches = 100
    current_page_searches = 0

    while page_queue and current_page_searches < max_page_searches:
        search_url = page_queue.popleft()

        # check to see if the page has already been indexed
        # if it has, just get the connected pages we stored for pagerank
        # to append to the page_queue

        page = fetcher.fetch_wikipedia(search_url)

        # run the index pipeline for any new pages
        word_iterator = iterate_words(page)
        redis_index_pipeline(word_iterator, search_url, redis_client)

        for page_url in link_generator(page):
            new_url = "https://en.wikipedia.org" + page_url.get("href")
            page_queue.append(new_url)


if __name__ == "__main__":
    main()
