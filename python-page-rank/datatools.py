from collections import deque
from pagerank import pagerank_numpy
import networkx as nx

def reachable_nodes_bfs(G, start):
    seen = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node not in seen:
            seen.add(node)
            neighbors = set(G[node]) - seen
            queue.extend(neighbors)
    return seen

def calculate_page_rank(link_graph):
    G = nx.from_dict_of_lists(link_graph) 
    return pagerank_numpy(G)

def calculate_hybrid_score(page_url, page_rank, redis_client):
    index_score = calculate_index_score(page_url, redis_client) 
    
    normalized_page_rank = page_rank / max(page_rank.values()) 
    normalized_index_score = index_score / ...

    hybrid_score = 0.7 * normalized_page_rank + 0.3 * normalized_index_score  
    return hybrid_score

def calculate_index_score(page_url, redis_client):
    return 0.5