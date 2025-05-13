#!/bin/bash

array=( "2019_09_05__18_43_15__128000" )


for i in "${array[@]}"
do
	DESCRIPTION=$i
	echo $DESCRIPTION

	echo "test.py"
	python3 test.py --description $DESCRIPTION

	echo "extract_features.py"
	python3 extract_features.py --description $DESCRIPTION

	echo "obtain_distributions.py"
	python3 obtain_distributions.py --description $DESCRIPTION

	echo "visualize_distributions.py"
	python3 visualize_distributions.py --description $DESCRIPTION

	echo "generate_digits.py"
	python3 generate_digits.py --description $DESCRIPTION

	echo "calculate_js_divergence.py"
	python3 calculate_js_divergence.py --description $DESCRIPTION

	echo "cluster.py"
	python3 cluster.py --description $DESCRIPTION

	echo "obtain_clustering_labels.py"
	python3 obtain_clustering_labels.py --description $DESCRIPTION --clustering_type kmeans

	echo "calculate_clustering_accuracy.py"
	python3 calculate_clustering_accuracy.py --description $DESCRIPTION --clustering_type kmeans

	echo "obtain_clustering_labels.py"
	python3 obtain_clustering_labels.py --description $DESCRIPTION --clustering_type nn

	echo "calculate_clustering_accuracy.py"
	python3 calculate_clustering_accuracy.py --description $DESCRIPTION --clustering_type nn
done


