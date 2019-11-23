import sys
import time
import math
import utils
import scipy.stats as sci_stats
import numpy as np
import pandas as pd

def run_paths_stats():
	dataset = pd.read_csv("E2_fulldata.csv")
	covariates = ["mean_len_c", "mean_logf_c", "mean_ldtz_c", "mean_conc_c"]
	VSM_vars = ["word2veccosine", "LSA"]
	control_networks = ["Undirected", "newdirected", "pathlength", "UPMFG_Cat"]
	word2vec_networks = [f"path_{i}" for i in range(28, 36)]
	for network in control_networks + word2vec_networks:
		by_pathlength = dict()
		dataline = dataset[["zRTTarget_trim", "word2veccosine", "LSA", network]]
		for i in range(len(dataline)):
			try:
				by_pathlength[int(dataline.loc[i][3])][0] = np.append(by_pathlength[int(dataline.loc[i][3])][0], [float(dataline.loc[i][0])])
				by_pathlength[int(dataline.loc[i][3])][1] = np.append(by_pathlength[int(dataline.loc[i][3])][1], [float(dataline.loc[i][1])])
				by_pathlength[int(dataline.loc[i][3])][2] = np.append(by_pathlength[int(dataline.loc[i][3])][2], [float(dataline.loc[i][2])])
			except KeyError:
				by_pathlength[int(dataline.loc[i][3])] = [np.array([float(dataline.loc[i][0])]), np.array([float(dataline.loc[i][1])]), np.array([float(dataline.loc[i][2])])]
		print(f"Network [{network}]")
		plot_data = []
		for k in sorted(list(by_pathlength.keys())):
			plot_data.append((k, np.mean(by_pathlength[k][1]), np.std(by_pathlength[k][1]), by_pathlength[k][1].shape[0]))
			print(f"Path Length: {k}  \t| Num: {by_pathlength[k][0].shape[0]}  \t| Mean zRT: {np.mean(by_pathlength[k][0]):.5f} \t| Mean word2vec: {np.mean(by_pathlength[k][1]):.5f} \t| Mean LSA: {np.mean(by_pathlength[k][2]):.5f}")
		savefile = input("Save network plot? (y/n): ")
		if (savefile != "y"):
			savefile = None
		else:
			savefile = f"plots/{network}_word2vec_plot.png"
		utils.plot_line(np.array(plot_data), title=network, savefile=savefile)

if (__name__ == '__main__'):
	run_paths_stats()