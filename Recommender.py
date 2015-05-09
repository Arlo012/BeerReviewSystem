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

	userBeerArray = csr_matrix((1,len(beerMap)), dtype = int)  #your rating of all the beers

	iterator = iter(beerReviews)
	for iterator in beerReviews:
		currentBeer = beerReviews[iterator][0]
		print currentBeer
		index = beerMap[currentBeer].matrixIndex
		userBeerArray[0, index] = beerReviews[iterator][1]



	similarityArray = []		#an array of your similarity to each other user in the correct indexing order
	magnitude1 = math.sqrt(userBeerArray.multiply(userBeerArray).sum())  #Your Magnitude
	userBeerArray = userBeerArray.transpose()		#Transpose so that this array can be dot producted
	print magnitude1

	# print userBeerReviewMatrix.get_shape()[0]
	# nextuser = userBeerReviewMatrix.getrow(6543)
	# print nextuser

	for i in range(0, userBeerReviewMatrix.get_shape()[0]):  #iterate through every user
		nextUser = userBeerReviewMatrix.getrow(i)			#each row represents a user
		dot = nextUser*userBeerArray						#dot you with every other user
		magnitude2 = math.sqrt(nextUser.multiply(nextUser).sum())		#getting the user's magnitude
		similarity = dot[0,0]/magnitude1/magnitude2			#Finding the cosine similarity with this user
		similarityArray.append(similarity)					#add it to the list

	userBeerArray = userBeerArray.transpose()		#untranspose from before
	top = []				#This array will contain the similarity of the top ten people
	topIndex = []			#this array of the top indexes

	for i in range(0, len(similarityArray)):			#cycle through all the users
		if i < numberOfTopReviewers:					#for the first 10 or so people
			top.append(similarityArray[i])				
			topIndex.append(i)
		else:
			top.sort()									#sort the top similarity
			if similarityArray[i] > top[0]:				#if my next value is greater than the smallest value in the list
				top[0] = similarityArray[i]				#replace the smallest value with the greater value
				topIndex.append(i)						#add this to the list of top indexes

	print top
	topIndex.reverse()
	topIndex = topIndex[0:numberOfTopReviewers]			#finds the top ten indexes for people
	topIndex.sort()
	print topIndex

	topReviewRows = []				#stores a list of sparse arrays that contain the top ten most similar users beer reviews

	for i in range(0, numberOfTopReviewers):				#get the rows that I need
		topReviewRows.append(userBeerReviewMatrix.getrow(topIndex[i]))

	columnAverages = []
	topBeers = []
	topBeersIndex = []

	for i in range(0, userBeerReviewMatrix.get_shape()[1]):			#A loop to calculate the average rating of the beers
		nextSum = 0
		nonZeroReviewCount = 0
		for j in range(0, numberOfTopReviewers):
			if topReviewRows[j][0,i] != 0:
				nextSum = nextSum + topReviewRows[j][0,i]
				nonZeroReviewCount += 1
		if nonZeroReviewCount != 0:
			nextAverage = float(nextSum)/nonZeroReviewCount		#average review of the current Beer
		else:
			nextAverage = 0		
		if nextAverage != 0:
			print nextAverage
		columnAverages.append(nextAverage)

		if i < numberOfTopBeers:							#finds the top ten Beers
			topBeers.append(nextAverage)					#for the first couple people...
			topBeersIndex.append(i)
		else:												#for the rest...same algorithm as with finding the top 10 people
			topBeers.sort()
			if (nextAverage > topBeers[0]) and (userBeerArray[0,i] == 0):   #also checks if beer is already in your list of reviewed beers
				topBeers[0] = nextAverage
				topBeersIndex.append(i)

	topBeersIndex.reverse()							#same as above
	topBeersIndex = topBeersIndex[0:numberOfTopBeers]
	topBeersIndex.sort()

	print topBeers
	print topBeersIndex

	recommendationList = []			#returns the list of the top recommendations

	iterator = iter(beerMap)
	for iterator in beerMap:
		currentBeer = beerMap.get(iterator)
		if currentBeer.matrixIndex in topBeersIndex:
			print currentBeer.name
			recommendationList.append(currentBeer.name)				#finds the name rather than the index of the beer


	return recommendationList

if __name__ == "__main__":
	recommender()