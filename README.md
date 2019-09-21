# Python Toolkit

## Filtering Word-Pairs

Use `filter_paths.py` and supply required arguments to generate list of \<prime, target\> pair queries from .csv file. Optional `-lsa` flag generates word pairs in correct formatting for lsa web input (extraction of cosines).

## Generating Graphs

Use `filter_graph.py` and supply with some raw data file in `prime \t target \t path_length` format to extract all neighboring node pairs. Uses minimal memory and scans 600MB raw data file in 35s.

## Searching for paths

Use `search_graph.py` and supply filtered word list and .graph file to generate paths for each word pair. Graph is loaded into memory and a bfs is run with memoization to search for paths.

#### Search Script Outputs
```
PS > python .\search_graph.py .\word_pairs_filtered.txt .\graph\pat
hlengths_directed_step_distance.graph .\paths\pathlengths_directed_step_distance.csv -d
Loading word list... [3.001ms]
Loading graph from file: .\graph\pathlengths_directed_step_distance.graph
Graph Loaded... [93.029ms]
Paths found... [18380.337ms]

PS > python .\search_graph.py .\word_pairs_filtered.txt .\graph\pat
hlengths_undirected_kennetetal.graph .\paths\pathlengths_undirected_kennetetal.csv
Loading word list... [3.0ms]
Loading graph from file: .\graph\pathlengths_undirected_kennetetal.graph
Graph Loaded... [52.012ms]
Paths found... [23884.555ms]

PS > python .\search_graph.py .\word_pairs_filtered.txt .\graph\pat
hlengths_undirected_step_distance.graph .\paths\pathlengths_undirected_step_distance.csv
Loading word list... [2.028ms]
Loading graph from file: .\graph\pathlengths_undirected_step_distance.graph
Graph Loaded... [177.338ms]
Paths found... [16875.377ms]

PS > python .\search_graph.py .\word_pairs_filtered.txt .\graph\pat
hlengths_undirected_step_distance_pmfg.graph .\paths\pathlengths_undirected_step_distance_pmfg.csv
Loading word list... [2.0ms]
Loading graph from file: .\graph\pathlengths_undirected_step_distance_pmfg.graph
Graph Loaded... [53.012ms]
Paths found... [23980.844ms]
```