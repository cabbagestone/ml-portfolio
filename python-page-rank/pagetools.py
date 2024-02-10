from bs4 import Tag, NavigableString
from string import punctuation, whitespace

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