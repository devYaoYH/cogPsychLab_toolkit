from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import json
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

graph_analysis_results = None
graph_plotting_params = None

GRAPH_PARAMS = 'expt_config.json'
GRAPH_RESULTS = 'graph\\analysis_log.json'

with open(GRAPH_PARAMS, 'r') as fin:
	graph_plotting_params = json.load(fin)

with open(GRAPH_RESULTS, 'r') as fin:
	graph_analysis_results = json.load(fin)

graph_analysis_name_labels = dict()
for gname, graph in graph_analysis_results.items():
	# gname = list(graph.keys())[0]
	graph_analysis_name_labels['.'.join(gname.split('.')[:-1])] = gname

graphs = dict()

for expt_config in graph_plotting_params['tests']:
	name = expt_config['name']
	min_edges = expt_config['filter_configs']['min_edges']
	cutoff = expt_config['filter_configs']['cutoff']

	graphs[name] = ((cutoff, min_edges), graph_analysis_results[graph_analysis_name_labels[name]])

# Plot details contained in our graphs list
x = []
y = []
z = []

for name, graph in graphs.items():
	cx = graph[1]['avg_connectivity']
	cy = graph[1]['avg_clustering']
	cz = graph[0][0]
	# if (cx > 12.5):
	# 	continue
	x.append(cx)
	y.append(cy)
	z.append(cz)
	ax.text(cx, cy, cz, '_'.join(name.split('_')[1:]), (1, 1, 1))

# Plot STANDARDS
baseline_graphs = ['pathlengths_directed_step_distance', 'pathlengths_undirected_kennetetal', 'pathlengths_undirected_step_distance', 'pathlengths_undirected_step_distance_pmfg']
for name in baseline_graphs:
	data = graph_analysis_results[graph_analysis_name_labels[name]]
	cx = data['avg_connectivity']
	cy = data['avg_clustering']
	cz = 0
	x.append(cx)
	y.append(cy)
	z.append(cz)
	ax.text(cx, cy, cz, name, (1, 1, 1))

ax.scatter(x, y, z, c='r', marker='o')

ax.set_xlabel('avg_connectivity')
ax.set_ylabel('avg_clustering')
ax.set_zlabel('Cosine Cutoff')

plt.show()