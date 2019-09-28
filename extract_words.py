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
FLAG_SINGLE = "s"
FLAGS = set([FLAG_SINGLE])

# Number of required arguments
REQUIRED_ARGS = ["word_list"]
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
is_single = FLAG_SINGLE in flags

############################
# READ WORD LIST FROM FILE #
############################
word_t = time.time()
word_list = set()
with open(WORD_FILE, 'r') as fin:
    for line in fin:
        prime = ""
        target = ""
        # Split by FIRST instance of ',' comma
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
                if (is_single):
                    for extra_single in extra.split():
                        word_list.add((prime, extra_single))
                else:
                    word_list.add((prime, extra))
        if (is_single):
            for target_single in target.split():
                word_list.add((prime, target_single))
        else:
            word_list.add((prime, target))

word_list = sorted(list(word_list))
debug_time("Finished extracting word pairs...", word_t, time.time())

###################
# WRITE WORD LIST #
###################
write_t = time.time()
# Write our filtered pairs to file
OUTPUT_FILTERED_WORDS = "{}_{}.csv".format('.'.join(WORD_FILE.split('.')[:-1]), "filtered")
print("Writing to: ", OUTPUT_FILTERED_WORDS, file=sys.stderr)
with open(OUTPUT_FILTERED_WORDS, 'w+') as fout:
    for prime, target in word_list:
        # Output to csv format
        fout.write("{},{}\n".format(prime, target))

debug_time("Finished printing word pairs...", write_t, time.time())