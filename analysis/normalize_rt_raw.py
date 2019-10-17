from __future__ import print_function
import re
import os
import sys
import time
import numpy as np

# Filter out incorrect responses
# Take mean of all subjects responses
# Compare to network path lengths
def parse_rt_path(rt_data, path_length):
    columns = dict()
    with open(rt_data, "r") as fin:
        word_pairs = dict()
        for line in fin:
            prompt, target, correct, time = line.split(',')
            correct = True if correct == "1" else False
            time = int(time)
            if (not correct):
                continue
            pair = (prompt.lower(), target.lower())
            try:
                word_pairs[pair][0] += 1
                word_pairs[pair][1] += time
            except KeyError:
                word_pairs[pair] = [1, time]
    fin.close()

    with open(path_length, "r") as fin:
        paths = dict()
        for line in fin:
            items = line.split(',')
            paths[(items[0], items[1])] = int(items[2])
    fin.close()

    # Process Mean RT for all subjects
    rt_fname = rt_data.split('\\')[-1].split('.')[0]
    path_fname = path_length.split('\\')[-1].split('.')[0]
    output_fname = '\\'.join(path_length.split('\\')[:-1]) + "\\" + rt_fname + "_" + path_fname + ".csv"
    with open(output_fname, "w+") as fout:
        for key, value in word_pairs.items():
            word_pairs[key] = float(value[1]/value[0])
            if (key in paths):
                fout.write("{},{},{},{}\n".format(key[0], key[1], word_pairs[key], paths[key]))
    fout.close()
    return output_fname

if (__name__ == "__main__"):
    ####################
    # CMD LINE PARSING #
    ####################
    argc = len(sys.argv)
    argv = sys.argv

    # List of cmdline flag variables
    FLAGS = set([])

    # Number of required arguments
    REQUIRED_ARGS = ["rt_raw_file", "path_lengths"]
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

    parse_rt_path(args[1], args[2])