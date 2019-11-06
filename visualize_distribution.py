from annoy import AnnoyIndex
import matplotlib.pyplot as plt
import numpy as np
import random
import json
import time
import sys

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
REQUIRED_ARGS = []
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
CACHE_PATH = "cache/" if optional_args["CACHE"] is None else optional_args["CACHE"]
GRAPH_PATH = "graph/" if optional_args["GRAPH"] is None else optional_args["GRAPH"]
ANN_TREE = "GoogleNews_index_nelson.ann" if optional_args["ANN"] is None else optional_args["ANN"]
DIC_FILE = "GoogleNews_wordlist_nelson.txt" if optional_args["DIC"] is None else optional_args["DIC"]
WORD_FILE = "test_sets/nelson_words.txt" if optional_args["WORD"] is None else optional_args["WORD"]

#########################
# Extract data from ann #
#########################

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

def read_wordpairs(fname):
	word_pairs = []
	word_t = time.time()
	with open(fname, 'r') as fin:
	    for line in fin:
	        line_data = line.strip().split(',')
	        prime = line_data[0].lower()
	        target = line_data[1].lower()
	        word_pairs.append((prime, target))
	debug_time("Loading word list...", word_t, time.time())
	return word_pairs

def get_nelson_dist():
	data = []
	print("Computing O(N^2) for {} nodes".format(len(word_list)))
	for i in range(len(word_list)):
		for j in range(i, len(word_list)):
			w1 = word_list[i]
			w2 = word_list[j]
			if (w1 != w2 and w1 in word_dic and w2 in word_dic):
				# Add cosine to data
				data.append(abs(1-model.get_distance(word_dic[w1], word_dic[w2])))
	return data

def get_nelson_rand_dist(t=0.4):
	data = []
	w = None
	while (w not in word_dic):
		w = random.choice(word_list)
	print("Computing O(N) for {} nodes | From: {}".format(len(word_list), w))
	for ow in word_list:
		if (ow != w and ow in word_dic):
			dist = abs(1-model.get_distance(word_dic[ow], word_dic[w]))
			data.append(dist)
			if (dist < t):
				print(ow)
	return data

def get_demasking_dist():
	data = []
	word_pairs = read_wordpairs(input("Word pairs: "))
	print("Computing O(N) for {} word pairs".format(len(word_pairs)))
	dup_filter = set()
	for w1, w2 in word_pairs:
		if (w1 in word_dic and w2 in word_dic):
			pair = (word_dic[w1], word_dic[w2])
			rev_pair = (pair[1], pair[0])
			if (rev_pair in dup_filter or pair in dup_filter):
				continue
			dup_filter.add(pair)
	for i1, i2 in dup_filter:
		data.append(abs(1-model.get_distance(i1, i2)))
	return data

def log_data(data):
	fname = input("Write log: ")
	with open(fname, 'w+') as fout:
		json.dump(data, fout)

# Generate data to plot
# data = get_nelson_dist()
# data = get_demasking_dist()
data = get_nelson_rand_dist()
print("Generated {} pairs".format(len(data)))
#log_data(data)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.hist(data, bins=20)

plt.show()