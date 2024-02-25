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
            key = f"Index:{word}"
            p.hset(key, url, count)
    p.execute()
