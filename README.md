# Python Toolkit

## Filtering Word-Pairs

Use `filter_paths.py` and supply required arguments to generate list of \<prime, target\> pair queries from .csv file. Optional `-lsa` flag generates word pairs in correct formatting for lsa web input (extraction of cosines).

## Generating Graphs

Use `filter_graph.py` and supply with some raw data file in `prime \t target \t path_length` format to extract all neighboring node pairs. Uses minimal memory and scans 600MB raw data file in 35s.

## Searching for paths

Use `search_graph.py` and supply filtered word list and .graph file to generate paths for each word pair. Graph is loaded into memory and a bfs is run with memoization to search for paths.
