#!/bin/bash
cd ..
echo Word pair .csv file (prime,target): 
read word_file
echo Reading (prime,target) information from... $word_file

echo Graph to run search in:
read graph_file
echo Reading graph information from... $graph_file

echo Output name of graph (need to include .csv):
read output_file
echo Printing extracted pathlengths output to... $output_file

echo Is the graph directed (y/n)?
read is_d

if ["$is_d" = "y"]; then
	echo DIRECTED GRAPH
	python search_graph.py %word_file% %graph_file% %output_file%
else
	python search_graph.py %word_file% %graph_file% %output_file% -d
fi