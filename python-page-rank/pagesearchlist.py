"""
Module name: pagesearchlist
"""

## To-do: also sort by the URL if the scores are the same, based on similarity to the search term


# the problem with the way that this is implemented
# is that it may only search a single group of pages from a single source.
# not sure how to fix that.

# it seems like it would be more effective to implement this as a heap rather than a linked list
class PageSearchList:
    """
    really just a wrapper around LinkedListSorted, with a more explicit api
    """

    def __init__(self, search_term, max_pages=100):
        self.list = LinkedListSorted()
        self.max_pages = max_pages
        self.current_page_searches = 0
        self.search_term = search_term

    def add_page(self, page_url, parent_score):
        """
        Adds the given page to the list in sorted order.

        Parameters:
        - page_url: The URL of the page to add to the list.
        - score: The score of the parent of the page to add to the list
        """
        self.list.add_sorted(PageDatum(page_url, parent_score))

    def get_page_with_highest_score(self):
        """
        Removes and returns the page with the highest score from the list.

        Returns:
        - A tuple containing the URL and score of the page with the highest score.
        """
        if self.current_page_searches >= self.max_pages:
            return None

        self.current_page_searches += 1
        return self.list.pop()

    def __str__(self):
        return (
            f"Page search list for {self.search_term} "
            f"with {self.current_page_searches} of {self.max_pages} pages searched. "
            f"Next page to search: {self.list.peek()}"
        )


class LinkedListSorted:
    """
    The linked list is good in this case because we
    only pull from one end, but insert in any position.
    """

    def __init__(self):
        self.head = None

    def add_sorted(self, datum):
        """
        Adds the given datum to the list in sorted order.

        Parameters:
        - datum: The datum to add to the list.
        """

        new_node = LLNode(datum)

        if self.head is None:
            self.head = new_node
            return

        search_node = self.head
        prev_node = None

        while search_node is not None and search_node.data.score >= datum.score:
            prev_node = search_node
            search_node = search_node.next

        if prev_node is None:
            new_node.next = self.head
            self.head = new_node
        else:
            prev_node.next = new_node
            new_node.next = search_node

    def pop(self):
        """
        Removes and returns the page with the highest score from the list.

        Returns:
        - A tuple containing the URL and score of the page with the highest score.
        """
        if self.head is None:
            return None

        current = self.head
        self.head = self.head.next
        return current.data

    def peek(self):
        """
        Returns the page with the highest score from the list without removing it.

        Returns:
        - A tuple containing the URL and score of the page with the highest score.
        """
        return self.head.data

    def __len__(self):
        length = 0
        current = self.head
        while current is not None:
            length += 1
            current = current.next
        return length


class LLNode:
    """
    The linked list is good in this case because we
    only pull from one end, but insert in any position.
    """

    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return f"{self.data}"


class PageDatum:
    """
    The linked list is good in this case because we
    only pull from one end, but insert in any position.
    """

    def __init__(self, page_url, score):
        if not isinstance(page_url, str):
            page_url = str(page_url, "utf-8")

        self.page_url = page_url
        self.score = score

    def __str__(self):
        return f"{self.page_url}: {self.score}"
