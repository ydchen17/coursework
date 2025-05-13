import numpy as np
import fnmatch
import os
import keras
from keras.datasets import mnist
from keras import backend as K
from itertools import combinations


class Dataset(object):
	def __init__(self, num_instances=2, num_samples_per_class=16, digit_arr=None, ucc_start=1, ucc_end=10):
		
		self._num_instances = num_instances
		self._num_samples_per_class = num_samples_per_class
		self._digit_arr = digit_arr
		self._ucc_start = ucc_start
		self._ucc_end = ucc_end

		self._num_digits = len(self._digit_arr)

		self._num_classes = self._ucc_end - self._ucc_start + 1

		splitted_dataset = np.load('../../data/mnist/splitted_mnist_dataset.npz')

		x_test = splitted_dataset['x_test']
		y_test = splitted_dataset['y_test']

		del splitted_dataset

		x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)
		x_test = x_test.astype('float32')
		x_test /= 255
		x_test = (x_test-np.mean(x_test,axis=(1,2,3))[:,np.newaxis,np.newaxis,np.newaxis])/np.std(x_test,axis=(1,2,3))[:,np.newaxis,np.newaxis,np.newaxis]

		print('x_test shape:', x_test.shape)
		print(x_test.shape[0], 'test samples')
		print('y_test shape:', y_test.shape)

		self._x_test = x_test
		self._y_test = y_test

		self._digit_dict = self.get_digit_dict()
		self._class_dict_test = self.get_class_dict()

		self._labels = self.generate_labels()

	def get_digit_dict(self):
		digit_dict = dict()
		for i in range(self._num_digits):
			digit_key = 'digit' + str(i)
			digit_value = self._digit_arr[i]

			temp_digit_dict = dict()

			temp_digit_dict['value'] = digit_value
			temp_digit_dict['test_indices'] = np.where(self._y_test == digit_value)[0]
			temp_digit_dict['num_test'] = len(temp_digit_dict['test_indices'])

			print('{}:{}, num_test:{}'.format(digit_key,digit_value,temp_digit_dict['num_test']))

			digit_dict[digit_key] = temp_digit_dict

		return digit_dict


	def get_class_dict(self):
		elements_arr = np.arange(self._num_digits)
		class_dict = dict()
		for i in range(self._num_classes):
			class_key = 'class_' + str(i)

			temp_class_dict = dict()
			# print(elements_arr)
			elements_list = list()
			for j in combinations(elements_arr,i+self._ucc_start):
				elements_list.append(np.array(j))

			elements_array = np.array(elements_list)

			temp_class_dict['tuples_arr'] = elements_array
			temp_class_dict['num_tuples'] = len(temp_class_dict['tuples_arr'])
			temp_class_dict['index'] = 0

			# print(temp_class_dict['tuples_arr'].shape)
			# print('{}, num_tuples:{}'.format(class_key,temp_class_dict['num_tuples']))

			class_dict[class_key] = temp_class_dict

		return class_dict

	def one_hot_label(self, label):
		one_hot_label = np.zeros(self._num_classes,dtype=np.int)
		one_hot_label[label]=1
		return one_hot_label

	def generate_labels(self):
		labels_list = list()
		for i in range(self._num_classes):
			labels_list.append(self.one_hot_label(i))

		labels_arr = np.repeat(np.array(labels_list),self._num_samples_per_class,axis=0)
		# print(labels_arr)

		return labels_arr

	def get_sample_data_test(self, indices_arr):
		sample = np.array(self._x_test[indices_arr,:,:,:])
		# print('Sample shape:{}'.format(sample.shape))
		return sample

	def next_batch_test(self):
		indices_list = list()
		for i in range(self._num_classes):
			class_key = 'class_' + str(i)
			# print('class_key:{}'.format(class_key))
			for j in range(self._num_samples_per_class):
				ind = self._class_dict_test[class_key]['index']
				
				temp_elements = self._class_dict_test[class_key]['tuples_arr'][ind,:]

				num_elements = temp_elements.shape[0]

				num_instances_per_element = self._num_instances // num_elements
				remainder_size = self._num_instances % num_elements

				num_instances_arr = np.repeat(num_instances_per_element,num_elements)
				num_instances_arr[:remainder_size] += 1

				for k in range(num_elements):
					digit_key = 'digit' + str(temp_elements[k])

					num_instances = num_instances_arr[k]

					indices_list += list(self._digit_dict[digit_key]['test_indices'][:num_instances])

					np.random.shuffle(self._digit_dict[digit_key]['test_indices'])


				self._class_dict_test[class_key]['index'] += 1

				if self._class_dict_test[class_key]['index'] >= self._class_dict_test[class_key]['num_tuples']:
					self._class_dict_test[class_key]['index'] = 0

		
		indices_arr = np.array(indices_list)

		samples_arr = self.get_sample_data_test(indices_arr)

		samples_arr = np.reshape(samples_arr, (-1,self._num_instances,samples_arr.shape[1],samples_arr.shape[2],samples_arr.shape[3]))

		samples_arr = np.transpose(samples_arr,(1,0,2,3,4))

		samples = list(samples_arr)

		labels = self._labels

		return samples, labels











