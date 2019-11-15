from __future__ import print_function
import os
import sys
import time
import json
import queue
import random

def debug_time(msg, init, now):
    print("{} [{}ms]".format(msg, int(round((now-init)*1000*1000))/1000.0), file=sys.stderr)

# Characterises each .graph file in the current directory (if argument not given)
# and outputs to stdout details (if not redirected to output json)

####################
# CMD LINE PARSING #
####################
argc = len(sys.argv)
argv = sys.argv

# List of cmdline flag variables
FLAG_JSON = "json"
FLAGS = set([FLAG_JSON])

# Number of required arguments
REQUIRED_ARGS = []
OPTIONAL_ARGS = {
    'dir': "directory to scan for .graph files"
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

is_json_output = FLAG_JSON in flags
GRAPH_DIR = "." if optional_args['dir'] is None else optional_args['dir']

####################
# HELPER FUNCTIONS #
####################
def load_graph(g_file, is_directed):
    # Load graph from file
    graph = dict()  # Stores graph as adjacency lists
    graph_t = time.time()
    graph_word_list = set()
    print("Loading graph from file: " + g_file, file=sys.stderr)
    with open(g_file, 'r') as fin:
        for line in fin:
            line_data = line.strip().split(',')
            source = line_data[0].lower()
            destination = line_data[1].lower()
            graph_word_list.add(source)
            graph_word_list.add(destination)
            try:
                graph[source].add(destination)
            except KeyError:
                graph[source] = set([destination])
            if (not is_directed):
                try:
                    graph[destination].add(source)
                except KeyError:
                    graph[destination] = set([source])
    debug_time("Graph Loaded...", graph_t, time.time())
    return graph, graph_word_list

def get_graphs():
    # Get all .graph files in selected folder
    for (dirpath, dirnames, filenames) in os.walk(GRAPH_DIR):
        return [(f, input(f"is graph {f} directed (y/n)?")=='y') for f in filenames if f.split('.')[-1] == 'graph']
    return []

def bfs(s, t, graph):
    v = set()
    q = queue.Queue()
    q.put((s, 0))
    v.add(s)
    while (not q.empty()):
        cur, dist = q.get()
        if (cur == t):
            return dist
        for adj in graph[cur]:
            if (adj not in v):
                q.put((adj, dist+1))
                v.add(adj)
    return None

####################################
# GRAPH CHARACTERIZATION FUNCTIONS #
####################################
# Local Clustering Coefficient
def cluster_coeff(graph, s):
    if (s not in graph):
        return 0
    direct_neighbors = set(graph[s])
    direct_neighbors.add(s)
    total_possible_conections = len(direct_neighbors)*(len(direct_neighbors)-1)/2
    if (total_possible_conections == 0):
        return 0
    local_links = 0
    for w in direct_neighbors:
        for to_node in graph[w]:
            if (to_node in direct_neighbors):
                local_links += 1
    local_links /= 2
    return local_links/total_possible_conections

# Average number of outgoing edges
def average_connectivity(graph):
    min_edges = 999999999
    max_edges = -1
    sum_edges = 0
    num_nodes = len(graph.keys())
    for s in graph.keys():
        cur_edges = len(graph[s])
        sum_edges += cur_edges
        min_edges = min(min_edges, cur_edges)
        max_edges = max(max_edges, cur_edges)
    return min_edges,sum_edges/num_nodes,max_edges

# Average pathlength in graph
def average_pathlength(graph, graph_word_list, k=100):
    p_len_tot = 0
    tot_num = k
    # run k random s,t pairs to test
    for i in range(k):
        s = random.choice(graph_word_list)
        t = random.choice(graph_word_list)
        cur_len = bfs(s, t, graph)
        if (cur_len is not None):
            p_len_tot += cur_len
        else:
            tot_num -= 1
    return p_len_tot/tot_num if tot_num > 0 else 9999999

def analyze_graph(graph, graph_word_list):
    # Get global average clustering coeff
    avg_clustering = sum([cluster_coeff(graph, s) for s in graph.keys()])/len(graph.keys())
    # Get average node connectivity
    min_connectivity, avg_connectivity, max_connectivity = average_connectivity(graph)
    # Get average path length for 100 runs
    avg_pathlength = average_pathlength(graph, graph_word_list)
    return {
        "avg_clustering": avg_clustering,
        "min_connectivity": min_connectivity,
        "avg_connectivity": avg_connectivity,
        "max_connectivity": max_connectivity,
        "avg_pathlength": avg_pathlength
    }

######################
# ANALYZE ALL GRAPHS #
######################
def run():
    graphs = get_graphs()
    analysis_result = dict()
    try:
        with open('analysis_log.json', 'r') as fin:
            present_analysis = json.load(fin)
        for g_name, data in present_analysis.items():
            analysis_result[g_name] = data
    except Exception as e:
        print(e)
        print("No prior data found...")
        present_analysis = dict()
    for g_name, graph_directed in graphs:
        if (g_name in analysis_result and not input(f"Graph {g_name} already analyzed...Run again (y/n)?") == 'y'):
            continue
        graph, graph_word_list = load_graph(g_name, graph_directed)
        analysis_output = analyze_graph(graph, list(graph_word_list))
        for key, value in analysis_output.items():
            print(f"    {key}\t: {value}")
        if (is_json_output):
            analysis_result[g_name] = analysis_output
    if (is_json_output):
        with open('analysis_log.json', 'w+') as fout:
            json.dump(analysis_result, fout)

if __name__ == '__main__':
    msg = "Launching Graph Analysis utility"
    print("#"*(len(msg)+2))
    print(f"#{msg}#")
    print("#"*(len(msg)+2))
    print_usage()
    print("-"*(len(msg)+2))
    run()