"""
Module name: main

Author: Cabbage Stone

Date: 02-24-2024

This module is responsible for interacting with a Redis database 
and handling user search terms. 

Example usage:

    python main.py

"""

import os
import sys
from dotenv import load_dotenv
from redis import Redis, RedisError
from wikifetcher import WikiFetcher
from pagetools import redis_index_pipeline, link_generator


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


def connect_to_redis():
    """
    Function that connects to Redis and returns the Redis client object.
    performs a ping to check if the connection was successful.

    Returns:
    - Redis client object used to interact with Redis.
    """
    load_dotenv()

    redis_host = os.getenv("REDIS_HOST")
    redis_port = os.getenv("REDIS_PORT")

    client = Redis(host=redis_host, port=redis_port)

    try:
        client.ping()
        print("Connected to Redis successfully!")
    except RedisError as e:
        print("Failed to connect to Redis." + str(e))
        sys.exit(1)

    return client


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

    page = fetcher.fetch_wikipedia(search_url)

    redis_index_pipeline(page, search_url, redis_client)

    for page_url in link_generator(page):
        print("https://en.wikipedia.org" + page_url.get("href"))


if __name__ == "__main__":
    main()
