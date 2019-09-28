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
FLAGS = set([])

# Number of required arguments
REQUIRED_ARGS = ["word_list", "acn_graph_data"]
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

WORD_LIST = args[1]
GRAPH_DATA = args[2]
OUTPUT_FILE = "{}_{}.csv".format('.'.join(WORD_LIST.split('.')[:-1]), "acn")

alpha_set = set(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()))

# Load word list
word_list = []
word_acn_map = dict()
with open(WORD_LIST, 'r') as fin:
    for line in fin:
        prime, target = line.split(',')
        prime = prime.strip().lower()
        target = target.strip().lower()
        word_acn_map[(prime, target)] = "N/A"
        word_list.append((prime, target))

# Scan through graph
extract_t = time.time()
with open(GRAPH_DATA, 'r') as fin:
    for line in fin:
        prime, target, dist = line.split('\t')
        prime = prime.strip().lower()
        target = target.strip().lower()
        try:
            dist = float(dist.strip())
        except:
            dist = "N/A"
        # Print out progress
        if (prime[0] in alpha_set):
            print("Scanning...[{}]".format(prime[0].upper()), file=sys.stderr)
            alpha_set.remove(prime[0])
        # Store acn value
        if ((prime, target) in word_acn_map):
            word_acn_map[(prime, target)] = dist

# Output distance values
with open(OUTPUT_FILE, 'w+') as fout:
    for k in word_list:
        fout.write("{},{},{}\n".format(k[0], k[1], word_acn_map[k]))
        fout.flush()

debug_time("Extracted acn pair values from graph data...", extract_t, time.time())