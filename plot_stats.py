import sys
import time
import math
import pandas as pd

def run_paths_stats():
	dataset = pd.read_csv("E2_fulldata.csv")
	dataline = dataset[["zRTTarget_trim", "directedfac"]]
	by_pathlength = dict()
	for i in range(len(dataline)):
		try:
			by_pathlength[int(dataline.loc[i][1])][0] += float(dataline.loc[i][0])
			by_pathlength[int(dataline.loc[i][1])][1] += 1
		except KeyError:
			by_pathlength[int(dataline.loc[i][1])] = [float(dataline.loc[i][0]), 1]
	for k in sorted(list(by_pathlength.keys())):
		print(f"Path Length: {k} | Mean zRT {by_pathlength[k][0]/by_pathlength[k][1]}")

if (__name__ == '__main__'):
	run_paths_stats()