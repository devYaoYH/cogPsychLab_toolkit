from __future__ import print_function
import re
import sys
import time

def debug_time(msg, init, now):
    print("{} [{}ms]".format(msg, int(round((now-init)*1000*1000))/1000.0), file=sys.stderr)

####################
# CMD LINE PARSING #
####################
argc = len(sys.argv)
argv = sys.argv

# List of cmdline flag variables
FLAG_LSA = "lsa"
FLAGS = set([FLAG_LSA])

# Number of required arguments
REQUIRED_ARGS = ["word_list"]
OPTIONAL_ARGS = {
    'g': "graph_edgelist"
}

NUM_REQUIRED_ARGS = len(REQUIRED_ARGS) + 1
# --> [executable name, word list file name]
args = argv[:NUM_REQUIRED_ARGS]

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

if (argc < 2):
    print_usage()
    exit()

# We scan through command line arguments and place them into the correct types
arg_i = NUM_REQUIRED_ARGS
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

# word pair .csv file
WORD_FILE = args[1]
# graph file with (from, to) word pairs representing an edge of distance 1 in graph
GRAPH_FILE = optional_args['g']

############################
# READ WORD LIST FROM FILE #
############################
init_t = time.time()
word_list = []
with open(WORD_FILE, 'r') as fin:
    for line in fin:
        prime = ""
        target = ""
        for i, c in enumerate(line):
            if (c == ','):
                prime = line[:i].lower().strip().strip('\"')
                target = line[i+1:].lower().strip().strip('\"')
                break
        # Use regex to extract words within brackets
        bracket_list = re.search("\(.*\)", target)
        if (bracket_list is not None):
            target = target[:bracket_list.span()[0]]
            extras = [s.strip() for s in bracket_list.group()[1:-1].split(',')]
            for extra in extras:
                word_list.append((prime, extra))
        word_list.append((prime, target))

debug_time("Finished extracting word pairs...", init_t, time.time())

###################
# WRITE WORD LIST #
###################
write_t = time.time()
# Write our filtered pairs to file
OUTPUT_FILTERED_WORDS = "{}_{}.txt".format(''.join(WORD_FILE.split('.')[:-1]), "filtered" if FLAG_LSA not in flags else "lsa")
print("Writing to:", OUTPUT_FILTERED_WORDS, file=sys.stderr)
with open(OUTPUT_FILTERED_WORDS, 'w+') as fout:
    if (FLAG_LSA in flags):
        # Output word list for LSA cosines web interface
        for prime, target in word_list:
            fout.write("{}\n\n{}\n\n".format(prime, target))
    else:
        for prime, target in word_list:
            fout.write("{} {}\n".format(prime, target))

debug_time("Finished printing word pairs...", write_t, time.time())

#############################
# LOAD GRAPH (if available) #
#############################
graph = None
if (GRAPH_FILE is not None):
    # Load graph from file
    graph = dict()
    graph_t = time.time()
    print("Loading graph from file: " + GRAPH_FILE, file=sys.stderr)

    debug_time("Graph Loaded...", graph_t, time.time())

#########################
# SEARCH GRAPH FOR PATH #
#########################
if (graph is not None):
    search_t = time.time()
    word_paths = {pair: -1 for pair in word_list}

    debug_time("Paths found...", search_t, time.time())