import numpy as np
import argparse

import os
import sys


def kde(data, num_nodes=None, sigma=None, batch_size=None, num_features=None):
	# print('kde data shape:{}'.format(data.shape))
	# print('num_nodes:{}'.format(num_nodes))
	# print('sigma:{}'.format(sigma))

	k_sample_points = np.tile(np.linspace(0,1,num=num_nodes),[batch_size,data.shape[1],1])
	# print('kde k_sample_points shape:{}'.format(k_sample_points.shape))

	k_alfa = 1/np.sqrt(2*np.pi*np.square(sigma))
	k_beta = -1/(2*np.square(sigma))

	out_list = list()
	for i in range(num_features):
		temp_data = np.reshape(data[:,:,i],(-1,data.shape[1],1))
		# print('temp_data shape:{}'.format(temp_data.shape))

		k_diff = k_sample_points - np.tile(temp_data,[1,1,num_nodes])
		k_diff_2 = np.square(k_diff)
		# print('k_diff_2 shape:{}'.format(k_diff_2.shape))

		k_result = k_alfa * np.exp(k_beta*k_diff_2)

		k_out_unnormalized = np.sum(k_result,axis=1)

		k_norm_coeff = np.reshape(np.sum(k_out_unnormalized,axis=1),(-1,1))

		k_out = k_out_unnormalized / np.tile(k_norm_coeff, [1,k_out_unnormalized.shape[1]])
		# print('k_out shape:{}'.format(k_out.shape))

		out_list.append(k_out)


	concat_out = np.concatenate(out_list,axis=-1)
	# print('concat_out shape:{}'.format(concat_out.shape))
	
	return concat_out

parser = argparse.ArgumentParser(description='')

parser.add_argument('--model_dir', default='saved_models/', help='Directory to save models', dest='model_dir')
parser.add_argument('--metrics_files_dir', default='loss_data/', help='Text file to write step, loss, accuracy metrics', dest='metrics_files_dir')
parser.add_argument('--features_dir', default='extracted_features/', help='', dest='features_dir')
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

splitted_dataset = np.load('../../data/mnist/splitted_mnist_dataset.npz')
labels_arr = splitted_dataset['y_{}'.format(FLAGS.dataset_type)]
del splitted_dataset

metrics_files_dir = FLAGS.metrics_files_dir + description + '/'
saved_models_dir = FLAGS.model_dir + description + '/'
extracted_features_dir = FLAGS.features_dir + description + '/'

distributions_dir = FLAGS.distributions_dir + description + '/'
if not os.path.exists(distributions_dir):
	os.makedirs(distributions_dir)

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

	# labels_filename = extracted_features_dir + '{}_labels'.format(FLAGS.dataset_type) + current_time + '.txt'
	# labels_arr = np.loadtxt(labels_filename, comments='#', delimiter='\t', dtype='int')
	
	features_file_name = extracted_features_dir + '{}_features'.format(FLAGS.dataset_type) + current_time + '.txt'
	features_arr = np.loadtxt(features_file_name, comments='#', delimiter='\t', dtype='float32')

	num_features = features_arr.shape[1]

	distributions_file_name = distributions_dir + '{}_distributions'.format(FLAGS.dataset_type) + current_time + '.txt'
	mean_features_file_name = extracted_features_dir + '{}_mean_features'.format(FLAGS.dataset_type) + current_time + '.txt'

	for i in range(10):
		digit_key = 'digit' + str(i)
		digit_value = i
		# print('digit_key: {}'.format(digit_key))

		temp_indices = np.where(labels_arr == digit_value)[0]
		# concat_size = len(temp_indices)

		batch_data = (features_arr[temp_indices,:])[np.newaxis,:,:]
		# print('batch_data shape:{}'.format(batch_data.shape))

		temp_mean_features = np.mean(batch_data[0,:,:], axis=0).reshape((1,-1))

		temp_distributions = kde(batch_data, num_nodes=FLAGS.num_bins, sigma=0.1, batch_size=1, num_features=num_features)
		# print(temp_distributions.shape)

		with open(distributions_file_name, 'ab') as f_distributions_file:
			np.savetxt(f_distributions_file, temp_distributions, fmt='%5.3f', delimiter='\t')
		
		with open(mean_features_file_name, 'ab') as f_mean_features_file:
			np.savetxt(f_mean_features_file, temp_mean_features, fmt='%5.3f', delimiter='\t')

print('All distributions obtained!!!')
sys.exit()



