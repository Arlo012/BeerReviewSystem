import time
import numpy as np
import sys
from scipy.sparse import *
from numpy import int8
from scipy import float16
import pickle
from LargeTextProcessor import Beer
from LargeTextProcessor import Review
from LargeTextProcessor import User
import Tkinter
import math


def Recommender(beerReviews):  #argument is a map of beer names to a list that is [beer name, rating]
	reviewThresholdString = "-T5"
	numberOfTopReviewers = 10
	numberOfTopBeers = 10

	beerMapFile = open("beerMap" + reviewThresholdString + ".pickle", 'r')
	matrixFile = open("userBeerReviewMatrix" + reviewThresholdString + ".pickle", 'r')
	beerMap = pickle.load(beerMapFile)
	userBeerReviewMatrix = pickle.load(matrixFile)

	userBeerArray = csr_matrix((1,len(beerMap)), dtype = int)

	iterator = iter(beerReviews)
	for iterator in beerReviews:
		currentBeer = beerReviews[iterator][0]
		print currentBeer
		index = beerMap[currentBeer].matrixIndex
		userBeerArray[0, index] = beerReviews[iterator][1]



	similarityArray = []
	magnitude1 = math.sqrt(userBeerArray.multiply(userBeerArray).sum())
	userBeerArray = userBeerArray.transpose()
	print magnitude1

	# print userBeerReviewMatrix.get_shape()[0]
	# nextuser = userBeerReviewMatrix.getrow(6543)
	# print nextuser

	for i in range(0, userBeerReviewMatrix.get_shape()[0]):
		nextUser = userBeerReviewMatrix.getrow(i)
		dot = nextUser*userBeerArray
		magnitude2 = math.sqrt(nextUser.multiply(nextUser).sum())
		similarity = dot[0,0]/magnitude1/magnitude2
		similarityArray.append(similarity)

	userBeerArray = userBeerArray.transpose()
	top = []
	topIndex = []

	for i in range(0, len(similarityArray)):
		if i < numberOfTopReviewers:
			top.append(similarityArray[i])
			topIndex.append(i)
		else:
			top.sort()
			if similarityArray[i] > top[0]:
				top[0] = similarityArray[i]
				topIndex.append(i)

	print top
	topIndex.reverse()
	topIndex = topIndex[0:numberOfTopReviewers]
	topIndex.sort()
	print topIndex

	topReviewRows = []

	for i in range(0, numberOfTopReviewers):
		topReviewRows.append(userBeerReviewMatrix.getrow(topIndex[i]))

	columnAverages = []
	topBeers = []
	topBeersIndex = []

	for i in range(0, userBeerReviewMatrix.get_shape()[1]):
		nextSum = 0
		for j in range(0, numberOfTopReviewers):
			nextSum = nextSum + topReviewRows[j][0,i]

		nextAverage = float(nextSum)/numberOfTopReviewers
		if nextAverage != 0:
			print nextAverage
		columnAverages.append(nextAverage)

		if i < numberOfTopBeers:
			topBeers.append(nextAverage)
			topBeersIndex.append(i)
		else:
			topBeers.sort()
			if (nextAverage > topBeers[0]) and (userBeerArray[0,i] == 0): 
				topBeers[0] = nextAverage
				topBeersIndex.append(i)

	topBeersIndex.reverse()
	topBeersIndex = topBeersIndex[0:numberOfTopBeers]
	topBeersIndex.sort()

	print topBeers
	print topBeersIndex

	recommendationList = []

	iterator = iter(beerMap)
	for iterator in beerMap:
		currentBeer = beerMap.get(iterator)
		if currentBeer.matrixIndex in topBeersIndex:
			print currentBeer.name
			recommendationList.append(currentBeer.name)


	return recommendationList

if __name__ == "__main__":
	recommender()