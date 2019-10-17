import os
import sys
import subprocess
import analysis

# Our Plotting functions
parse_rt_path = analysis.parse_rt_path
plot_rt_path = analysis.plot_rt_path

# Make sure we have the proper configurations setup
CACHE_DIR = "C:/_YaoYiheng/_Projects/NLP_AssocMap/graph_processing/cache/"
GRAPH_DIR = "C:/_YaoYiheng/_Projects/NLP_AssocMap/graph_processing/graph/"
WORD_FILE = "C:/_YaoYiheng/_Projects/NLP_AssocMap/graph_processing/test_sets/nelson_words.txt"
argslist = f" -CACHE {CACHE_DIR} -GRAPH {GRAPH_DIR} -WORD {WORD_FILE}"

# Wrapper function for generating raw plot data
def plot_trend(arg1, arg2):
	return plot_rt_path(parse_rt_path(arg1, arg2))

# Wrapper function for launching os process to generate graph
def gen_graph(fname, args):
	cmd = "python C:/_YaoYiheng/_Projects/NLP_AssocMap/graph_processing/generate_graph.py " + fname + args
	print("Running child process:", cmd)
	return subprocess.Popen([cmd], stdout=subprocess.PIPE)

gen_graph_process = gen_graph(input("Graph output file name:"), argslist)

print("Gen_Graph ran with output:", file=sys.stderr)
print(gen_graph_process.communicate()[0])