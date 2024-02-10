from bs4 import Tag

def link_generator(root):
    for element in root.descendants:
        if isinstance(element, Tag) and element.name == 'a':
            title = element.get('title', '')
            href = element.get('href', '')
            if title and href.startswith('/wiki'):
                yield element