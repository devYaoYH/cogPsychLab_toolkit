import sys
import time
import math
import utils
from fa2 import ForceAtlas2
import matplotlib.pyplot as plt
import networkx as nx

def plot_graph(fname, iters=500, lbl=False, show=True):
	nx_graph = nx.Graph()
	graph = utils.load_graph(fname, weighted=True)
	for prime in graph.keys():
		for target, weight in graph[prime]:
			nx_graph.add_edge(prime, target, weight=weight)
	forceatlas2 = ForceAtlas2(
		# Behavior alternatives
		outboundAttractionDistribution=True,  # Dissuade hubs
		linLogMode=False,  # NOT IMPLEMENTED
		adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
		edgeWeightInfluence=0.1,

		# Performance
		jitterTolerance=1.0,  # Tolerance
		barnesHutOptimize=True,
		barnesHutTheta=1.2,
		multiThreaded=False,  # NOT IMPLEMENTED

		# Tuning
		scalingRatio=2.0,
		strongGravityMode=False,
		gravity=1.0,

		# Log
		verbose=True)
	positions = forceatlas2.forceatlas2_networkx_layout(nx_graph, pos=None, iterations=iters)
	if (lbl):
		nx.draw_networkx_labels(nx_graph, positions, labels=dict([(n, n) for n in nx_graph.nodes()]))
	nx.draw_networkx_nodes(nx_graph, positions, node_size=5, with_labels=False, node_color="blue", alpha=0.4)
	nx.draw_networkx_edges(nx_graph, positions, edge_color="green", alpha=0.05)
	plt.axis('off')
	plt.savefig(f"{fname.split('.')[-2]}_graph.png")
	if (show):
		plt.show()
	plt.clf()

def plot_graph_unweighted(fname, iters=500, lbl=False, show=True):
	nx_graph = nx.Graph()
	graph = utils.load_graph(fname)
	for prime in graph.keys():
		for target in graph[prime]:
			nx_graph.add_edge(prime, target)
	forceatlas2 = ForceAtlas2(
		# Behavior alternatives
		outboundAttractionDistribution=True,  # Dissuade hubs
		linLogMode=False,  # NOT IMPLEMENTED
		adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
		edgeWeightInfluence=0,

		# Performance
		jitterTolerance=1.0,  # Tolerance
		barnesHutOptimize=True,
		barnesHutTheta=1.2,
		multiThreaded=False,  # NOT IMPLEMENTED

		# Tuning
		scalingRatio=2.0,
		strongGravityMode=False,
		gravity=1.0,

		# Log
		verbose=True)
	positions = forceatlas2.forceatlas2_networkx_layout(nx_graph, pos=None, iterations=iters)
	if (lbl):
		nx.draw_networkx_labels(nx_graph, positions, labels=dict([(n, n) for n in nx_graph.nodes()]))
	nx.draw_networkx_nodes(nx_graph, positions, node_size=5, with_labels=False, node_color="blue", alpha=0.4)
	nx.draw_networkx_edges(nx_graph, positions, edge_color="green", alpha=0.05)
	plt.axis('off')
	plt.savefig(f"{fname.split('.')[-2]}_graph.png")
	if (show):
		plt.show()
	plt.clf()

if (__name__ == '__main__'):
	utils.plot_scatter()
	# for x in range(35, 95, 5):
	# 	plot_graph(f"graph/nelson_1_{x}.graph", iters=100, show=False)
	# for x in range(25, 35):
	# 	plot_graph(f"graph/nelson_1_{x}.graph", iters=100, show=False)
	# for fname in ["pathlengths_undirected_kennetetal", "pathlengths_undirected_step_distance", "pathlengths_undirected_step_distance_pmfg"]:
	# 	plot_graph_unweighted(f"graph/{fname}.graph", iters=100, show=False)