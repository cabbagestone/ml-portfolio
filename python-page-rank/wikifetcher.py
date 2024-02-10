from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import time, sleep
    
class WikiFetcher:
    next_request_time = None
    min_interval = 1  # second

    def fetch_wikipedia(self, url):
        self.sleep_if_needed()
        fp = urlopen(url)
        soup = BeautifulSoup(fp, 'html.parser')
        return soup

    def sleep_if_needed(self):
        if self.next_request_time:
            sleep_time = self.next_request_time - time()    
            if sleep_time > 0:
                sleep(sleep_time)
        
        self.next_request_time = time() + self.min_interval