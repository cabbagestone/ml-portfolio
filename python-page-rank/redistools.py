"""
Module name: redistools
"""

import os
import sys
from collections import Counter

from dotenv import load_dotenv
from redis import Redis, RedisError


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


def redis_index_pipeline(word_iterator, url, r: Redis):
    """
    Function that creates a Redis pipeline to index the words in the given root
    and updates the index with the given URL.

    Parameters:
    - word_iterator: Iterator that yields the words to index.
    - url: The URL of the page to index.
    - r: Redis client object used to interact with Redis.
    """

    counter = Counter(word_iterator)
    p = r.pipeline(transaction=False)
    for word, count in counter.items():
        if count >= 3:
            hash_key = f"Index:{word}"
            sorted_set_key = f"IndexSorted:{word}"
            p.hset(hash_key, url, count)
            p.zadd(sorted_set_key, {url: count})
    p.execute()


def linked_pages(r: Redis, url):
    """
    Function that returns the URLs of the pages that are linked to the given URL.
    If it doesn't exist, it returns an empty list.

    Parameters:
    - r: Redis client object used to interact with Redis.
    - url: The URL of the page to get the linked pages for.

    Returns:
    - A list of URLs of the pages that are linked to the given URL.
    """
    key = f"Links:{url}"

    if not r.exists(key):
        return []

    return r.smembers(key)


def store_page_links(r: Redis, url, page_links):
    """
    Function that stores the URLs of the pages that are linked to the given URL.

    Parameters:
    - r: Redis client object used to interact with Redis.
    - url: The URL of the page to store the linked pages for.
    - linked_pages: A list of URLs of the pages that are linked to the given URL.
    """
    key = f"Links:{url}"
    r.sadd(key, *page_links)

    # to-do: use r.expire(key, {some_seconds}) to handle cache invalidation for page changes


def get_sorted_index_list_for_word(r: Redis, word):
    """
    Modified function to retrieve a sorted list of URLs and counts for the given word
    using a Sorted Set to efficiently manage sorted data.

    This version assumes that during indexing, scores (counts) for words are stored in a Sorted Set
    with a key pattern like "IndexSorted:{word}", where each member of the set is a URL
    and its score represents the count (or any other metric determining the order).

    Parameters:
    - r: Redis client object used to interact with Redis.
    - word: The word to get the index list for.

    Returns:
    - A list of tuples containing the URL and count for the given word, sorted by count.
    """
    sorted_set_key = f"IndexSorted:{word}"

    page_index_scores = r.zrevrange(sorted_set_key, 0, -1, withscores=True)

    sorted_list = [
        (member.decode("utf-8"), int(score)) for member, score in page_index_scores
    ]

    return sorted_list


def get_index_for_page_for_search_term(r: Redis, search_term, url):
    """
    Function that returns the index score for the given page and search term.

    Parameters:
    - r: Redis client object used to interact with Redis.
    - search_term: The search term entered by the user.
    - url: The URL of the page to get the index score for.

    Returns:
    - The index score for the given page and search term.
    """
    key = f"Index:{search_term}"
    count = r.hget(key, url)

    if count is None:
        return 0

    return int(count)


def get_highest_index_for_search_term(r: Redis, search_term):
    """
    retrieve the highest index score for a search term using Sorted Sets
    """
    sorted_set_key = f"IndexSorted:{search_term}"
    highest_scores = r.zrange(sorted_set_key, -1, -1, withscores=True)

    if not highest_scores:
        return 0

    # The zrange will return a list of tuples [(url, score)]
    _, highest_score = highest_scores[0]
    return int(highest_score)
