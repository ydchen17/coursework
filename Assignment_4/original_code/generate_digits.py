import numpy as np
import argparse

import os
import sys
import matplotlib.pyplot as plt

from model import Keras_Model


parser = argparse.ArgumentParser(description='')

parser.add_argument('--model_dir', default='saved_models/', help='Directory to save models', dest='model_dir')
parser.add_argument('--metrics_files_dir', default='loss_data/', help='Text file to write step, loss, accuracy metrics', dest='metrics_files_dir')
parser.add_argument('--features_dir', default='extracted_features/', help='', dest='features_dir')
parser.add_argument('--generated_digits_dir', default='generated_digits/', help='', dest='generated_digits_dir')
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

batch_size = 4

if FLAGS.description:
	description = FLAGS.description
else:
	print('Error: description is not given!!!')
	sys.exit()

splitted_dataset = np.load('../../data/mnist/splitted_mnist_dataset.npz')

x_data_raw = splitted_dataset['x_{}'.format(FLAGS.dataset_type)]
y_data = splitted_dataset['y_{}'.format(FLAGS.dataset_type)]

del splitted_dataset

x_data_raw = x_data_raw.reshape(x_data_raw.shape[0], x_data_raw.shape[1], x_data_raw.shape[2], 1)
x_data_raw = x_data_raw.astype('float32')
x_data_norm = x_data_raw/255
x_data_mean = np.mean(x_data_norm,axis=(1,2,3))
x_data_std = np.std(x_data_norm,axis=(1,2,3))
x_data = (x_data_norm-x_data_mean[:,np.newaxis,np.newaxis,np.newaxis])/x_data_std[:,np.newaxis,np.newaxis,np.newaxis]

num_samples = x_data.shape[0]
num_batches = num_samples//batch_size
last_batch_size = int(num_samples%batch_size)

metrics_files_dir = FLAGS.metrics_files_dir + description + '/'
saved_models_dir = FLAGS.model_dir + description + '/'

extracted_features_dir = FLAGS.features_dir + description + '/'
if not os.path.exists(extracted_features_dir):
	os.makedirs(extracted_features_dir)

generated_digits_dir = FLAGS.generated_digits_dir + description + '/'
if not os.path.exists(generated_digits_dir):
	os.makedirs(generated_digits_dir)

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

	mean_features_file_name = extracted_features_dir + '{}_mean_features'.format(FLAGS.dataset_type) + current_time + '.txt'
	feature_arr = np.loadtxt(mean_features_file_name, comments='#', delimiter='\t', dtype='float')
	print('feature_arr.shape:{}'.format(feature_arr.shape))

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

	reconstructed_imgs = model.generate_image_from_feature(batch_inputs=feature_arr)

	fig,ax = plt.subplots(feature_arr.shape[0])
	for j in range(feature_arr.shape[0]):

		temp_reconstructed = reconstructed_imgs[j][:,:,0]

		print(np.mean(temp_reconstructed))
		print(np.std(temp_reconstructed))

		ax[j].imshow(temp_reconstructed,cmap='gray')
		ax[j].get_xaxis().set_visible(False)
		ax[j].get_yaxis().set_visible(False)

		# plt.figure()
		# plt.imshow(temp_reconstructed,cmap='gray')
		# plt.show()
	
	fig_filename = generated_digits_dir + '{}_generated_digits'.format(FLAGS.dataset_type) + current_time + '.png'
	fig.savefig(fig_filename, bbox_inches='tight')

	# plt.show()
	

print('Digit generation finished!!!')
sys.exit()


