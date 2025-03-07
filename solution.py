from util import arff_to_df
from funcs import *
import random
import pandas as pd

#Initialize
k = 2
df = arff_to_df('fruitfly.arff')
smallestError = -1
	#Fruitfly dataset convergence values:
	#k=1   ->   72618
	#k=2   ->   74414 (1000 iterations)
	#k=3   ->   73418 (1000 iterations)

#Repeat the process arbitrarily, looking for the lowest error
for i in range(1000):

	#Select first seeds randomly
	randomSelection = df.sample(k)
	randomSelection = randomSelection.reset_index(drop=True)

	oldError, currentError = -1, -2

	#Loop until finished
	while not oldError == currentError:
		oldError = currentError

		#distances is a list of dicts, each list representing a different k-cluster. 
		#Each dict has two keys: 'items' and 'distances'. 
		#Each item value is a row (point) that belongs to the current cluster. 
		#Each distance value is the distance from the item to the current centroid. The item is at the same index as its distance
		distances = [{"items": [], "distances": []} for i in range(k)]
		for index, item in df.iterrows():
			smallestDistance = -1
			clusterIndex = 0

			#Loops through the clusters to find which distance to the current item is smaller
			for kindex, seedItem in randomSelection.iterrows():
				distance = getSquaredDistance(seedItem, item)
				if distance < smallestDistance or smallestDistance == -1:
					smallestDistance = distance
					clusterIndex = kindex 

			#Add item and distance data to appropriate cluster list
			distances[clusterIndex]['items'].append(item)
			distances[clusterIndex]['distances'].append(distance)

		#Get error
		currentError = getSquaredError(distances)

		#Compute new centroids
		newCentroids = []
		for cluster in distances:
			newCentroids.append(getCentroid(cluster['items']))

		#Convert centroids to DataFrame format for next iteration
		newSeedDF = {}
		for index, key in enumerate(df.keys()):
			newSeedDF[key] = [newCentroids[i][index] for i in range(len(newCentroids))]
		randomSelection = pd.DataFrame(newSeedDF)

	#Update smallestError
	print("Current error:", int(currentError))
	if currentError < smallestError or smallestError == -1:
		smallestError = currentError

print("Global error:", int(smallestError))