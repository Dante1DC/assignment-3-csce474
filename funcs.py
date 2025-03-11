import math

def getDistance(origin, item):
	total_distance = 0

	#For each attribute, find the squared difference to the origin and add to the total
	for attribute in origin.index:
		attribute_diff = (float(origin[attribute]) - float(item[attribute]))**2
		total_distance += attribute_diff
	return math.sqrt(total_distance)

def getSquaredError(distance_array):
	total_error = 0

	#Loop through distance values and square them to get error values
	for cluster in distance_array:
		cluster_error = 0
		for distance in cluster['distances']:
			cluster_error += distance**2
		total_error += cluster_error
	return total_error

def getCentroid(items):
	numAttributes = len(items[0])
	totalAttributes = [[] for i in range(numAttributes)]

	#For each item in this cluster, aggregate their values to each attribute's total
	for item in items:
		for index, attribute in enumerate(item):
			totalAttributes[index].append(float(attribute))

	#Find average values for each attribute's list of values
	totalMean = [0] * numAttributes
	for index, attribute in enumerate(totalAttributes):
		totalMean[index] = sum(attribute)/len(attribute)

	return totalMean

def normalizeDF(df):
	newDF = df.copy()
	for attribute in df:
		itemRow = df[attribute]
		minValue = float(min(itemRow))
		maxValue = float(max(itemRow))
		itemArray = []
		for item in df[attribute]:
			itemArray.append((float(item)-minValue)/(maxValue-minValue))
		newDF[attribute] = itemArray
	return newDF