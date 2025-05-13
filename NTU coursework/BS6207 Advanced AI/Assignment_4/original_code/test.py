import numpy as np
import argparse
import os
from os import path
import sys
import itertools

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

from model import Keras_Model
from dataset_test import Dataset

def plot_confusion_matrix(cm, classes,
						  normalize=False,
						  title='Confusion matrix',
						  cmap=plt.cm.Blues):
	"""
	This function prints and plots the confusion matrix.
	Normalization can be applied by setting `normalize=True`.
	"""
	if normalize:
		cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
		print("Normalized confusion matrix")
	else:
		print('Confusion matrix, without normalization')

	# print(cm)

	plt.imshow(cm, interpolation='nearest', cmap=cmap)
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=0)
	plt.yticks(tick_marks, classes)

	fmt = '.3f' if normalize else 'd'
	thresh = cm.max() / 2.
	for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
		plt.text(j, i, format(cm[i, j], fmt),
				 horizontalalignment="center",
				 color="white" if cm[i, j] > thresh else "black")

	plt.ylabel('True label')
	plt.xlabel('Predicted label')
	plt.tight_layout()

parser = argparse.ArgumentParser(description='')

parser.add_argument('--model_dir', default='saved_models/', help='Directory to save models', dest='model_dir')
parser.add_argument('--metrics_files_dir', default='loss_data/', help='Text file to write step, loss, accuracy metrics', dest='metrics_files_dir')
parser.add_argument('--predictions_dir', default='predictions/', help='', dest='predictions_dir')
parser.add_argument('--patch_size', default='28', type=int, help='Patch size', dest='patch_size')
parser.add_argument('--num_instances', default='32', type=int, help='Number of patches to be concatenated', dest='num_instances')
parser.add_argument('--num_samples_per_class', type=int, help='Batch size', dest='num_samples_per_class')
parser.add_argument('--num_bins', default='11', type=int, help='Number of bins in kde layer', dest='num_bins')
parser.add_argument('--num_features', default='10', type=int, help='Number of features', dest='num_features')
parser.add_argument('--ucc_start', default='1', type=int, help='UOC start', dest='ucc_start')
parser.add_argument('--ucc_end', default='4', type=int, help='UOC end', dest='ucc_end')
parser.add_argument('--subset_length', default='10', type=int, help='Length of subset', dest='subset_length')
parser.add_argument('--dataset_type', default='test', help='', dest='dataset_type')
parser.add_argument('--description', help='', dest='description')

FLAGS = parser.parse_args()

class_names = ['ucc1','ucc2','ucc3','ucc4','ucc5','ucc6','ucc7','ucc8','ucc9','ucc10']
class_names = class_names[FLAGS.ucc_start - 1:FLAGS.ucc_end]

num_classes = FLAGS.ucc_end - FLAGS.ucc_start + 1

FLAGS.num_samples_per_class = int(40/num_classes)

batch_size = num_classes * FLAGS.num_samples_per_class

if FLAGS.description:
	description = FLAGS.description
else:
	print('Error: description is not given!!!')
	sys.exit()

num_batches = (252*20)//FLAGS.num_samples_per_class

metrics_files_dir = FLAGS.metrics_files_dir + description + '/'
saved_models_dir = FLAGS.model_dir + description + '/'

predictions_dir = FLAGS.predictions_dir + description + '/'
if not os.path.exists(predictions_dir):
	os.makedirs(predictions_dir)

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

	subset_elements_set = set(map(int, set(subset_elements_str)))
	subset_elements_arr = np.array(list(subset_elements_set))

	truth_labels_filename = predictions_dir + '{}_truth_labels'.format(FLAGS.dataset_type) + current_time + '.txt'
	predicted_labels_filename = predictions_dir + '{}_predicted_labels'.format(FLAGS.dataset_type) + current_time + '.txt'

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

	splitted_dataset = Dataset(num_instances=FLAGS.num_instances, num_samples_per_class=FLAGS.num_samples_per_class, digit_arr=subset_elements_arr, ucc_start=FLAGS.ucc_start, ucc_end=FLAGS.ucc_end)
	
	truth_labels_list = list()
	predicted_labels_list = list()
	for i in range(num_batches):
		print('Batch %d/%d' % (i+1,num_batches))

		test_batch = splitted_dataset.next_batch_test()

		batch_data = test_batch[0]
		batch_label =  np.argmax(test_batch[1],axis=1)

		truth_labels_list += list(batch_label)

		with open(truth_labels_filename,'ab') as f_truth_labels_filename:
			np.savetxt(f_truth_labels_filename, batch_label.reshape((-1,1)), fmt='%d', delimiter='\t')

		probs = model.predict_ucc_on_batch_data(batch_inputs=batch_data)
		# print('probs shape:{}'.format(probs.shape))

		predicted_labels = np.argmax(probs,axis=1)
		# print('predicted_labels shape:{}'.format(predicted_labels.shape))

		predicted_labels_list += list(predicted_labels)

		with open(predicted_labels_filename,'ab') as f_predicted_labels_filename:
			np.savetxt(f_predicted_labels_filename, predicted_labels.reshape((-1,1)), fmt='%d', delimiter='\t')

	truth_labels_arr = np.array(truth_labels_list)
	print('truth_labels_arr shape:{}'.format(truth_labels_arr.shape))

	predicted_labels_arr = np.array(predicted_labels_list)
	print('predicted_labels_arr shape:{}'.format(predicted_labels_arr.shape))

	conf_mat = confusion_matrix(truth_labels_arr, predicted_labels_arr)
	print('conf_mat shape:{}'.format(conf_mat.shape))

	conf_mat_filename = predictions_dir + '{}_confusion_matrix'.format(FLAGS.dataset_type) + current_time + '.txt'
	np.savetxt(conf_mat_filename, conf_mat, fmt='%d', delimiter='\t')

	ucc_acc = np.sum(conf_mat.diagonal())/np.sum(conf_mat)
	acc_filename = predictions_dir + '{}_ucc_acc'.format(FLAGS.dataset_type) + current_time + '.txt'
	np.savetxt(acc_filename, ucc_acc.reshape((-1,1)), fmt='%.4f', delimiter='\t')

	fig1 = plt.figure(figsize=(9,9))
	plot_confusion_matrix(conf_mat, classes=class_names, normalize=True, title='Confusion matrix')
	fig_filename = predictions_dir + '{}_confusion_matrix_normalized'.format(FLAGS.dataset_type) + current_time + '.png'
	fig1.savefig(fig_filename, bbox_inches='tight')

	fig2 = plt.figure(figsize=(9,9))
	plot_confusion_matrix(conf_mat, classes=class_names, normalize=False, title='Confusion matrix, without normalization')
	fig_filename = predictions_dir + '{}_confusion_matrix_unnormalized'.format(FLAGS.dataset_type) + current_time + '.png'
	fig2.savefig(fig_filename, bbox_inches='tight')

print('Test finished!!!')
sys.exit()


