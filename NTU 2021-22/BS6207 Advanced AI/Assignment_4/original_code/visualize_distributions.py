import numpy as np
import argparse

import os
import sys
import matplotlib.pyplot as plt

import itertools


parser = argparse.ArgumentParser(description='')

parser.add_argument('--metrics_files_dir', default='loss_data/', help='Text file to write step, loss, accuracy metrics', dest='metrics_files_dir')
parser.add_argument('--distributions_dir', default='distributions/', help='', dest='distributions_dir')
parser.add_argument('--num_bins', default='11', type=int, help='Number of bins in kde layer', dest='num_bins')
parser.add_argument('--subset_length', default='10', type=int, help='Length of subset', dest='subset_length')
parser.add_argument('--dataset_type', default='test', help='', dest='dataset_type')
parser.add_argument('--description', help='', dest='description')

FLAGS = parser.parse_args()

if FLAGS.description:
	description = FLAGS.description
else:
	print('Error: description is not given!!!')
	sys.exit()

NUM_BINS = FLAGS.num_bins

classes = ['0','1','2','3','4','5','6','7','8','9']

metrics_files_dir = FLAGS.metrics_files_dir + description + '/'
distributions_dir = FLAGS.distributions_dir + description + '/'

description2 = '__'.join(description.split('__')[:-1])
saved_models_file = metrics_files_dir + 'saved_model_weights_filenames_{}_element_subsets__{}.txt'.format(FLAGS.subset_length, description2)
saved_models_arr = np.loadtxt(saved_models_file, comments='#', delimiter='\t', dtype='str')
# print(saved_models_arr)

if saved_models_arr.ndim > 1:
	num_models = saved_models_arr.shape[0]
else:
	num_models = 1	

for j in range(num_models):
	if saved_models_arr.ndim > 1:
		subset_elements_str = saved_models_arr[j,0]
		model_weights_filename = saved_models_arr[j,1].split('/')[1]
	else:
		subset_elements_str = saved_models_arr[0]
		model_weights_filename = saved_models_arr[1].split('/')[1]

	current_time = model_weights_filename[13:-3]
	print(current_time)

	distributions_file_name = distributions_dir + '{}_distributions'.format(FLAGS.dataset_type) + current_time + '.txt'
	distributions_arr = np.loadtxt(distributions_file_name, comments='#', delimiter='\t', dtype='float32')

	hist_max = np.amax(distributions_arr)

	num_features = int(distributions_arr.shape[1]/NUM_BINS)

	# m_color = ['Blue','DarkGreen','Brown','BurlyWood','CadetBlue','Chartreuse','Chocolate','Coral','Cyan','BlueViolet']
	m_color = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
	m_shape=['-',':']
	fig, ax = plt.subplots(len(classes),num_features,figsize=(16, 10))
	fig.subplots_adjust(left=0.04, right=0.98, top=0.95, bottom=0.1)
	# plt.suptitle('deneme')
	fig.canvas.set_window_title(distributions_dir + '{}_distributions'.format(FLAGS.dataset_type) + current_time + '.png')

	legend_color = list()
	for h in range(num_features):
		temp_hist_data = distributions_arr[:,h*NUM_BINS:(h+1)*NUM_BINS]

		for c in range(len(classes)):
			data = temp_hist_data[c,:]

			ax1 = ax[c,h]
			bp, = ax1.plot(np.arange(0,1.1,0.1),data,c=m_color[c],linestyle='-')

			if h == (num_features -1):
				legend_color.append(bp)

			ax1.tick_params(axis='both',labelsize=6)
			ax1.tick_params(axis='x',rotation=90)
			ax1.set_ylim((-0.05,hist_max+0.05))
			ax1.yaxis.set_ticks(np.arange(0, hist_max+0.05, 0.1))
			ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
			ax1.set_xlim((-0.1,1.1))
			ax1.xaxis.set_ticks(np.arange(0, 1.1, 0.2))
			# ax1.xaxis.set_tick_params(labelsize=6, label1On=False)
			ax1.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
			ax1.set_axisbelow(True)
	
	fig.tight_layout()
	fig.subplots_adjust(left=0.03, right=0.98, top=0.96, bottom=0.10)
	fig.legend(legend_color, classes, loc='lower center', bbox_to_anchor=(0.5, 0.01), fancybox=True, shadow=True, ncol=10, fontsize=15)

	fig_filename = distributions_dir + '{}_distributions'.format(FLAGS.dataset_type) + current_time + '.png'
	# fig.savefig(fig_filename, bbox_inches='tight')
	fig.savefig(fig_filename, bbox_inches='tight')

	# plt.show()

print('Visualization finished!!!')
sys.exit()
