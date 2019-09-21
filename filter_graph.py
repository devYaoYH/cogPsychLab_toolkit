from __future__ import print_function
import sys
import time

def debug_time(msg, init, now):
    print("{} [{}ms]".format(msg, int(round((now-init)*1000*1000))/1000.0), file=sys.stderr)

if (len(sys.argv) != 3):
    print("Usage: python {} <input_file_name> <output_file_name>")
    exit()

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

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