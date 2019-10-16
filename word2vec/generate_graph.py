import sys
import time
import json
import numpy as np
from annoy import AnnoyIndex

def debug_time(msg, init, now):
    print("{} [{}ms]".format(msg, int(round((now-init)*1000*1000))/1000.0), file=sys.stderr)

# Configuration Parameters
VSM_DIMS = 300
CACHE_PATH = "C:/_YaoYiheng/_Projects/NLP_AssocMap/graph_processing/cache/"
GRAPH_PATH = "C:/_YaoYiheng/_Projects/NLP_AssocMap/graph_processing/graph/"
ANN_TREE = "GoogleNews_index_nelson.ann"
DIC_FILE = "GoogleNews_wordlist_nelson.txt"
WORD_FILE = "../test_sets/nelson_words.txt"

# Load query word file
word_list = []
with open(WORD_FILE, 'r') as fin:
	for line in fin:
		word = line.lower().strip().replace('_', ' ')
		word_list.append(word)
print(f"Loaded words from {WORD_FILE}", file=sys.stderr)

# Load word to index dictionary
word_dic = dict()
rev_word_dic = dict()
with open(f"{CACHE_PATH}{DIC_FILE}", 'r', encoding='utf8') as fin:
	for line in fin:
		idx, word = line.lower().strip().split('\t')
		idx = int(idx)
		word = word[2:-1]
		word = word.replace('_', ' ')
		word_dic[word] = idx
		rev_word_dic[idx] = word
print(f"Loaded word dictionary from {DIC_FILE}", file=sys.stderr)

# Load up our index tree
load_t = time.time()
model = AnnoyIndex(VSM_DIMS)
model.load(f"{CACHE_PATH}{ANN_TREE}")
debug_time(f"Annoying Tree Loaded from {ANN_TREE}", load_t, time.time())

###############################
# WRITE GRAPH TO FILE FORMATS #
###############################
# Write to .json
def write_json(graph, fname):
    json_graph = dict()
    json_graph['nodes'] = {'name': n for n in graph['nodes']}
    # 'source': 0, 'target': 0, 'value': 0
    json_graph['links'] = [{'source': graph['edges'][k][0], 'target': graph['edges'][k][1], 'value': graph['edges'][k][2]} for k in range(len(graph['edges']))]
    with open(fname + ".json", "w+") as fout:
        json.dump(json_graph, fout)

# Write to .gexf
def write_gexf(graph, fname):
    print("Generating .gexf file for graph with {} Nodes | {} Edges".format(len(graph['nodes']), len(graph['edges'])))
    # Write Actual file in proper format
    gexf_header = """<?xml version="1.0" encoding="UTF-8"?>
    <gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
        <meta lastmodifieddate="2009-03-20">
            <creator>devYaoYH</creator>
            <description>Linguistic Association Network Graph</description>
        </meta>
        <graph mode="static" defaultedgetype="undirected">
            <nodes>"""
    gexf_footer = """            </edges>
        </graph>
    </gexf>"""
    with open(fname + ".gexf", "w+") as fout:
        fout.write(gexf_header)
        # Extract All Nodes Information
        for i, node in enumerate(graph['nodes']):
            fout.write("                <node id=\"{}\" label=\"{}\" />\n".format(i, node))
        fout.write("            </nodes>\n            <edges>\n")
        # Extract All Edges Information
        for i, tup in enumerate(graph['edges']):
            source, target, value = tup
            fout.write("                <edge id=\"{}\" source=\"{}\" target=\"{}\" />\n".format(i, source, target))
        fout.write(gexf_footer)

# Raw unit edge format
def write_raw(graph, fname):
	with open(fname + ".graph", "w+") as fout:
		for source, target, value in graph['edges']:
			fout.write(f"{rev_word_dic[source]},{rev_word_dic[target]}\n")

def debug_json(graph, fname):
    with open(fname.split('.')[0]+"_log.json", "w+") as fout:
        json.dump(graph, fout);

# Write all formats
def write_all(graph, fname):
	write_json(graph, fname)
	write_gexf(graph, fname)
	write_raw(graph, fname)
	debug_json(graph, fname)

#######################
# CONFIGURATION FUNCS #
#######################
def cosine_filter(source, min_edges=1, cutoff=0.1, k=10):
	li = sorted([(abs(1-model.get_distance(source, t)), t) for t in model.get_nns_by_item(source, k)], key=lambda x: x[0])
	ret_nodes = [(t, v) for v, t in li[:min_edges]]
	for value, target in li[min_edges:]:
		if (value > cutoff):
			return ret_nodes
		ret_nodes.append((target, value))
	return ret_nodes

##################
# GENERATE GRAPH #
##################
# Generates graph given file format and node-node connection function
def generate_graph(save_format=None, fname=None, edge_filter=None):
	# Default Behavior
	if (save_format is None):
		save_format = write_json
	if (fname is None):
		fname = f"{GRAPH_PATH}graph_{(int(time.time()*1000000)//1000)}"
	if (edge_filter is None):
		edge_filter = cosine_filter

	# Construct Graph object
	graph = dict()
	graph['nodes'] = []
	for w in word_list:
		if (w not in word_dic):
			print(f"Error, unable to find: {w}")
		else:
			graph['nodes'].append(w)
	graph['edges'] = []
	# Connect nodes
	for w in graph['nodes']:
		source = word_dic[w]
		for target, value in edge_filter(source):
			graph['edges'].append((source, target, value))
	# Save graph
	save_format(graph, fname)

generate_graph(save_format=write_all)