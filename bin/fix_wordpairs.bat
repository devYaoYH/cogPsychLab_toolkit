@echo off
cd ..
set /P word_file="Word pair .csv file (prime,target) to fix: "
echo "Reading from... " + %word_file%
python filter_words.py %word_file%