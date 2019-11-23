import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def plot_line(data, title=None, savefile=None):
	print(data.shape)
	print(data)
	plt.figure()
	ax = plt.axes()
	X = data[:,0]
	Y = data[:,1]
	ERR = data[:,2]
	numbers = list(map(int, data[:,3]))
	plt.errorbar(list(map(int, X)), Y, yerr=ERR, capsize=5)
	if (title is not None):
		plt.title(title)
	ax.xaxis.set_major_locator(MaxNLocator(integer=True))
	for i, n in enumerate(numbers):
		plt.annotate(f"{n}", (X[i]+0.02, Y[i]-ERR[i]+0.02))
		plt.annotate(f"{ERR[i]:.3f}", (X[i]+0.02, Y[i]+ERR[i]+0.02))
	if (savefile is not None):
		plt.savefig(savefile)
	# plt.show()