from __future__ import print_function
import re
import os
import sys
import time
import numpy as np

def plot_rt_path(rt_data):
    columns = dict()
    with open(rt_data, "r") as fin:
        network_lengths = dict()
        for line in fin:
            prompt, target, time, length = line.split(',')
            time = float(time)
            length = int(length)
            if (length < 0):
                continue
            try:
                network_lengths[length].append(time)
            except KeyError:
                network_lengths[length] = [time]
    fin.close()

    s_key_list = []
    for key in network_lengths.keys():
        s_key_list.append(key)
    s_key_list = sorted(s_key_list)
    for key in s_key_list:
        print("{}: {}".format(key, len(network_lengths[key])))

    # Compute Numpy std/mean for each length
    output_fname = '.'.join(rt_data.split('.')[:-1]) + "_plot.csv"
    with open(output_fname, "w+") as fout:
        for key in s_key_list:
            li = network_lengths[key]
            data = np.array(li)
            fout.write("{},{},{},{}\n".format(key, np.mean(data), np.std(data), len(li)))
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
    REQUIRED_ARGS = ["rt_vs_pathlengths"]
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

    plot_rt_path(args[1])