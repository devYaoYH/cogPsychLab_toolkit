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
REQUIRED_ARGS = ["lsa_output_file"]
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
OUTPUT_FILE = '.'.join(args[1].split('.')[:-1]) + "_output.csv"
OUTPUT_ERROR_FILE = '.'.join(args[1].split('.')[:-1]) + "_error.csv"

print("Logging errors in: " + OUTPUT_ERROR_FILE)
print("Saving results in: " + OUTPUT_FILE)

print("\nRUNTIME ERRORS:")

with open(OUTPUT_ERROR_FILE, 'w+') as ferr:
    with open(OUTPUT_FILE, 'w+') as fout:
        with open(INPUT_FILE, 'r') as fin:
            # Ignore first 2 lines
            for line in fin:
                line = line.strip()
                if (line[:5] == "Texts"):
                    target = " ".join(line.split()[1:])
                    second_line = fin.readline().split()
                    prime = " ".join(second_line[:-1])
                    cosine = float(second_line[-1]) if second_line[-1] != "N/A" else "N/A"
                    # Extract relevant information into output file
                    fout.write("{},{},{}\n".format(prime, target, cosine))
                    fout.flush()
                else:
                    bracket_list = re.search(": \'.*\'", line)
                    if (bracket_list is not None):
                        ferr.write(bracket_list.group()[3:-1])
                        ferr.write("\n")
                        ferr.flush()
                    else:
                        print("Unrecognized line: " + line)