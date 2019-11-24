@echo off
cd ..
set WORD_LIST=C:\_YaoYiheng\_Projects\NLP_AssocMap\_Results\DEMASKING_TASK\E2_fulldata_wordlist.csv
set OUTPUT=C:\_YaoYiheng\_Projects\NLP_AssocMap\_Results\DEMASKING_TASK\
FOR /L %%A IN (29, 1, 35) DO (
	python .\search_graph.py %WORD_LIST% .\graph\nelson_1_%%A.graph %OUTPUT%nelson_1_%%A_search.csv
)
REM python .\search_graph.py %WORD_LIST% .\graph\nelson_1_28.graph nelson_1_28_search.csv