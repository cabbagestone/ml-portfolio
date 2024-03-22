"""
Module name: pagesearchlist
"""

import heapq


## To-do: also sort by the URL if the scores are the same, based on similarity to the search term

# the problem with the way that this is implemented
# is that it may only search a single group of pages from a single source.
# not sure how to fix that.


class PageSearchList:
    """
    a max heap priority queue that keeps track of the number of pages
    """

    def __init__(self, search_term, max_pages=100):
        self.heap = []
        self.max_pages = max_pages
        self.current_page_searches = 0
        self.search_term = search_term

    def add_page(self, page_url, parent_score):
        """
        Adds the given page to the list in sorted order.
        """
        heapq.heappush(self.heap, PageDatum(page_url, -parent_score))

    def get_page_with_highest_score(self):
        """
        Removes and returns the page with the highest score from the list.
        """
        if self.current_page_searches >= self.max_pages:
            return None

        self.current_page_searches += 1
        return heapq.heappop(self.heap)

    def __str__(self):
        if not self.heap:
            return f"No pages to search for {self.search_term}."

        return (
            f"Page search list for {self.search_term} "
            f"with {self.current_page_searches} of {self.max_pages} pages searched. "
            f"Next page to search: {self.heap[0]}"
        )


class PageDatum:
    """
    A class to hold the URL and score of a page.
    """

    def __init__(self, page_url, score):
        if not isinstance(page_url, str):
            page_url = str(page_url, "utf-8")

        self.page_url = page_url
        self.score = score

    def __str__(self):
        return f"{self.page_url}: {self.score}"

    def __lt__(self, other: "PageDatum"):
        return self.score < other.score

    def __eq__(self, other: "PageDatum"):
        return self.score == other.score

    def __gt__(self, other: "PageDatum"):
        return self.score > other.score
