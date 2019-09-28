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
REQUIRED_ARGS = ["word_list"]
OPTIONAL_ARGS = {
}

# Define this to print more helpful messages after cmd usage line
def help():
    print(".csv word pair file (prime, target) -> .txt lsa formatted file:")
    print("==========\n|prime\n|\n|target\n|\n==FORMAT==")

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
    help()

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

OUTPUT_LSA_WORDS = "{}_{}.txt".format('.'.join(WORD_LIST.split('.')[:-1]), "lsa")

print("Storing lsa formatted word pairs in: " + OUTPUT_LSA_WORDS)

# Load word list
with open(OUTPUT_LSA_WORDS, 'w+') as fout:
    with open(WORD_LIST, 'r') as fin:
        for line in fin:
            prime, target = line.split(',')
            prime = prime.strip().lower()
            target = target.strip().lower()
            # Write to lsa file
            fout.write("{}\n\n{}\n\n".format(prime, target))