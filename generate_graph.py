from __future__ import print_function
import sys
import time
import json
import numpy as np
import utils
from annoy import AnnoyIndex

def debug_time(msg, init, now):
    print("{} [{}ms]".format(msg, int(round((now-init)*1000*1000))/1000.0), file=sys.stderr)

####################
# CMD LINE PARSING #
####################
argc = len(sys.argv)
argv = sys.argv

# List of cmdline flag variables
FLAGS = set([])

# Number of required arguments
REQUIRED_ARGS = ["output_name"]
OPTIONAL_ARGS = {
    "CACHE": "cache_path",
    "GRAPH": "path_to_save_graphs",
    "ANN": "index_tree_path",
    "DIC": "word_to_index_dictionary_for_tree",
    "WORD": "word_list"
}

############################################
# PARSING CMD LINE STUFF - no need to edit #
############################################
NUM_REQUIRED_ARGS = len(REQUIRED_ARGS) + 1
# --> [executable name, word list file name]
args = []

# Flags/Optional Arguments
flags = set()
optional_args = {key: None for key in OPTIONAL_ARGS.keys()}
undefined_args = []

def print_usage():
    print("Usage: python " + args[0], end='')
    for arg in REQUIRED_ARGS:
        print(" <{}>".format(arg), end='')
    if (len(OPTIONAL_ARGS) > 0):
        for k, v in OPTIONAL_ARGS.items():
            print(" -{} <{}>".format(k, v), end='')
    if (len(FLAGS) > 0):
        print(' [', end='')
        for f in FLAGS:
            print(" -{}".format(f), end='')
        print(' ]', end='')
    print('')

# We scan through command line arguments and place them into the correct types
arg_i = 0
while (arg_i < argc):
    if ('-' == argv[arg_i][0]):
        flag = argv[arg_i][1:]
        if (flag in FLAGS):
            # Argument format: -flag
            flags.add(flag)
        elif (flag in optional_args):
            # Argument format: -flag <string>
            optional_args[argv[arg_i][1:]] = argv[arg_i+1]
            arg_i += 1
        else:
            undefined_args.append(argv[arg_i])
    else:
        args.append(argv[arg_i])
    arg_i += 1

if (len(args) < NUM_REQUIRED_ARGS):
    print_usage()
    exit()
#############################################################################
# END OF PARSING - arguments in: args, optional_args, undefined_args, flags #
#############################################################################

# Configuration Parameters
VSM_DIMS = 300
CACHE_PATH = "C:/_YaoYiheng/_Projects/NLP_AssocMap/graph_processing/cache/" if optional_args["CACHE"] is None else optional_args["CACHE"]
GRAPH_PATH = "C:/_YaoYiheng/_Projects/NLP_AssocMap/graph_processing/graph/" if optional_args["GRAPH"] is None else optional_args["GRAPH"]
ANN_TREE = "GoogleNews_index_nelson.ann" if optional_args["ANN"] is None else optional_args["ANN"]
DIC_FILE = "GoogleNews_wordlist_nelson.txt" if optional_args["DIC"] is None else optional_args["DIC"]
WORD_FILE = "test_sets/nelson_words.txt" if optional_args["WORD"] is None else optional_args["WORD"]

# Load query word file
word_list = []
with open(WORD_FILE, 'r') as fin:
    for line in fin:
        word = line.lower().strip().replace('_', ' ')
        word_list.append(word)
print(f"Loaded words from {WORD_FILE}", file=sys.stderr)

# Load word to index dictionary
word_dic = dict()
with open(f"{CACHE_PATH}{DIC_FILE}", 'r', encoding='utf8') as fin:
    for line in fin:
        idx, word = line.lower().strip().split('\t')
        idx = int(idx)
        word = word[2:-1]
        word = word.replace('_', ' ')
        word_dic[word] = idx
print(f"Loaded word dictionary from {DIC_FILE}", file=sys.stderr)

# Load up our index tree
load_t = time.time()
model = AnnoyIndex(VSM_DIMS)
model.load(f"{CACHE_PATH}{ANN_TREE}")
debug_time(f"Annoying Tree Loaded from {ANN_TREE}", load_t, time.time())

###############################
# WRITE GRAPH TO FILE FORMATS #
###############################
# Write all formats
def write_all(graph, fname):
    utils.write_json(graph, fname)
    utils.write_gexf(graph, fname)
    utils.write_raw(graph, fname)
    utils.debug_json(graph, fname)

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
    else:
        fname = f"{GRAPH_PATH}{fname}"
    if (edge_filter is None):
        edge_filter = cosine_filter

    # Construct Graph object
    graph = dict()
    #NOTE: This assumes we have constructed our ann cache with continuous running index
    graph['nodes'] = sorted([w for w in word_dic.keys()], key=lambda x: word_dic[x])
    for w in word_list:
        if (w not in word_dic):
            print(f"Error, unable to find: {w}")
    graph['edges'] = []
    # Connect nodes
    for w in graph['nodes']:
        source = word_dic[w]
        for target, value in edge_filter(source):
            graph['edges'].append((source, target, value))
    # Save graph
    save_format(graph, fname)

generate_graph(save_format=write_all, fname=args[1])