"""
make_model.py
Simulation Enabled Estimation of Kinetic Rates (SEEKR) is a tool that facilitates the preparation, running and analysis of multiscale MD/BD/Milestoning  simulations for the calculation of protein-ligand binding kinetics.

extracts transition information from the simulation output files and creates the milestoning model

Parameters
		----------
		milestone_filename : string Required 
				name of the XML file containing all information regarding simulation directories, parameters, etc.

		Returns
		-------
		model : class 
				contains all required information for milestoning analysis

		max_steps : int 
				total number of s
"""
import matplotlib.pyplot as plt
import pickle 
import numpy as np
from cycler import cycler
from itertools import islice


def plot_n_conv(conv_values, conv_intervals):
	fig, ax = plt.subplots()
	new_colors = [plt.get_cmap('tab20')(1.* i/(_get_colormap(conv_values))) for i in range(_get_colormap(conv_values))]
	plt.rc('axes', prop_cycle=(cycler('color', new_colors)))
	#ax = fig.add_subplot(1,1,1,)

	for i in range(conv_values.shape[0]):
		for j in range(conv_values.shape[1]):
				if np.sum(conv_values[i][j][:]) != 0:
					label_string = 'Src: '+str(i) +',' + 'Dest: '+str(j)
					ax.plot(np.multiply(conv_intervals,2e-6), conv_values[i][j][:], label = label_string ,
						linestyle='-', marker="o", markersize = 1)
	plt.xlabel('time (ns)')
	plt.ylabel('N/T')
	#plt.legend(loc = 'right')
	#box = fig.get_position()
	#plt.set_position([box.x0,box.y0, box.width * 0.8, box.height])
	plt.legend(loc ='center left', bbox_to_anchor=(1, 0.5), ncol = 2)  
	plt.grid(b=True,axis = 'y', which = 'both')
	return fig, ax

def plot_r_conv(conv_values, conv_intervals):
	fig, ax = plt.subplots()
	new_colors = [plt.get_cmap('tab20')(1.* i/(_get_colormap(conv_values))) for i in range(_get_colormap(conv_values))]
	plt.rc('axes', prop_cycle=(cycler('color', new_colors)))
	#ax = fig.add_subplot(1,1,1,)

	for i in range(conv_values.shape[0]):
		for j in range(conv_values.shape[1]):
				if np.sum(conv_values[i][j][:]) != 0:
					label_string = 'anchor ' +str(i) + ',' + 'Milestone '+str(j)
					ax.plot(np.multiply(conv_intervals,2e-6), conv_values[i][j][:], label = label_string ,
						linestyle='-', marker="o", markersize = 1)
	plt.xlabel('time (ns)')
	plt.ylabel('R/T')
	#plt.legend(loc = 'right')
	#box = fig.get_position()
	#plt.set_position([box.x0,box.y0, box.width * 0.8, box.height])
	plt.legend(loc ='center left', bbox_to_anchor=(1, 0.5), ncol = 2)  
	plt.grid(b=True,axis = 'y', which = 'both')
	return fig, ax

def _get_colormap(conv_values):
	cmap_length = 0
	for i in range(conv_values.shape[0]):
		for j in range(conv_values.shape[1]):
				if np.sum(conv_values[i][j][:]) != 0:
					cmap_length +=1
	return cmap_length

def plot_p_equil(conv_values, conv_intervals):
	fig, ax = plt.subplots()
	new_colors = [plt.get_cmap('tab20')(1.* i/conv_values.shape[0]) for i in range(conv_values.shape[0])]
	plt.rc('axes', prop_cycle=(cycler('color', new_colors)))
#f, (ax, ax2, ax3) = plt.subplots(3, 1, sharex=True)
	for i in range(conv_values.shape[0]):
		label_string = 'anchor ' +str(i)
		ax.plot(np.multiply(conv_intervals,2e-6), conv_values[i][:], 
						 label = label_string ,linestyle='-', marker="o", markersize = 1)
	plt.xlabel('time (ns)')
	plt.ylabel('p equil')
	plt.legend(loc ='center left', bbox_to_anchor=(1, 0.5), ncol = 2)  
	plt.grid(b=True,axis = 'y', which = 'both')
	return fig, ax

def plot_k_conv(conv_values, conv_intervals):
	fig, ax = plt.subplots()
	ax.plot(np.multiply(conv_intervals,2e-6), conv_values, linestyle='-', marker="o", markersize = 1)
	plt.ylabel('k off (s^-1)')
	plt.xlabel('time (ns)')
	#plt.legend(loc ='center left', bbox_to_anchor=(1, 0.5))
	return fig, ax

def MCMC_conv(running_avg, running_std):
	fig = plt.figure()
	ax = fig.add_subplot(2,1,1,)
	ax.plot(running_avg)
	ax.set_ylabel('Average off rate (1/s)')
	ax.set_xlabel('MCMC Samples')
	ax2 = fig.add_subplot(2,1,2,)
	ax2.plot(running_std)
	ax2.set_ylabel('off rate st. dev. (1/s)')
	ax2.set_xlabel('MCMC Samples')

	plt.savefig('MCMC_conv.png', format ='png', dpi=300 )
	pickle.dump(fig, open('MCMC.fig.pickle', 'wb'))
	plt.show()
	return fig, ax, ax2 

def _make_windows(seq, n):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def _calc_window_rmsd(conv_values):
    #print(conv_values)
    average = np.mean(conv_values)
    #print(average)
    test =conv_values - average
    #print(test)
    new_test = np.delete(test, 0)
    #print(new_test)
    RMSD = np.sqrt(np.sum(new_test)**2/(len(conv_values) -1))
    #print(RMSD)
    return RMSD

def plot_window_rmsd(conv_values, conv_intervals, window, cutoff):
	rmsd_list = []
	fig, ax = plt.subplots()
	new_colors = [plt.get_cmap('tab20')(1.* i/(_get_colormap(conv_values))) for i in range(_get_colormap(conv_values))]
	plt.rc('axes', prop_cycle=(cycler('color', new_colors)))
	#ax = fig.add_subplot(1,1,1,)

	for i in range(conv_values.shape[0]):
		for j in range(conv_values.shape[1]):
				if np.sum(conv_values[i][j][:]) != 0:
					rmsd_list = []
					windows = _make_windows(conv_values[i][j][:], window)
					for w in windows:
						rmsd_list.append(_calc_window_rmsd(w))
					label_string = str(i) + ',' +str(j)
					ax.plot(rmsd_list,
						linestyle='-', marker="o", markersize = 1, label = label_string ,)
	plt.xlabel('windows')
	plt.ylabel('RMSD')
	#plt.legend(loc = 'right')
	#box = fig.get_position()
	#plt.set_position([box.x0,box.y0, box.width * 0.8, box.height])
	plt.legend(loc ='center left', bbox_to_anchor=(1, 0.5), ncol = 2)  
	plt.grid(b=True,axis = 'y', which = 'both')
	return fig, ax
