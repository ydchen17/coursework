import numpy as np
import argparse

import os
import sys

from time import time
from scipy.optimize import linear_sum_assignment

parser = argparse.ArgumentParser(description='')

parser.add_argument('--model_dir', default='saved_models/', help='Directory to save models', dest='model_dir')
parser.add_argument('--metrics_files_dir', default='loss_data/', help='Text file to write step, loss, accuracy metrics', dest='metrics_files_dir')
parser.add_argument('--clustering_dir', default='clustering/', help='', dest='clustering_dir')
parser.add_argument('--subset_length', default='10', type=int, help='Length of subset', dest='subset_length')
parser.add_argument('--dataset_type', default='test', help='', dest='dataset_type')
parser.add_argument('--clustering_type', help='', dest='clustering_type')
parser.add_argument('--description', help='', dest='description')

FLAGS = parser.parse_args()

if FLAGS.description:
	description = FLAGS.description
	print('description:{}'.format(description))
else:
	print('Error: description is not given!!!')
	sys.exit()

splitted_dataset = np.load('../../data/mnist/splitted_mnist_dataset.npz')
truth_labels_arr = splitted_dataset['y_{}'.format(FLAGS.dataset_type)]
del splitted_dataset

metrics_files_dir = FLAGS.metrics_files_dir + description + '/'
saved_models_dir = FLAGS.model_dir + description + '/'

clustering_dir = FLAGS.clustering_dir + description + '/'
if not os.path.exists(clustering_dir):
	os.makedirs(clustering_dir)

description2 = '__'.join(description.split('__')[:-1])
saved_models_file = metrics_files_dir + 'saved_model_weights_filenames_{}_element_subsets__{}.txt'.format(FLAGS.subset_length, description2)
saved_models_arr = np.loadtxt(saved_models_file, comments='#', delimiter='\t', dtype='str')
# print(saved_models_arr)

if saved_models_arr.ndim > 1:
	# num_models = saved_models_arr.shape[0]
	num_models = 5
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

	predicted_labels_filename = clustering_dir + '{}_predicted_labels_{}'.format(FLAGS.dataset_type,FLAGS.clustering_type) + current_time + '.txt'
	predicted_labels_arr = np.loadtxt(predicted_labels_filename, delimiter='\t', dtype='int')

	cost_matrix = np.zeros((10,10))
	num_samples = np.zeros(10)
	for truth_val in range(10):
		# print('truth_val:{}'.format(truth_val))
		temp_sample_indices = np.where(truth_labels_arr == truth_val)[0]
		num_samples[truth_val] = temp_sample_indices.shape[0]

		temp_predicted_labels = predicted_labels_arr[temp_sample_indices]

		for predicted_val in range(10):

			temp_matching_pairs = np.where(temp_predicted_labels == predicted_val)[0]

			cost_matrix[truth_val,predicted_val] = 1- (temp_matching_pairs.shape[0]/temp_sample_indices.shape[0])

			# print('predicted_val:{}'.format(predicted_val))
			# print('num samples:{}'.format(temp_sample_indices.shape[0]))
			# print('num matching pairs:{}'.format(temp_matching_pairs.shape[0]))
			# print('accuracy:{}'.format(temp_matching_pairs.shape[0]/temp_sample_indices.shape[0]))
			# print('cost:{}'.format(1- (temp_matching_pairs.shape[0]/temp_sample_indices.shape[0])))

	# print(np.round(cost_matrix,3))

	row_ind, col_ind = linear_sum_assignment(cost_matrix)

	cost = cost_matrix[row_ind,col_ind]

	clustering_acc = ((1-cost)*num_samples).sum() / num_samples.sum()

	# print(row_ind)
	# print(col_ind)
	# print(np.round(cost,3))
	# print(num_samples)
	print('Clustering acc:{}'.format( ((1-cost)*num_samples).sum() / num_samples.sum() ) )

	clustering_acc_filename = clustering_dir + '{}_clustering_acc_{}'.format(FLAGS.dataset_type,FLAGS.clustering_type) + current_time + '.txt'
	np.savetxt(clustering_acc_filename, clustering_acc.reshape((-1,1)), fmt='%.4f', delimiter='\t')
	


		

print('Clustering accuracy calculation completed!!!')
sys.exit()



