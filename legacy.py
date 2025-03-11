"""
!!! code from before the merge !!!


from util import arff_to_df
from funcs import *
import random
import pandas as pd
import matplotlib.pyplot as plt
import math

import matplotlib.pyplot as plot
import numpy as np

# True: save graphs, False: don't save them
VERBOSE = True

#Initialize

# clusters
k = user_parameter_choice(int, "Choose a number of clusters (default 2): ", "Number of clusters is:", default=2)
# iterations
iterations = user_parameter_choice(int, "Choose a number of iterations (default 100): ", "Number of iterations is:", default=100)
# epsilon (stopping value)
e = user_parameter_choice(float, "Choose a stopping value/epsilon (default 0.00001): ", "Stopping value is:", default=0.00001)

df = arff_to_df('continuous_fruitfly.arff')
dfNormalized = normalizeDF(df)

k = 3
epsilon = 0.5
iterations = 10

best_dist = None
best_selection = None
best_errors = []

#Repeat the process arbitrarily, looking for the lowest error
for i in range(iterations):

	errors = []

errorList = []

#Repeat the process for each value of k
for clusterNums in range(k):

	#Loop until finished
	# changed `oldError == currentError` -> `abs(oldError - currentError) > e` to allow stopping if change is less than the minimum desired change
	while abs(oldError - currentError) > e:
		oldError = currentError

	#Repeat the process arbitrarily, looking for the lowest error
	for i in range(iterations):

		#Select first seeds randomly
		seedSelection = dfNormalized.sample(k)
		seedSelection = seedSelection.reset_index(drop=True)

			#Add item and distance data to appropriate cluster list
			distances[clusterIndex]['items'].append(item)
			# should append smallest distance
			distances[clusterIndex]['distances'].append(smallestDistance)

		#Get error
		currentError = getSquaredError(distances)
		errors.append(currentError)

			#distances is a list of dicts, each list representing a different k-cluster. 
			#Each dict has two keys: 'items' and 'distances'. 
			#Each item value is a row (point) that belongs to the current cluster. 
			#Each distance value is the distance from the item to the current centroid. The item is at the same index as its distance
			distances = [{"items": [], "distances": []} for i in range(k)]
			for index, item in dfNormalized.iterrows():
				smallestDistance = -1
				clusterIndex = 0

				#Loops through the clusters to find which centroid is closer to the current item
				for kindex, seedItem in seedSelection.iterrows():
					distance = getSquaredDistance(seedItem, item)
					if distance < smallestDistance or smallestDistance == -1:
						smallestDistance = distance
						clusterIndex = kindex 

	#Update smallestError
	print("Current error:", round(currentError, 4))
	if currentError < smallestError or smallestError == -1:
		smallestError = currentError
		best_dist = distances.copy()
		best_selection = seedSelection.copy()
		best_errors = errors.copy()
		

			#Get error
			currentError = getSquaredError(distances)

			#Compute new centroids
			newCentroids = []
			for cluster in distances:
				newCentroids.append(getCentroid(cluster['items']))

for index, row in seedSelection.iterrows():
	print("\nCluster", index, ":\nTHORAX", row['THORAX'] * max(df['THORAX']), "\nSLEEP", row['SLEEP'] * max(df['SLEEP']), "\nclass", row['class'] * max(df['class']))

if VERBOSE:
	plot.figure()
	plot.plot(range(len(best_errors)), best_errors, marker='o')
	plot.xlabel('Iteration')
	plot.ylabel('Squared Error')
	plot.title(f'Error Convergence with K of {k} and Iterations of {iterations}')
	plot.savefig(f'error_graph_k={k}_i={iterations}_e={e}.png')
	plot.close()

	plot.figure()
	colors = plot.cm.rainbow(np.linspace(0, 1, k))
	for clusterIndex, cluster in enumerate(best_dist):
		cluster_items = cluster['items']
		x = [item['THORAX'] for item in cluster_items]
		y = [item['SLEEP'] for item in cluster_items]
		plot.scatter(x, y, color=colors[clusterIndex], label=f'Cluster {clusterIndex}', alpha=0.6)

	plot.scatter(best_selection['THORAX'], best_selection['SLEEP'],
				color='black', marker='x', s=100, label='Centroids')
	plot.xlabel('THORAX (normalized)')
	plot.ylabel('SLEEP (normalized)')
	plot.title(f'Clusters with K of {k} and Iterations of {iterations}')
	plot.legend()
	plot.savefig(f'clusters_k={k}_i={iterations}_e={e}.png')
	plot.close()
"""