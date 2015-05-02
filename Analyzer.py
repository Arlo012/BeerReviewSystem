import time
import numpy as np
import sys
from scipy.sparse import *
from numpy import int8
from scipy import float16
import pickle

calculateSimilarityMatrix = False		#Re-calculate similarity matrix from user-beer-review sparse matrix?
repickleSimilarityMatrix = False		#Over-write similarity matrix? Note it is a BIG file... (~1.5gb)
reviewThresholdString = "-T25"				#File extension for review threshold (set in largeTextProcessor), #=num reviews

if calculateSimilarityMatrix:
	if repickleSimilarityMatrix:
		print '[WARNING] This is a TEST run! The output will not be pickled.'
	
	# Open the serialized user-beer review sparse array from pickled file
	try:
		print '[INFO] Reading serialized (PICKLED!) user-beer-review matrix.....'
		file = open("userBeerReviewMatrix" + reviewThresholdString + ".pickle", 'r')
		userBeerReviewMatrix = pickle.load(file)
		print '[INFO] Successfully opened pickled user-beer-review matrix!'
	except Exception as e:
		print '[ERROR] Opening pickled file failed!: ' + str(e)

	#Calculate/load magnitude vector
	rowMagnitudes = []
	print '\n[INFO] Calculating magnitude vectors.....'
	for i in range(0, userBeerReviewMatrix.shape[0]):
		row = userBeerReviewMatrix.getrow(i)
		multiplied = row.multiply(row)
		sum = multiplied.sum()
		magnitude = sum ** 0.5
		if magnitude == 0:
			print
			print '[ERROR] Zero magnitude user review row detected. VECTOR INCOMPLETE!'
			break
		else:
			rowMagnitudes.append(magnitude)
		
		#Progress bar lifted from http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
		if i % int(0.01*userBeerReviewMatrix.shape[0]) == 0:
			bar_length = 100
			percent = float(i) / userBeerReviewMatrix.shape[0]
			hashes = '#' * int(round(percent * bar_length))
			spaces = ' ' * (bar_length - len(hashes))
			sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
			sys.stdout.flush()
			
	print '\n[INFO] Finished calculated review magnitude vector'
	rowMagnitudeArray = np.array(rowMagnitudes)
		
	#Calculate/load dot product
	print '\n[INFO] Performing multiplication on transpose....'
	startTime = time.clock()				 #Time for profiling
	transpose = userBeerReviewMatrix.transpose(copy=True)
	
	resultantMatrix = userBeerReviewMatrix * transpose
	
	reviewTimeToProcess = time.clock() - startTime
	print '[INFO] Completed multiplication on transpose in ' + str(reviewTimeToProcess) + ' seconds'
		
	if resultantMatrix.shape[0] != resultantMatrix.shape[1]:  
		print '[ERROR] Invalid matrix dimensions! Similarity matrix should be square, user-user!'
	
	#Split array into manageable parts in memory (rows x #beers)
	rows = 100
	maxRows = resultantMatrix.shape[1]
	rowMagnitudeArrayDivisor = 1/rowMagnitudeArray	  #Divisor for converting to cosine form	
	
	print '\n[INFO] Calculating user similarity matrix...'
	for i in range(0,maxRows,rows):
		if i + rows < maxRows:
			slicedMatrix = resultantMatrix[i:i+rows]		#Slice the matrix to a smaller subset
		else:
			slicedMatrix = resultantMatrix[i:]			  #Catch last bit of the matrix
		  
		try:
			slicedMatrix = slicedMatrix.multiply(rowMagnitudeArrayDivisor)
			testArrayTrans = slicedMatrix.transpose()					   #Transpose in order to multiply by sliced row magnitude
			slicedRowMag = rowMagnitudeArrayDivisor[i:i+rows]			   #Slice by subset
			testArrayTrans = np.multiply(testArrayTrans, slicedRowMag)	  #By ELEMENT multiplication
			  
			restoredMatrix = testArrayTrans.transpose()					 #Back to original dimensions
			  
			resultantMatrix[i:i+rows] = restoredMatrix
		except Exception as e:
			print '[ERROR] Failed to do matrix multiplication. Are you sure you are using the correct magnitude vector? Try setting calculateMagnitudeVector = True and re-running'
			print e
			
		#TODO fix progress bar
		sys.stdout.write("Working...")
		sys.stdout.flush()
	  
	print '\n[INFO] Similarity matrix complete!'
	# print str(resultantMatrix.todense())
	print '---------------'
		 
	print '\n[INFO] Converting matrix to dense array form....' 
	arrayForm = resultantMatrix.toarray()
	print '[INFO] Converting matrix to triangular form.... '
	triMatrix = np.tril(arrayForm)
	print '[INFO] Conversion complete!'
	if repickleSimilarityMatrix:
		print '[INFO] Pickling triangular matrix'
		
		try:
			similarityMatrix = open("similatiryMatrix" + reviewThresholdString + ".pickle", 'w')
			
			pickle.dump(triMatrix, similarityMatrix)
			print '[INFO] Finished pickling triangular similarity matrix'
		
		except Exception as e:
			print '[ERROR] Pickling operation failed!: ' + str(e)
	else:
		'[INFO] Pickling disabled. Terminating....'

else:		#Load pickled similarity matrix
	# Open the serialized user-beer review sparse array from pickled file
	try:
		print '[INFO] Reading serialized (PICKLED!) triangular similarity matrix.....'
		file = open("similatiryMatrix" + reviewThresholdString + ".pickle", 'r')
		similarityMatrix = pickle.load(file)
		print '[INFO] Successfully opened pickled triangular similarity matrix!'
	except Exception as e:
		print '[ERROR] Opening pickled file failed!: ' + str(e)

print similarityMatrix[0]


