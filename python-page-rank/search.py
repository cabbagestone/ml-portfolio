from collections import deque

from pagetools import link_generator, iterate_words
from redistools import (
    redis_index_pipeline,
    linked_pages,
    store_page_links,
    get_sorted_index_list_for_word,
)
from wikifetcher import WikiFetcher


def handle_search_term(redis_client, search_term):
    """
    Function that handles the given search term by fetching the search page,
    creating the page index, and updating relevant pagerank scores.

    Parameters:
    - redis_client: Redis client object used to interact with Redis.
    - searchTerm: The search term entered by the user.
    """
    fetcher = WikiFetcher()
    search_url = str(
        "https://en.wikipedia.org/wiki/Special:Search?go=Go&search="
        + search_term
        + "&ns0=1"
    )

    page_queue = deque([search_url])
    max_page_searches = 100
    current_page_searches = 0

    # to-do: higher preference on page urls similar to the search term
    # do in-progress adjustment for which pages to search next
    # based on the calculated index scores so far?
    # should I do the same with pagerank?
    while page_queue and current_page_searches < max_page_searches:
        search_url = page_queue.popleft()

        if handle_existing_page(redis_client, search_url, page_queue):
            continue

        print(f"Searching {search_url}, {current_page_searches} of {max_page_searches}")
        current_page_searches += 1

        handle_new_page(redis_client, search_url, page_queue, fetcher)

    index_list = get_sorted_index_list_for_word(redis_client, search_term)

    for url, score in index_list:
        print(f"{url}: {score}")


def handle_existing_page(redis_client, search_url, page_queue):
    """
    Parameters:
    - redis_client: Redis client object used to interact with Redis.
    - search_url: The search url entered by the user.
    """
    links = linked_pages(redis_client, search_url)

    if links:
        for link in links:
            page_queue.append(str(link, "utf-8"))
        return True

    return False


def handle_new_page(redis_client, search_url, page_queue, fetcher):
    """
    Parameters:
    - redis_client: Redis client object used to interact with Redis.
    - search_url: The search url entered by the user.
    """
    page = fetcher.fetch_wikipedia(search_url)

    redis_index_pipeline(iterate_words(page), search_url, redis_client)

    links = []
    for page_url in link_generator(page):
        new_url = str("https://en.wikipedia.org" + page_url.get("href"))
        page_queue.append(new_url)
        links.append(new_url)

    store_page_links(redis_client, search_url, links)
