import numpy as np
import argparse

import os
import sys

from time import time
from sklearn import metrics
from sklearn.cluster import KMeans, SpectralClustering


def cluster(estimator=None, data=None):
	t0 = time()
	estimator.fit(data)
	predicted_clustering_labels = estimator.labels_

	return predicted_clustering_labels

parser = argparse.ArgumentParser(description='')

parser.add_argument('--model_dir', default='saved_models/', help='Directory to save models', dest='model_dir')
parser.add_argument('--metrics_files_dir', default='loss_data/', help='Text file to write step, loss, accuracy metrics', dest='metrics_files_dir')
parser.add_argument('--features_dir', default='extracted_features/', help='', dest='features_dir')
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

if FLAGS.clustering_type:
	print('clustering_type:{}'.format(FLAGS.clustering_type))
else:
	print('Error: clustering type is not given!!!')
	sys.exit()

splitted_dataset = np.load('../../data/mnist/splitted_mnist_dataset.npz')
truth_labels_arr = splitted_dataset['y_{}'.format(FLAGS.dataset_type)]
del splitted_dataset

metrics_files_dir = FLAGS.metrics_files_dir + description + '/'
saved_models_dir = FLAGS.model_dir + description + '/'
extracted_features_dir = FLAGS.features_dir + description + '/'

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

	features_file_name = extracted_features_dir + '{}_features'.format(FLAGS.dataset_type) + current_time + '.txt'
	features_arr = np.loadtxt(features_file_name, comments='#', delimiter='\t', dtype='float32')

	all_classes_arr = np.arange(10)

	# cluster all data
	num_clusters = len(all_classes_arr)

	if FLAGS.clustering_type =='nn':
		estimator = SpectralClustering(n_clusters=num_clusters, eigen_solver='arpack', affinity="nearest_neighbors")
	elif FLAGS.clustering_type =='kmeans':
		estimator = KMeans(n_clusters=num_clusters, init='k-means++', n_init=10)

	predicted_labels_arr = cluster(estimator=estimator, data=features_arr)

	predicted_labels_filename = clustering_dir + '{}_predicted_labels_{}'.format(FLAGS.dataset_type,FLAGS.clustering_type) + current_time + '.txt'
	np.savetxt(predicted_labels_filename, predicted_labels_arr.reshape((-1,1)), fmt='%d', delimiter='\t')
	

print('Clustering completed!!!')
sys.exit()



