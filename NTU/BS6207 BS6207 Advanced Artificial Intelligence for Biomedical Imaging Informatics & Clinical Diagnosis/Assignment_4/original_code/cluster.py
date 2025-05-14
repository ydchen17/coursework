import numpy as np
import argparse

import os
import sys

from time import time
from sklearn import metrics
from sklearn.cluster import KMeans, SpectralClustering


def cluster(estimator=None, name=None, data=None, labels=None):
	t0 = time()
	estimator.fit(data)
	homogeneity_score = metrics.homogeneity_score(labels, estimator.labels_)
	completeness_score = metrics.completeness_score(labels, estimator.labels_)
	v_measure_score = metrics.v_measure_score(labels, estimator.labels_)
	adjusted_rand_score = metrics.adjusted_rand_score(labels, estimator.labels_)
	adjusted_mutual_info_score = metrics.adjusted_mutual_info_score(labels,  estimator.labels_)

	print('%-9s\t%.2fs\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'% (name,
														(time() - t0),
														homogeneity_score,
														completeness_score,
														v_measure_score,
														adjusted_rand_score,
														adjusted_mutual_info_score))

	clustering_scores = np.array([homogeneity_score, completeness_score, v_measure_score, adjusted_rand_score, adjusted_mutual_info_score]).reshape((1,-1))
	return clustering_scores

parser = argparse.ArgumentParser(description='')

parser.add_argument('--model_dir', default='saved_models/', help='Directory to save models', dest='model_dir')
parser.add_argument('--metrics_files_dir', default='loss_data/', help='Text file to write step, loss, accuracy metrics', dest='metrics_files_dir')
parser.add_argument('--features_dir', default='extracted_features/', help='', dest='features_dir')
parser.add_argument('--clustering_dir', default='clustering/', help='', dest='clustering_dir')
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

clustering_dir = FLAGS.clustering_dir + description + '/'
if not os.path.exists(clustering_dir):
	os.makedirs(clustering_dir)

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

	all_classes_arr = np.arange(10)

	clustering_file_name = clustering_dir + '{}_clustering'.format(FLAGS.dataset_type) + current_time + '.txt'
	with open(clustering_file_name, 'ab') as f_clustering_file:
		np.savetxt(	f_clustering_file, 
					np.array([	'#row order:',
								'all_spectral_nn','all_kmeans++']).reshape((1,-1)),
					fmt='%s', delimiter='\t')
		np.savetxt(	f_clustering_file, 
					np.array(['#homogeneity_score', 'completeness_score', 'v_measure_score', 'adjusted_rand_score', 'adjusted_mutual_info_score']).reshape((1,-1)),
					fmt='%s', delimiter='\t')

	print('init\t\ttime\thomo\tcompl\tv-meas\tARI\tAMI')

	# cluster all data
	num_clusters = len(all_classes_arr)
	estimator = SpectralClustering(n_clusters=num_clusters, eigen_solver='arpack', affinity="nearest_neighbors")
	clustering_scores = cluster(estimator=estimator, name='all: spectral-nn', data=features_arr, labels=labels_arr)
	with open(clustering_file_name, 'ab') as f_clustering_file:
		np.savetxt(f_clustering_file, clustering_scores, fmt='%5.3f', delimiter='\t')

	estimator = KMeans(n_clusters=num_clusters, init='k-means++', n_init=10)
	clustering_scores = cluster(estimator=estimator, name='all: kmeans++', data=features_arr, labels=labels_arr)
	with open(clustering_file_name, 'ab') as f_clustering_file:
		np.savetxt(f_clustering_file, clustering_scores, fmt='%5.3f', delimiter='\t')

print('Clustering completed!!!')
sys.exit()



