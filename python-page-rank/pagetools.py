from bs4 import Tag, NavigableString, BeautifulSoup
from string import punctuation, whitespace
from collections import Counter
from redis import Redis

def link_generator(root):
    for element in root.descendants:
        if isinstance(element, Tag) and element.name == 'a':
            title = element.get('title', '')
            href = element.get('href', '')
            if title and href.startswith('/wiki'):
                yield element

def iterate_words(root):
    for element in root.descendants:
        if isinstance(element, NavigableString):
            for word in element.string.split():
                word = word.strip(whitespace + punctuation)
                if word:
                    yield word.lower()


def redis_index_pipeline(root, url, r: Redis):
    counter = Counter(iterate_words(root))
    p = r.pipeline(transaction=False)
    for word, count in counter.items():
        if count >= 3:
            key = f'Index:{word}'
            p.hset(key, url, count)
    p.execute()