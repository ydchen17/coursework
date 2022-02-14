import numpy as np
import argparse

import os
import sys
import matplotlib.pyplot as plt

import itertools

def js_divergence(p,q):
	m = 0.5*(p+q)
	log_p_over_m = np.log2(p/m)
	log_q_over_m = np.log2(q/m)

	return 0.5*np.sum(p*log_p_over_m) + 0.5*np.sum(q*log_q_over_m)



parser = argparse.ArgumentParser(description='')

parser.add_argument('--metrics_files_dir', default='loss_data/', help='Text file to write step, loss, accuracy metrics', dest='metrics_files_dir')
parser.add_argument('--distributions_dir', default='distributions/', help='', dest='distributions_dir')
parser.add_argument('--subset_length', default='10', type=int, help='Length of subset', dest='subset_length')
parser.add_argument('--num_bins', default='11', type=int, help='Number of bins in kde layer', dest='num_bins')
parser.add_argument('--dataset_type', default='test', help='', dest='dataset_type')
parser.add_argument('--description', help='', dest='description')

FLAGS = parser.parse_args()

if FLAGS.description:
	description = FLAGS.description
else:
	print('Error: description is not given!!!')
	sys.exit()


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
	# print(current_time)

	distributions_file_name = distributions_dir + '{}_distributions'.format(FLAGS.dataset_type) + current_time + '.txt'
	distributions_arr = np.loadtxt(distributions_file_name, comments='#', delimiter='\t', dtype='float32')

	num_features = distributions_arr.shape[1]/FLAGS.num_bins

	distributions_arr /= num_features

	js_divergence_arr = np.zeros((10,10))
	for i in range(10):
		p = np.clip(distributions_arr[i,:],1e-12,1)
		for k in range(i,10):
			q = np.clip(distributions_arr[k,:],1e-12,1)
			js_divergence_arr[i,k] = js_divergence(p,q)
			js_divergence_arr[k,i] = js_divergence_arr[i,k]

	print('JS divergence: min={:.2f} - max={:.3f} - mean={:.3f} - std={:.3f}'.format(np.amin(js_divergence_arr[js_divergence_arr>0]),np.amax(js_divergence_arr),np.mean(js_divergence_arr),np.std(js_divergence_arr)))

	js_divergence_filename = distributions_dir + '{}_JS_divergence'.format(FLAGS.dataset_type) + current_time + '.txt'
	np.savetxt(js_divergence_filename, js_divergence_arr, fmt='%.3f', delimiter='\t', comments='# ')

	fig = plt.figure(figsize=(10,9))

	plt.imshow(js_divergence_arr, interpolation='nearest', cmap=plt.cm.Blues, vmin=0, vmax=1 )
	plt.title('$D_{\mathcal{JS}}(\mathcal{P}||\mathcal{Q})$')
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=0)
	plt.yticks(tick_marks, classes)

	fmt = '.3f'
	for m, n in itertools.product(range(js_divergence_arr.shape[0]), range(js_divergence_arr.shape[1])):
		plt.text(n, m, format(js_divergence_arr[m, n], fmt),
				 horizontalalignment="center",
				 color="black")

	plt.ylabel('$\mathcal{P}$')
	plt.xlabel('$\mathcal{Q}$')

	fig.tight_layout()
	fig_filename = distributions_dir + '{}_JS_divergence'.format(FLAGS.dataset_type) + current_time + '.png'
	fig.savefig(fig_filename, bbox_inches='tight')
	
	# plt.show()

	del fig

print('All JS divergence values calculated!!!')
sys.exit()



