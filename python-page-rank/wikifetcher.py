"""
Module name: wikifetcher
"""

from time import sleep, time
from urllib.request import urlopen

from bs4 import BeautifulSoup


class WikiFetcher:
    """
    A class used to fetch Wikipedia pages.

    Attributes
    ----------
    next_request_time : float
        The time when the next request can be made.
    min_interval : int
        The minimum interval between requests in seconds.

    Methods
    -------
    fetch_wikipedia(url)
        Fetches the Wikipedia page at the given URL and returns a BeautifulSoup object.
    sleep_if_needed()
        Sleeps for the necessary amount of time to respect the minimum interval between requests.
    """

    next_request_time = None
    min_interval = 1  # second

    def fetch_wikipedia(self, url):
        """
        Fetches the Wikipedia page at the given URL and returns a BeautifulSoup object.

        Parameters
        ----------
        url : str
            The URL of the Wikipedia page to fetch.

        Returns
        -------
        BeautifulSoup
            A BeautifulSoup object representing the fetched Wikipedia page.
        """
        self.sleep_if_needed()

        with urlopen(url) as fp:
            soup = BeautifulSoup(fp, "html.parser")
            return soup

    def sleep_if_needed(self):
        """
        Sleeps for the necessary amount of time to respect the minimum interval between requests.
        """
        if self.next_request_time:
            sleep_time = self.next_request_time - time()
            if sleep_time > 0:
                sleep(sleep_time)

        self.next_request_time = time() + self.min_interval
