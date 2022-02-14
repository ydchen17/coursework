import numpy as np
import argparse
import tensorflow as tf
from datetime import datetime
import os
import sys

from model import Keras_Model
from dataset import Dataset
from keras.models import load_model
import yaml
import time

parser = argparse.ArgumentParser(description='')

parser.add_argument('--model_dir', default='saved_models/', help='Directory to save models', dest='model_dir')
parser.add_argument('--init_model_file', help='Initial model file (optional)', dest='init_model_file')
parser.add_argument('--patch_size', default='28', type=int, help='Patch size', dest='patch_size')
parser.add_argument('--num_instances', default='32', type=int, help='Number of instances in a bag', dest='num_instances')
parser.add_argument('--ucc_start', default='1', type=int, help='ucc start', dest='ucc_start')
parser.add_argument('--ucc_end', default='4', type=int, help='ucc end', dest='ucc_end')
parser.add_argument('--subset_length', default='10', type=int, help='Length of subset', dest='subset_length')
parser.add_argument('--num_samples_per_class', type=int, help='', dest='num_samples_per_class')
parser.add_argument('--learning_rate', default='1e-4', type=float, help='', dest='learning_rate')
parser.add_argument('--num_bins', default='11', type=int, help='Number of bins in kde layer', dest='num_bins')
parser.add_argument('--num_features', default='10', type=int, help='Number of features', dest='num_features')
parser.add_argument('--num_steps', default=1000001, type=int, help='Number of steps of execution (default: 1000000)', dest='num_steps')
parser.add_argument('--save_interval', default=1000, type=int, help='Model save interval (default: 1000)', dest='save_interval')
parser.add_argument('--metrics_file', default='loss_data/', help='Text file to write step, loss, accuracy metrics', dest='metrics_file')
parser.add_argument('--description', help='', dest='description')

FLAGS = parser.parse_args()

num_classes = FLAGS.ucc_end - FLAGS.ucc_start + 1
FLAGS.num_samples_per_class = int(20/num_classes)

subsets_dict_obj = np.load("../../data/subsets/subsets.npy", allow_pickle=True)
subsets_arr = subsets_dict_obj.item().get('{}_element_subsets'.format(FLAGS.subset_length))

if FLAGS.description:
	description = FLAGS.description
else:
	description = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")

saved_models_file = FLAGS.metrics_file + 'saved_model_weights_filenames_{}_element_subsets__{}.txt'.format(FLAGS.subset_length, description)
with open(saved_models_file,'a') as f_saved_models_file:
	f_saved_models_file.write('#subset_elements_str\t#model_weights_filename\n')

if subsets_arr.shape[0]>5:
	first_k_subsets=5
else:
	first_k_subsets=subsets_arr.shape[0]

for s in range(first_k_subsets):
	subset_elements_arr = subsets_arr[s]

	subset_elements_str = ''.join(list(subset_elements_arr.astype('str')))

	current_time = datetime.now().strftime("__%Y_%m_%d__%H_%M_%S__") + subset_elements_str
	metrics_file = FLAGS.metrics_file + 'step_loss_acc_metrics' + current_time + '.txt'

	batch_size = num_classes * FLAGS.num_samples_per_class

	print('CNN model parameters:')
	print('patch_size = {}'.format(FLAGS.patch_size))
	print('num_instances = {}'.format(FLAGS.num_instances))
	print('num_features = {}'.format(FLAGS.num_features))
	print('batch_size = {}'.format(batch_size))
	print('num_samples_per_class = {}'.format(FLAGS.num_samples_per_class))
	print('num_classes = {}'.format(num_classes))
	print('subset_length = {}'.format(FLAGS.subset_length))
	print('ucc_start = {}'.format(FLAGS.ucc_start))
	print('ucc_end = {}'.format(FLAGS.ucc_end))
	print('learning_rate = {}'.format(FLAGS.learning_rate))
	print('num_steps = {}'.format(FLAGS.num_steps))
	print('metrics_file = {}'.format(metrics_file))
	print('init_model_file = {}'.format(FLAGS.init_model_file))

	model = Keras_Model(patch_size=FLAGS.patch_size, num_instances=FLAGS.num_instances, num_classes=num_classes, learning_rate=FLAGS.learning_rate, num_bins=FLAGS.num_bins, num_features=FLAGS.num_features, batch_size=batch_size)

	if FLAGS.init_model_file:
		if os.path.isfile(FLAGS.init_model_file):
			model.load_saved_weights(FLAGS.init_model_file)
			print('weights loaded successfully!!!')
			print(FLAGS.init_model_file)


	model_yaml_filename = FLAGS.model_dir + "model_summary" + current_time + '.yaml'
	with open(model_yaml_filename, 'w') as f_model_yaml_filename:
		yaml.dump(model.yaml_file, f_model_yaml_filename)


	splitted_dataset = Dataset(num_instances=FLAGS.num_instances, num_samples_per_class=FLAGS.num_samples_per_class, digit_arr=subset_elements_arr, ucc_start=FLAGS.ucc_start, ucc_end=FLAGS.ucc_end)

	with open(metrics_file,'a') as f_metric_file:
		f_metric_file.write('# CNN model parameters:\n')
		f_metric_file.write('# patch_size = {}\n'.format(FLAGS.patch_size))
		f_metric_file.write('# num_instances = {}\n'.format(FLAGS.num_instances))
		f_metric_file.write('# num_features = {}\n'.format(FLAGS.num_features))
		f_metric_file.write('# batch_size = {}\n'.format(batch_size))
		f_metric_file.write('# num_samples_per_class = {}\n'.format(FLAGS.num_samples_per_class))
		f_metric_file.write('# num_classes = {}\n'.format(num_classes))
		f_metric_file.write('# subset_length = {}\n'.format(FLAGS.subset_length))
		f_metric_file.write('# ucc_start = {}\n'.format(FLAGS.ucc_start))
		f_metric_file.write('# ucc_end = {}\n'.format(FLAGS.ucc_end))
		f_metric_file.write('# learning_rate = {}\n'.format(FLAGS.learning_rate))
		f_metric_file.write('# num_steps = {}\n'.format(FLAGS.num_steps))
		f_metric_file.write('# save_interval = {}\n'.format(FLAGS.save_interval))
		f_metric_file.write('# metrics_file = {}\n'.format(metrics_file))
		f_metric_file.write('# init_model_file = {}\n'.format(FLAGS.init_model_file))
		f_metric_file.write('# step\ttrain_ucc_acc\ttrain_ucc_loss\tval_ucc_acc\tval_ucc_loss\ttrain_ae_loss\tval_ae_loss\ttrain_loss_weighted\tval_loss_weighted\n')

	for i in range(FLAGS.num_steps):

		train_batch = splitted_dataset.next_batch_train()

		[train_loss_weighted, train_ucc_loss, train_ae_loss, train_ucc_acc, train_ae_acc] = model.train_on_batch_data(batch_inputs=train_batch[0], batch_outputs=train_batch[1])

		if i<1000:
			if i % 100 == 0:
				if i != 0:
					model_weights_filename = FLAGS.model_dir + "model_weights" + current_time + '__' + str(i) + ".h5"
					model.save_model_weights(model_weight_save_path=model_weights_filename)
					with open(saved_models_file,'a') as f_saved_models_file:
						f_saved_models_file.write('{}\t{}\n'.format(subset_elements_str,model_weights_filename))
					print("Model weights saved in file: ", model_weights_filename)

		if i % FLAGS.save_interval == 0:
			if i != 0:
				model_weights_filename = FLAGS.model_dir + "model_weights" + current_time + '__' + str(i) + ".h5"
				model.save_model_weights(model_weight_save_path=model_weights_filename)
				with open(saved_models_file,'a') as f_saved_models_file:
					f_saved_models_file.write('{}\t{}\n'.format(subset_elements_str,model_weights_filename))
				print("Model weights saved in file: ", model_weights_filename)

		if i % 10 == 0:
			val_batch = splitted_dataset.next_batch_val()

			[val_loss_weighted, val_ucc_loss, val_ae_loss, val_ucc_acc, val_ae_acc] = model.test_on_batch_data(batch_inputs=val_batch[0], batch_outputs=val_batch[1])
						
			print('Subset=%s, Step=%d ### training: weighted_loss=%5.3f, ucc_acc=%5.3f, ucc_loss=%5.3f, ae_loss=%5.3f ### validation: weighted_loss=%5.3f, ucc_acc=%5.3f, ucc_loss=%5.3f, ae_loss=%5.3f' % (subset_elements_str, i, train_loss_weighted, train_ucc_acc, train_ucc_loss, train_ae_loss, val_loss_weighted, val_ucc_acc, val_ucc_loss, val_ae_loss))

			with open(metrics_file,'a') as f_metric_file:
				f_metric_file.write('%d\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\n' % (i, train_ucc_acc, train_ucc_loss, val_ucc_acc, val_ucc_loss, train_ae_loss, val_ae_loss, train_loss_weighted, val_loss_weighted))


	print('Training finished!!!')
	model_weights_filename = FLAGS.model_dir + "model_weights" + current_time + '__' + str(i) + ".h5"
	model.save_model_weights(model_weight_save_path=model_weights_filename)
	print("Model weights saved in file: ", model_weights_filename)

	with open(saved_models_file,'a') as f_saved_models_file:
		f_saved_models_file.write('{}\t{}\n'.format(subset_elements_str,model_weights_filename))


