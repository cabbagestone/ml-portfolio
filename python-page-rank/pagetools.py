"""
Module Name: pagetools
"""

from string import punctuation, whitespace

from bs4 import NavigableString, Tag


def link_generator(root):
    """
    Function that generates links from the given root BeautifulSoup object.

    Parameters:
    - root: The root BeautifulSoup object to generate links from.

    Yields:
    - The next link in the root BeautifulSoup object.
    """

    for element in root.descendants:
        if isinstance(element, Tag) and element.name == "a":
            title = element.get("title", "")
            href = element.get("href", "")
            if (
                title
                and href.startswith("/wiki")
                and not href.startswith(
                    (
                        "/wiki/Wikipedia",
                        "/wiki/Help",
                        "/wiki/File",
                        "/wiki/Special",
                        "/wiki/Template",
                        "/wiki/Talk",
                    )
                )
            ):
                yield element


def iterate_words(root):
    """
    Function that iterates over the words in the given root BeautifulSoup object.

    Parameters:
    - root: The root BeautifulSoup object to iterate over.

    Yields:
    - The next word in the root BeautifulSoup object.
    """

    for element in root.descendants:
        if isinstance(element, NavigableString):
            for word in element.string.split():
                word = word.strip(whitespace + punctuation)
                if word:
                    yield word.lower()
