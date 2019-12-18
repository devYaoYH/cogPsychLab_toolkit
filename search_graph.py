from __future__ import print_function
import re
import sys
import time
import utils
try: 
    import queue
except ImportError:
    import Queue as queue

def debug_time(msg, init, now):
    print("{} [{}ms]".format(msg, int(round((now-init)*1000*1000))/1000.0), file=sys.stderr)

####################
# CMD LINE PARSING #
####################
argc = len(sys.argv)
argv = sys.argv

# List of cmdline flag variables
FLAG_DIRECTED = "d"
FLAGS = set([FLAG_DIRECTED])

# Number of required arguments
REQUIRED_ARGS = ["word_list", ".graph file", "output file name"]
OPTIONAL_ARGS = {
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

# word pair .csv file
WORD_FILE = args[1]
# graph file with (from, to) word pairs representing an edge of distance 1 in graph
GRAPH_FILE = args[2]
# output file to store paths
OUTPUT_PATH_FILE = args[3].replace('\\', '/')
output_path_file_split = OUTPUT_PATH_FILE.split("/")
extension = output_path_file_split[-1].split('.')[-1]
output_path_file_split[-1] = '.'.join(output_path_file_split[-1].split('.')[:-1]) + "_error." + extension
OUTPUT_PATH_ERROR_FILE = "/".join(output_path_file_split)
# is our graph directed?
is_directed = FLAG_DIRECTED in flags

print(OUTPUT_PATH_FILE)
print(OUTPUT_PATH_ERROR_FILE)

alpha_set = set(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()))
unrecognized_word_list = set()
graph_word_list = set()
graph_memoization = dict()

####################
# SEARCH ALGORITHM #
####################
def bfs(graph, source, destination):
    if (source not in graph_word_list):
        # print("ERROR word not found in graph: {}".format(source, file=sys.stderr))
        unrecognized_word_list.add(source)
        return None
    if (destination not in graph_word_list):
        # print("ERROR word not found in graph: {}".format(destination, file=sys.stderr))
        unrecognized_word_list.add(destination)
        return None
    try:
        return graph_memoization[source][destination]
    except KeyError:
        pass
    q = queue.Queue()
    v = set()
    q.put((source, [source]))
    while (not q.empty()):
        cur, path = q.get()
        if (cur in v):
            continue
        v.add(cur)
        if (cur not in graph):
            continue
        # Memoize graph
        try:
            graph_memoization[source][cur] = path
        except:
            graph_memoization[source] = {cur: path}
        if (cur == destination):
            return path
        for adj in graph[cur]:
            q.put((adj, path[:] + [adj]))
    return None

def dijkstra(graph, source, destination, decay=1.1):
    if (source not in graph_word_list):
        # print("ERROR word not found in graph: {}".format(source, file=sys.stderr))
        unrecognized_word_list.add(source)
        return None
    if (destination not in graph_word_list):
        # print("ERROR word not found in graph: {}".format(destination, file=sys.stderr))
        unrecognized_word_list.add(destination)
        return None
    q = queue.PriorityQueue()
    v = dict()
    q.put((0, source, [source]))
    while (not q.empty()):
        cost, cur, path = q.get()
        if (cur in v and v[cur] < cost):
            continue
        v[cur] = cost
        if (cur == destination):
            return (cost, path)
        for adj, weight in graph[cur]:
            adj_cost = cost + (1 - weight)*(decay**(len(path)-1))
            if (adj not in v):
                v[adj] = adj_cost
                q.put((adj_cost, adj, path[:] + [adj]))
            elif (v[adj] > adj_cost):
                v[adj] = adj_cost
                q.put((adj_cost, adj, path[:] + [adj]))
    return None

#######################
# LOAD WORD PAIR LIST #
#######################
word_t = time.time()
word_list = []
with open(WORD_FILE, 'r') as fin:
    for line in fin:
        line_data = line.strip().split(',')
        prime = line_data[0].lower()
        target = line_data[1].lower()
        word_list.append((prime, target))
debug_time("Loading word list...", word_t, time.time())

##############
# LOAD GRAPH #
##############
# Load graph from file
graph = dict()  # Stores graph as adjacency lists
graph_costs = dict()
graph_t = time.time()
print("Loading graph from file: " + GRAPH_FILE, file=sys.stderr)
graph = utils.load_graph(GRAPH_FILE, weighted=True)
graph_word_list = list(graph.keys())
# with open(GRAPH_FILE, 'r') as fin:
#     for line in fin:
#         line_data = line.strip().split(',')
#         source = line_data[0].lower()
#         destination = line_data[1].lower()
#         cost = None
#         if (len(line_data) > 2):
#             cost = float(line_data[2])
#         graph_word_list.add(source)
#         graph_word_list.add(destination)
#         try:
#             graph[source].add(destination)
#             if (cost is not None):
#                 graph_costs[source][destination] = cost
#         except KeyError:
#             graph[source] = set([destination])
#             if (cost is not None):
#                 graph_costs[source] = dict()
#                 graph_costs[source][destination] = cost
#         if (not is_directed):
#             try:
#                 graph[destination].add(source)
#             except KeyError:
#                 graph[destination] = set([source])
debug_time("Graph Loaded...", graph_t, time.time())

#########################
# SEARCH GRAPH FOR PATH #
#########################
search_t = time.time()
word_paths = dict()
path_cost = dict()
for pair in word_list:
    if (pair[0][0] in alpha_set):
        print("Scanning...[{}]".format(pair[0][0].upper()), file=sys.stderr)
        alpha_set.remove(pair[0][0])
    # word_paths[pair] = bfs(graph, pair[0], pair[1])
    results = dijkstra(graph, pair[0], pair[1])
    path_cost[pair], word_paths[pair] = results if results is not None else (None, None)
    # print(f"Found path {pair}: {path_cost[pair]} | {len(word_paths[pair])} | {word_paths[pair]}")
    if (is_directed):
        # word_paths[(pair[1], pair[0])] = bfs(graph, pair[1], pair[0])
        results = dijkstra(graph, pair[1], pair[0])
        path_cost[pair], word_paths[(pair[1], pair[0])] = results if results is not None else (None, None)
with open(OUTPUT_PATH_ERROR_FILE, 'w+') as fout:
    err_list = sorted(list(unrecognized_word_list))
    for word in err_list:
        fout.write("{}\n".format(word))
        fout.flush()
with open(OUTPUT_PATH_FILE, 'w+') as fout:
    for pair in word_list:
        if (word_paths[pair] is not None):
            # fout.write("{},{},{},\"".format(pair[0], pair[1], len(word_paths[pair])-1))
            fout.write("{},{},{},\"".format(pair[0], pair[1], path_cost[pair]))
            for node in word_paths[pair][:-1]:
                fout.write("{},".format(node))
            fout.write("{}".format(word_paths[pair][-1]))
            fout.write('\"')
            if (is_directed):
                # fout.write(",{},\"".format(len(word_paths[(pair[1], pair[0])])-1))
                fout.write(",{},\"".format(path_cost[(pair[1], pair[0])]))
                for node in word_paths[(pair[1], pair[0])][:-1]:
                    fout.write("{},".format(node))
                fout.write("{}".format(word_paths[(pair[1], pair[0])][-1]))
                fout.write('\"')
            fout.write('\n')
            fout.flush()
        else:
            fout.write("{},{},-1,\"NOT FOUND\"\n".format(pair[0], pair[1]))
            fout.flush()
debug_time("Paths found...", search_t, time.time())