"""
Module name: pagerank
"""

import numpy as np
import networkx as nx

# copied nearly verbatim from https://allendowney.github.io/DSIRP/pagerank.html


def google_matrix(graph_to_convert, alpha=0.85):
    """Returns the Google matrix of the graph.

    Parameters
    ----------
    G : graph
      A NetworkX graph.  Undirected graphs will be converted to a directed
      graph with two directed edges for each undirected edge.

    alpha : float
      The damping factor.

    Notes
    -----
    The matrix returned represents the transition matrix that describes the
    Markov chain used in PageRank. For PageRank to converge to a unique
    solution (i.e., a unique stationary distribution in a Markov chain), the
    transition matrix must be irreducible. In other words, it must be that
    there exists a path between every pair of nodes in the graph, or else there
    is the potential of "rank sinks."
    """
    graph_as_matrix = np.asmatrix(nx.to_numpy_array(graph_to_convert))
    matrix_length = len(graph_to_convert)
    if matrix_length == 0:
        return graph_as_matrix

    # Personalization vector
    personalization_vector = np.repeat(1.0 / matrix_length, matrix_length)

    # Dangling nodes
    dangling_weights = personalization_vector
    dangling_nodes = np.where(graph_as_matrix.sum(axis=1) == 0)[0]

    # Assign dangling_weights to any dangling nodes
    # (nodes with no out links)
    for node in dangling_nodes:
        graph_as_matrix[node] = dangling_weights

    graph_as_matrix /= graph_as_matrix.sum(axis=1)  # Normalize rows to sum to 1

    return alpha * graph_as_matrix + (1 - alpha) * personalization_vector


def pagerank_numpy(graph_to_calculate, alpha=0.85):
    """Returns the PageRank of the nodes in the graph.

    PageRank computes a ranking of the nodes in the graph G based on
    the structure of the incoming links. It was originally designed as
    an algorithm to rank web pages.

    Parameters
    ----------
    G : graph
      A NetworkX graph.  Undirected graphs will be converted to a directed
      graph with two directed edges for each undirected edge.

    alpha : float, optional
      Damping parameter for PageRank, default=0.85.

    Returns
    -------
    pagerank : dictionary
       Dictionary of nodes with PageRank as value.

    Examples
    --------
    >>> G = nx.DiGraph(nx.path_graph(4))
    >>> pr = nx.pagerank_numpy(G, alpha=0.9)

    Notes
    -----
    The eigenvector calculation uses NumPy's interface to the LAPACK
    eigenvalue solvers.  This will be the fastest and most accurate
    for small graphs.

    References
    ----------
    .. [1] A. Langville and C. Meyer,
       "A survey of eigenvector methods of web information retrieval."
       http://citeseer.ist.psu.edu/713792.html
    .. [2] Page, Lawrence; Brin, Sergey; Motwani, Rajeev and Winograd, Terry,
       The PageRank citation ranking: Bringing order to the Web. 1999
       http://dbpubs.stanford.edu:8090/pub/showDoc.Fulltext?lang=en&doc=1999-66&format=pdf
    """
    if len(graph_to_calculate) == 0:
        return {}
    google_matrix_from_graph = google_matrix(graph_to_calculate, alpha)

    # use numpy LAPACK solver
    eigenvalues, eigenvectors = np.linalg.eig(google_matrix_from_graph.T)
    indices = np.argmax(eigenvalues)

    # eigenvector of largest eigenvalue is at ind, normalized
    largest = np.array(eigenvectors[:, indices]).flatten().real
    norm = float(largest.sum())
    return dict(zip(graph_to_calculate, map(float, largest / norm)))
