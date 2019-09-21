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
FLAGS = set([])

# Number of required arguments
REQUIRED_ARGS = ["raw_graph_data", "output_graph.graph"]
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

INPUT_FILE = args[1]
OUTPUT_FILE = args[2]

alpha_set = set(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

filter_t = time.time()
with open(OUTPUT_FILE, 'w+') as fout:
    with open(INPUT_FILE, 'r') as fin:
        for line in fin:
            line_data = line.split()
            prime = line_data[0]
            length = -1
            try:
                length = int(float(line_data[-1]))
            except:
                # Improperly formatted float encountered
                # print("FLOAT ERROR line: {}".format(line), file=sys.stderr)
                continue
            target = ' '.join(line_data[1:-1])
            if (length == 1):
                fout.write("{} {}\n".format(prime, target))
                fout.flush()
            if (prime[0] in alpha_set):
                print("Scanning...[{}]".format(prime[0]), file=sys.stderr)
                alpha_set.remove(prime[0])

debug_time("Extracted graph 1-length edges...", filter_t, time.time())