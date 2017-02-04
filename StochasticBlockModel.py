#!/usr/bin/env python
#coding:utf-8
"""
  Purpose:  Stochastic block model
  Created:  01/02/2017
"""
from time import clock
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sys

#----------------------------------------------------------------------
def degreesExpectations(probability_matrix, n_per_community):
    """Calculate expected degrees of vertices in each community (C1, ..., Ck)"""
    return np.dot(probability_matrix[:len(n_per_community),:len(n_per_community)], n_per_community) # return [E(d1), E(d2), ..., E(dk)]

#----------------------------------------------------------------------
def diagDegreeMatrix(adjacency_matrix, lower_triangular=False):
    """Return D diagonal matrix where D[i,i] is degree of each node i"""
    return np.diag(np.sum(adjacency_matrix + adjacency_matrix.T if lower_triangular else adjacency_matrix, axis=0))

#----------------------------------------------------------------------
def averageDegree(adjacency_matrix, lower_triangular=False):
    """Return average degree of a graph represented by his adjacency matrix"""
    return np.mean(np.sum(adjacency_matrix + adjacency_matrix.T if lower_triangular else adjacency_matrix, axis=0))

#----------------------------------------------------------------------
# Stochastic block model parameters
n_vertices = 6  # number of vertices
n_communities = 2  # number of communities
community_labels = np.random.randint(low=0, high=n_communities, size=n_vertices) # community label assigned to each vertex
n_per_community = [len(np.argwhere(community_labels == i)) for i in xrange(n_communities)] # number of vertices per community (n1, n2, ..., nk)
probability_matrix = np.array([
    [0.1, .1, .1, .01],
    [.1, 0.9, .9, .01],
    [.1, .9, 0.5, .011],
    [.01, .01, .01, 0.1],
]) # matrix of edge probabilities
if(not (probability_matrix.T == probability_matrix).all()):
    print("Probability matrix isn't symmetric!")

#----------------------------------------------------------------------
# Adjacency matrix generation (strictly lower triangular as graph is undirected)
t0 = clock()
graph_matrix = np.zeros((n_vertices, n_vertices), dtype=bool) # adjacency matrix initialization
for i in xrange(n_vertices):
    for j in xrange(i):
        val = probability_matrix[community_labels[i],community_labels[j]]
        p = np.random.rand()
        if p <= val:
            graph_matrix[i][j] = 1

print("Time taken to generate the graph: " + str((clock() - t0)*1000) + "ms")
print("Size: " + str(sys.getsizeof(graph_matrix)/1024) + "ko\n")

#----------------------------------------------------------------------
# Draw generated graph and print communities
color_map = np.array(['cyan', 'red', 'yellow', 'magenta', 'blue', 'green', 'white'][:n_communities])
degrees_expectations = degreesExpectations(probability_matrix, n_per_community)
for i in xrange(n_communities):
    indices = [j+1 for j, x in enumerate(community_labels) if x == i]
    print("Community C{}, color: {}, E[di] = {}".format(str(i), color_map[i], degrees_expectations[i]))

if n_vertices > 100: sys.exit(0) # Can't draw if number of vertices is too big
node_color = color_map[community_labels]
labels = {key: key+1 for key in xrange(n_vertices)} # vertices numbers
G = nx.from_numpy_matrix(graph_matrix) # generate networkx graph
nx.draw(G, labels=labels, node_color=node_color, font_size=12)

plt.show()
