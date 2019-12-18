import sys
import time

###################################
# Data Wrangling Helper functions #
###################################
def read_wordpairs(fname, delim=','):
    word_pairs = []
    i = 0
    with open(fname, 'r') as fin:
        for line in fin:
            i += 1
            line_data = line.strip().split(delim)
            if (len(line_data) < 2):
                print("Insufficient Items in line {} (Expected 2)".format(i), file=sys.stderr)
                return word_pairs
            prime = line_data[0].lower()
            target = line_data[1].lower()
            word_pairs.append((prime, target))
    return word_pairs

def load_graph(fname, delim=',', weighted=False):
    graph = dict()
    with open(fname, 'r') as fin:
        for line in fin:
            line_contents = line.strip().split(delim)
            if (weighted and len(line_contents) < 3):
                print("Error: Insufficient arguments on line:", line)
                return None
            if (weighted):
                prime, target, weight = line_contents
                weight = float(weight)
                try:
                    graph[prime].append((target, weight))
                except KeyError:
                    graph[prime] = [(target, weight)]
            else:
                prime, target = line_contents
                try:
                    graph[prime].append(target)
                except KeyError:
                    graph[prime] = [target]
    return graph

def load_data(fname, delim=',', expt=1, d_filter=None):
    if (d_filter is None):
        d_filter = [None for i in range(expt)]
    data = []
    i = 0
    with open(fname, 'r') as fin:
        for line in fin:
            i += 1
            line_data = line.strip().split(delim)
            if (len(line_data) < expt):
                print("Insufficient Items in line {} (Expected {})".format(i, expt), file=sys.stderr)
                return data
            try:
                data.append([d_filter[i](d) if d_filter[i] is not None else d for i, d in enumerate(line_data[:expt])])
            except Exception as e:
                print(e)
                print(line_data)
    return data

def write_data(fname, data, delim=','):
    with open(fname, 'w+') as fout:
        for d in data:
            fout.write(delim.join([str(di) for di in d]))
            fout.write("\n")

def join_data(fname, key=2, delim=None, expt=None, d_filter=None):
    if (delim is None):
        delim = [',' for i in range(len(fname))]
    if (expt is None):
        expt = [1 for i in range(len(fname))]
    if (d_filter is None):
        d_filter = [None for i in range(len(fname))]
    tot_k_set = set()
    tot_data = dict()
    for i, f in enumerate(fname):
        f_data = load_data(f, delim=delim[i], expt=expt[i], d_filter=d_filter[i])
        f_data_len = 0
        f_keyed_data = dict()
        for d in f_data:
            d_key = tuple(d[:key])
            tot_k_set.add(d_key)
            if (d_key not in f_keyed_data):
                f_keyed_data[d_key] = []
            f_keyed_data[d_key] = d[key:]
            f_data_len = max(f_data_len, len(f_keyed_data[d_key]))
        f_keyed_data['len'] = f_data_len
        print("len {}".format(f_keyed_data['len']))
        tot_data[f] = f_keyed_data
    out_data = []
    for k in tot_k_set:
        k_data = list(k)
        for f in fname:
            if (k in tot_data[f]):
                k_data.extend(tot_data[f][k])
            else:
                k_data.extend(["N/A" for i in range(tot_data[f]['len'])])
        out_data.append(k_data)
        print(k_data)
    return sorted(out_data)