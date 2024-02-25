"""
Module name: scratch

used for testing and debugging
"""

from redistools import connect_to_redis, get_sorted_index_list_for_word


def main():
    """
    Main
    """

    client = connect_to_redis()

    print(str(get_sorted_index_list_for_word(client, "python")))


if __name__ == "__main__":
    main()


# from collections import deque
#
# import networkx as nx
#
# from pagerank import pagerank_numpy
# def reachable_nodes_bfs(graph, start):
#     """
#     Performs a breadth-first search (BFS) on the graph starting from the 'start' node.
#     Returns a set of all nodes reachable from the 'start' node.

#     Parameters:
#     graph (dict): The graph represented as an adjacency list.
#     start (str): The starting node for the BFS.

#     Returns:
#     set: A set of all nodes reachable from the 'start' node.
#     """
#     seen = set()
#     queue = deque([start])
#     while queue:
#         node = queue.popleft()
#         if node not in seen:
#             seen.add(node)
#             neighbors = set(graph[node]) - seen
#             queue.extend(neighbors)
#     return seen


# def calculate_page_rank(link_graph):
#     """
#     Calculates the PageRank for each node in the link graph.

#     Parameters:
#     link_graph (dict): The link graph represented as an adjacency list.

#     Returns:
#     dict: A dictionary where the keys are nodes and the values are their corresponding PageRank.
#     """
#     graph = nx.from_dict_of_lists(link_graph)
#     return pagerank_numpy(graph)


# def calculate_hybrid_score(page_url, page_rank, redis_client):
#     """
#     Calculates a hybrid score for a page based on its PageRank and index score.

#     Parameters:
#     page_url (str): The URL of the page.
#     page_rank (dict): A dictionary where the keys are page URLs and the values are their corresponding PageRank.
#     redis_client (Redis): The Redis client.

#     Returns:
#     float: The hybrid score for the page.
#     """
#     index_score = calculate_index_score(page_url, redis_client)

#     normalized_page_rank = page_rank / max(page_rank.values())
#     normalized_index_score = index_score

#     hybrid_score = 0.7 * normalized_page_rank + 0.3 * normalized_index_score
#     return hybrid_score


# def calculate_index_score(page_url, redis_client):
#     """
#     Calculates the index score for a page. Currently, this function returns a constant value.

#     Parameters:
#     page_url (str): The URL of the page.
#     redis_client (Redis): The Redis client.

#     Returns:
#     float: The index score for the page.
#     """
#     return 0.5
