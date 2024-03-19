"""
Module Name: search
"""

from pagetools import iterate_words, link_generator
from redistools import (
    get_sorted_index_list_for_word,
    linked_pages,
    redis_index_pipeline,
    store_page_links,
    get_index_for_page_for_search_term,
    get_highest_index_for_search_term,
)
from wikifetcher import WikiFetcher
from pagesearchlist import PageSearchList
from wordtools import url_relevance


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

    page_list = PageSearchList(search_term)
    page_list.add_page(search_url, 1)

    # do in-progress adjustment for which pages to search next
    # based on the calculated index scores so far?
    # should I do the same with pagerank?

    while page_datum := page_list.get_page_with_highest_score():
        search_url = page_datum.page_url

        if handle_existing_page(redis_client, search_url, page_list):
            continue

        print(str(page_list))

        handle_new_page(redis_client, search_url, page_list, fetcher)

    index_list = get_sorted_index_list_for_word(redis_client, search_term)

    # for url, score in index_list:
    #     print(f"{url}: {score}")


def handle_existing_page(redis_client, search_url, page_list: PageSearchList):
    """
    Parameters:
    - redis_client: Redis client object used to interact with Redis.
    - search_url: The search url entered by the user.
    """
    links = linked_pages(redis_client, search_url)

    index = get_index_for_page_for_search_term(
        redis_client,
        page_list.search_term,
        search_url,
    )

    if links:
        for link in links:
            total_score = calculate_page_score_for_searching(
                url_relevance(link, page_list.search_term), index
            )
            page_list.add_page(link, total_score)
        return True

    return False


def handle_new_page(redis_client, search_url, page_list: PageSearchList, fetcher):
    """
    Parameters:
    - redis_client: Redis client object used to interact with Redis.
    - search_url: The search url entered by the user.
    """
    page = fetcher.fetch_wikipedia(search_url)

    iterator = iterate_words(page)
    redis_index_pipeline(iterator, search_url, redis_client)

    index = get_index_for_page_for_search_term(
        redis_client,
        page_list.search_term,
        search_url,
    )

    index_score = index / get_highest_index_for_search_term(
        redis_client, page_list.search_term
    )

    links = []
    for page_url in link_generator(page):
        href = page_url.get("href")
        new_url = str("https://en.wikipedia.org" + href)
        word_score = url_relevance(href, page_list.search_term)
        total_score = calculate_page_score_for_searching(word_score, index_score)

        page_list.add_page(new_url, total_score)
        links.append(new_url)

    store_page_links(redis_client, search_url, links)


def calculate_page_score_for_searching(word_score, index_score):
    """
    Function that calculates the page score for searching based on the word and index scores.

    Parameters:
    - word_score: The word score for the page.
    - index_score: The index score for the page.

    Returns:
    - The page score for searching based on the word and index scores.
    """

    return word_score * 0.5 + index_score * 0.5
