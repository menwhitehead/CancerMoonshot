import sys
import math
import numpy as np
import scipy.spatial.distance

def loadFeatures2(filename):
    features = {}
    f = open(filename, 'r')
    for line in f:
        values = line.split()
        features[values[0]] = map(float, values[1:])
    return features

def loadFeatures(filename):
    features = {}
    f = open(filename, 'r')
    for line in f:
        values = line.split()
        features[values[0]] = np.array(map(float, values[1:]))
    return features

def cosineSimilarity2(v1, v2):
    top = 0
    left = 0
    right = 0
    for i in range(len(v1)):
        top += v1[i] * v2[i]
        left += v1[i]**2
        right += v2[i]**2

    return top / math.sqrt(left * right)


def cosineSimilarity(v1, v2):
    return 1.0 - scipy.spatial.distance.cosine(v1, v2)

def euclideanDistance(v1, v2):
    return scipy.spatial.distance.euclidean(v1, v2)


def nearestNeighbors(v1, features, k=25):
	nearest = []
	for key in features:
		v2 = features[key]
		#print len(v1), len(v2)
		sim = cosineSimilarity(v1, v2)
		nearest.append((sim, key))
		nearest.sort(reverse=True)
		nearest = nearest[:k]

	return nearest


def addToFeature(v1, v2):
    for i in range(len(v1)):
        v1[i] += v2[i]

def add(v1, v2):
    result = []
    for i in range(len(v1)):
        result.append(v1[i] + v2[i])
    return result

def scalarMultiply(s, vec):
    result = []
    for i in range(len(vec)):
        result.append(vec[i] * s)
    return result



def sparseCosineSimilarity(m1, m2):
    top = 0
    left = 0
    right = 0
    for key in m1:
        if key in m2:
            top += m1[key] * m2[key]
        left += m1[key]**2
    for key in m2:
        if key not in m1:
            right += m2[key]**2

    bot = math.sqrt(left * right)
    if bot != 0:
        return top / bot
    else:
        return 0


def stringAverage(features, s):
    tokens = s.split()
    if len(tokens) == 0:
        return []

    running_sum = [0.0] * len(features.values()[0])
    for token in tokens[1:]:
        if token in features:
            addToFeature(running_sum, features[token])


    for i in range(len(running_sum)):
        running_sum[i] /= len(tokens)


    return running_sum

def stringSimilarity(features, s1, s2):
    sum1 = stringAverage(features, s1)
    sum2 = stringAverage(features, s2)
    return cosineSimilarity(sum1, sum2)



if __name__ == "__main__":
    filename = sys.argv[1]
    word_features = loadFeatures(filename)
    #print features['computer']
    #print cosineSimilarity(features['computer'], features['software'])
    print stringSimilarity(word_features, "the computer is a software machine", "the dog ate the grass")
    print stringSimilarity(word_features, "the computer is a software machine", "the processor has new hardware")
    print stringSimilarity(word_features, "the computer is a software machine", "chemical process")
    print stringSimilarity(word_features, "hydraulic mechanism", "water process")
