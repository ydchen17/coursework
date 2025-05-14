import numpy as np
import argparse

import os
import sys

from model import Keras_Model


parser = argparse.ArgumentParser(description='')

parser.add_argument('--model_dir', default='saved_models/', help='Directory to save models', dest='model_dir')
parser.add_argument('--metrics_files_dir', default='loss_data/', help='Text file to write step, loss, accuracy metrics', dest='metrics_files_dir')
parser.add_argument('--features_dir', default='extracted_features/', help='', dest='features_dir')
parser.add_argument('--patch_size', default='28', type=int, help='Patch size', dest='patch_size')
parser.add_argument('--num_instances', default='32', type=int, help='Number of patches to be concatenated', dest='num_instances')
parser.add_argument('--num_bins', default='11', type=int, help='Number of bins in kde layer', dest='num_bins')
parser.add_argument('--num_features', default='10', type=int, help='Number of features', dest='num_features')
parser.add_argument('--ucc_start', default='1', type=int, help='UOC start', dest='ucc_start')
parser.add_argument('--ucc_end', default='4', type=int, help='UOC start', dest='ucc_end')
parser.add_argument('--subset_length', default='10', type=int, help='Length of subset', dest='subset_length')
parser.add_argument('--dataset_type', default='test', help='', dest='dataset_type')
parser.add_argument('--description', help='', dest='description')

FLAGS = parser.parse_args()

num_classes = FLAGS.ucc_end - FLAGS.ucc_start + 1

batch_size = 512

if FLAGS.description:
	description = FLAGS.description
else:
	print('Error: description is not given!!!')
	sys.exit()

splitted_dataset = np.load('../../data/mnist/splitted_mnist_dataset.npz')

x_data = splitted_dataset['x_{}'.format(FLAGS.dataset_type)]
y_data = splitted_dataset['y_{}'.format(FLAGS.dataset_type)]

del splitted_dataset

x_data = x_data.reshape(x_data.shape[0], x_data.shape[1], x_data.shape[2], 1)
x_data = x_data.astype('float32')
x_data /= 255
x_data = (x_data-np.mean(x_data,axis=(1,2,3))[:,np.newaxis,np.newaxis,np.newaxis])/np.std(x_data,axis=(1,2,3))[:,np.newaxis,np.newaxis,np.newaxis]

num_samples = x_data.shape[0]
num_batches = num_samples//batch_size
last_batch_size = int(num_samples%batch_size)

metrics_files_dir = FLAGS.metrics_files_dir + description + '/'
saved_models_dir = FLAGS.model_dir + description + '/'

extracted_features_dir = FLAGS.features_dir + description + '/'
if not os.path.exists(extracted_features_dir):
	os.makedirs(extracted_features_dir)

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

	labels_filename = extracted_features_dir + '{}_labels'.format(FLAGS.dataset_type) + current_time + '.txt'
	features_file_name = extracted_features_dir + '{}_features'.format(FLAGS.dataset_type) + current_time + '.txt'

	print('CNN model parameters:')
	print('patch_size = {}'.format(FLAGS.patch_size))
	print('subset_length = {}'.format(FLAGS.subset_length))
	print('num_classes = {}'.format(num_classes))
	print('batch_size = {}'.format(batch_size))

	model = Keras_Model(patch_size=FLAGS.patch_size, num_instances=FLAGS.num_instances, num_classes=num_classes, num_bins=FLAGS.num_bins, num_features=FLAGS.num_features, batch_size=batch_size)

	model_weights_file_path = saved_models_dir + model_weights_filename
	if os.path.isfile(model_weights_file_path):
		model.load_saved_weights(model_weights_file_path)
		print('weights loaded successfully!!!\nmodel_weights_filename: {}'.format(model_weights_file_path))
	else:
		print('Error: saved model weights file cannot be found!!!\nmodel_weights_filename: {}'.format(model_weights_file_path))
		sys.exit()

	for i in range(num_batches):
		print('Batch %d/%d' % (i,num_batches))

		batch_data = x_data[i*batch_size:(i+1)*batch_size]
		batch_label = y_data[i*batch_size:(i+1)*batch_size]

		features_out = model.predict_on_batch_data_patches(batch_inputs=batch_data)
		print('features_out shape:{}'.format(features_out.shape))

		# with open(labels_filename,'ab') as f_labels_file:
		# 	np.savetxt(f_labels_file, batch_label.reshape((-1,1)), fmt='%d', delimiter='\t')

		with open(features_file_name, 'ab') as f_features_file:
			np.savetxt(f_features_file, features_out.reshape((-1,FLAGS.num_features)), fmt='%5.3f', delimiter='\t')


	# last batch
	i += 1
	print('Batch %d/%d' % (i,num_batches))
	if last_batch_size != 0:
		batch_data = x_data[i*batch_size:]
		batch_label = y_data[i*batch_size:]

		features_out = model.predict_on_batch_data_patches(batch_inputs=batch_data)
		# print('features_out shape:{}'.format(features_out.shape))

		# with open(labels_filename,'ab') as f_labels_file:
		# 	np.savetxt(f_labels_file, batch_label.reshape((-1,1)), fmt='%d', delimiter='\t')

		with open(features_file_name, 'ab') as f_features_file:
			np.savetxt(f_features_file, features_out.reshape((-1,FLAGS.num_features)), fmt='%5.3f', delimiter='\t')


		

print('Feature extraction finished!!!')
sys.exit()


