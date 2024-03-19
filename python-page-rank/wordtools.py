from difflib import SequenceMatcher


def url_relevance(url, search_term):
    url, search_term = url.lower(), search_term.lower()

    if search_term in url:
        return 1.0

    match_size = (
        SequenceMatcher(None, url, search_term)
        .find_longest_match(0, len(url), 0, len(search_term))
        .size
    )
    score = match_size / len(search_term)

    return score
