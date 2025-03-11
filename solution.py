from util import arff_to_df
from funcs import *
import random
import pandas as pd

#Initialize
k = 2
df = arff_to_df('continuous_fruitfly.arff')

dfNormalized = normalizeDF(df)

smallestError = -1
	#Fruitfly dataset convergence values:
	#k=1   ->   72618
	#k=2   ->   74414 (1000 iterations)
	#k=3   ->   73418 (1000 iterations)

#Repeat the process arbitrarily, looking for the lowest error
for i in range(10):

	#Select first seeds randomly
	seedSelection = dfNormalized.sample(k)
	seedSelection = seedSelection.reset_index(drop=True)

	oldError, currentError = -1, -2

	#Loop until finished
	while not oldError == currentError:
		oldError = currentError

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
		for index, key in enumerate(dfNormalized.keys()):
			newSeedDF[key] = [newCentroids[i][index] for i in range(len(newCentroids))]
		seedSelection = pd.DataFrame(newSeedDF)

	#Update smallestError
	print("Current error:", round(currentError, 4))
	if currentError < smallestError or smallestError == -1:
		smallestError = currentError

print("Global error:", round(smallestError, 4))

print(len(distances[1]['items']))
for index, row in seedSelection.iterrows():
	print("\nCluster", index)
	for item in row.keys():
		print(item, row[item] * max(df[item]))
	print("Num Items:", len(distances[index]['items']), "(", len(distances[index]['items'])/len(df) * 100,"%)")

print("\nTotal")
for header in df.columns:
	print(header, sum(df[header])/len(df[header]))
print("Num Items:", len(df), "(", len(df[header])/len(df[header]) * 100,"%)")

# print("\nTotal:\nTHORAX", sum(df['THORAX'])/len(df['THORAX']), "\nSLEEP", sum(df['SLEEP'])/len(df['SLEEP']), "\nclass", sum(df['class'])/len(df['class']))