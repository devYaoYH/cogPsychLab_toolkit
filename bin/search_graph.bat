@echo off
cd ..
set /P word_file="Word pair .csv file (prime,target): "
echo Reading (prime,target) information from... %word_file%
set /P graph_file="Graph to run search in: "
echo Reading graph information from... %graph_file%
set /P output_file="Output name of graph (need to include .csv): "
echo Printing extracted pathlengths output to... %output_file%
set /P is_d="Is the graph directed (y/n)? "
if "%is_d%"=="y" (
	echo DIRECTED GRAPH
	python search_graph.py %word_file% %graph_file% %output_file%
) else (
	python search_graph.py %word_file% %graph_file% %output_file% -d
)