#!/bin/bash
cd ..
echo Word pair .csv file (prime,target) to fix:
read word_file
echo Reading from... $word_file
python filter_words.py $word_file