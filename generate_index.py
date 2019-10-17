import sys
import time
import numpy as np
from annoy import AnnoyIndex
from gensim.models.keyedvectors import KeyedVectors

def debug_time(msg, init, now):
    print("{} [{}ms]".format(msg, int(round((now-init)*1000*1000))/1000.0), file=sys.stderr)

# Configuration Parameters
DATA_PATH = 'C:/_YaoYiheng/_Projects/NLP_AssocMap/linguistic_association_networks/data/'
VSM_BIN = "GoogleNews-vectors-negative300.bin"
VSM_LIMIT = 100000
WORD_FILE = "../test_sets/nelson_words.txt"
word_list_name = "nelson"

# Optionally load word file
if (WORD_FILE is not None):
    loaded_words = []
    with open(WORD_FILE, 'r') as fin:
        for line in fin:
            loaded_words.append(line.lower().strip().replace(' ', '_'))
    print(f"Loaded words from {WORD_FILE}", file=sys.stderr)

# Load gensim model
load_t = time.time()
if (WORD_FILE is None):
    model = KeyedVectors.load_word2vec_format(f'{DATA_PATH}{VSM_BIN}', binary=True, limit=VSM_LIMIT)
else:
    model = KeyedVectors.load_word2vec_format(f'{DATA_PATH}{VSM_BIN}', binary=True)
dims = 300
lowercase_dic = {w.lower(): w for w in model.vocab.keys()}
debug_time(f"Loaded gensim model for top {VSM_LIMIT if WORD_FILE is None else 'all'} vectors", load_t, time.time())

# Build index tree
print(f"Building index tree for {VSM_LIMIT if WORD_FILE is None else 'selected'} words:", file=sys.stderr)
init_t = time.time()
t = AnnoyIndex(dims)
i = 0
with open(f"cache/GoogleNews_wordlist_{VSM_LIMIT if WORD_FILE is None else word_list_name}.txt", "w+") as fout:
    for word in model.vocab.keys() if WORD_FILE is None else loaded_words:
        # Get vector, push into ann
        if (not i%1000):
            print(i, word, file=sys.stderr)
        try:
            t.add_item(i, model[word])
            fout.write(f"{i}\t{word.encode('utf8')}\n")
            i += 1
            continue
        except:
            try:
                t.add_item(i, model[lowercase_dic[word]])
                fout.write(f"{i}\t{word.encode('utf8')}\n")
                i += 1
                print("Word replacement found: ", lowercase_dic[word], file=sys.stderr)
            except:
                print("Word not found:", word)
# 53 trees (speed/space tradeoff)
# If we build with more trees, faster lookup, but larger disk footprint
t.build(53)

# Write to file
t.save(f"{DATA_PATH}GoogleNews_index_{VSM_LIMIT if WORD_FILE is None else word_list_name}.ann")
debug_time("Successfully Generated Index Tree", init_t, time.time())