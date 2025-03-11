from util import arff_to_df
from funcs import *
import pandas as pd
import matplotlib.pyplot as plt
import random
import math
import time

#Initialize
filename = input(".arff file for analysis: ")

df = arff_to_df(filename)
dfNormalized = normalizeDF(df)

k = user_parameter_choice(int, "Select a max number of clusters (default 6): ", "Number of clusters:", 6)
epsilon = user_parameter_choice(float, "Select a stopping parameter/epsilon (default 0.001): ", "Epsilon:", 0.001)
iterations = user_parameter_choice(int, "Select the number of iterations (default 100): ", "Iterations:", 100)

smallestDistances, optimalCentroids, kTimes, errorList = [], [], [], []
globalSmallestError, optimalCluster = -1, -1

errorList = []

#Repeat the process for each value of k
for clusterNums in range(1, k+1):
	print("code")
	start = time.time()

	smallestError = -1

	#Repeat the process arbitrarily, looking for the lowest error
	for i in range(iterations):

		#Select first seeds randomly
		seedSelection = dfNormalized.sample(clusterNums)
		seedSelection = seedSelection.reset_index(drop=True)

		oldError, currentError = -1, -2

		#Loop until finished
		while not oldError == currentError:
			oldError = currentError

			#distances is a list of dicts, each list representing a different k-cluster. 
			#Each dict has two keys: 'items' and 'distances'. 
			#Each item value is a row (point) that belongs to the current cluster. 
			#Each distance value is the distance from the item to the current centroid. The item is at the same index as its distance
			distances = [{"items": [], "distances": []} for i in range(clusterNums)]
			for index, item in dfNormalized.iterrows():
				smallestDistance = -1
				clusterIndex = 0

				#Loops through the clusters to find which centroid is closer to the current item
				for kindex, seedItem in seedSelection.iterrows():
					distance = getDistance(seedItem, item)
					if distance < smallestDistance or smallestDistance == -1:
						smallestDistance = distance
						clusterIndex = kindex 
				#Add item and distance data to appropriate cluster list
				distances[clusterIndex]['items'].append(item)
				distances[clusterIndex]['distances'].append(smallestDistance)

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
		if currentError < smallestError or smallestError == -1:
			if smallestError > -1 and smallestError - currentError <= epsilon:
				smallestError = currentError
				break
			else:
				smallestError = currentError

	#Update globalSmallestError
	if smallestError < globalSmallestError or globalSmallestError == -1:
		globalSmallestError = smallestError
		smallestDistances = distances
		optimalCentroids = seedSelection
		optimalCluster = clusterNums

	end = time.time()
	kTimes.append(end-start)
	errorList.append(smallestError)


print("\nGlobal error:", round(globalSmallestError, 4))

print("Optimal # of clusters:", optimalCluster)

for index, row in optimalCentroids.iterrows():
	print("\nCluster", index+1)
	for item in row.keys():
		print(item, row[item] * max(df[item]))
	print("Num Items:", len(smallestDistances[index]['items']), "(", round(len(smallestDistances[index]['items'])/len(df) * 100, 2),"%)")

print("\nTotal")
for header in df.columns:
	print(header, sum(df[header])/len(df[header]))
print("Num Items:", len(df), "(", len(df[header])/len(df[header]) * 100,"%)")

plt.plot(range(1, k+1), kTimes)
plt.xlim(1, k)
plt.xticks(range(1, k+1))
plt.xlabel("Clusters")
plt.ylim(0, math.ceil(max(kTimes))+2)
plt.ylabel("Runtime (seconds)")
plt.savefig("runtime.png")
plt.show()

plt.plot(range(1, k+1), errorList)
plt.xlim(1, k)
plt.xticks(range(1, k+1))
plt.xlabel("Clusters")
plt.ylim(0, math.ceil(max(errorList))+2)
plt.ylabel("Within Cluster Squared Error")
plt.savefig("clusters.png")
plt.show()
