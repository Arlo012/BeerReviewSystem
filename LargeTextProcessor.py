import time
import numpy as np
import sys
from scipy.sparse import *
from numpy import int8, int
from scipy import float16
import pickle

class Beer:
	'''
		Name: Name of the beer.... duh
		ID: Unique identifier in beer advocate DB
		brewerID: Unqiue brewer ID in beer advocate DB
		abv = alcohol by volume
		style = name of this beer's style (may cross brewers)
	'''
	
	def __init__(self, name, ID, bID, abv, style):
		self.name = name
		self.ID = int(ID)
		self.brewerID = int(bID)
		self.abv = float(abv)
		self.style = style
		
		self.matrixIndex = -1           #For referencing column on matrix (default invalid to -1 to catch errors)
	
class Review:
	'''
	A review is made up of one reviewer, one beer, and one set of
	beer rated parameters.
	'''
	
	def __init__(self, user, beer, aroma, palate, taste, overall, reviewTime, text):
		self.user = user        #User object
		self.beer = beer        #Beer object
		
		#0-50 review categories
		self.aroma = int8(float(aroma)*10)       #Convert to int 0-50 to save on memory
		self.palate = int8(float(palate)*10)
		self.taste = int8(float(taste)*10)
		self.overall = int8(float(overall)*10)
		
		#Other parameters
		self.reviewTime = long(reviewTime)
		self.text = text

class User:
	'''
	TODO document me
	'''
	
	def __init__(self, userName):
		self.username = userName        #String
		self.matrixIndex = -1           #For referencing row on matrix (default invalid to -1 to catch errors)
		self.reviews = []               #Contains list of reviews made by this user
		
	def AddReview(self, review):
		self.reviews.append(review)


if __name__ == "__main__":
	
	reviewsToProcess = 1586300          #How many reviews to we want to process
	overwritePickle = True                 #Overwrite the pickle output file with this run?

	'''
	Do line-by-line read of the file (won't load it all into memory) and store
	in above class structures.
	'''
	#CHANGE FILEPATH HERE FOR YOUR MACHINE
	with open("beeradvocate.txt") as infile:
		#Beer Info
		name = "undefined"
		beerID = -1
		brewerID = -1
		abv = 0
		style = "undefined"
		
		#Review Info
		appearance = -1
		aroma = -1
		palate = -1 
		taste = -1
		overall = -1
		reviewTime = 0                                                                                                                                                    
		text = "undefined"
		
		#User
		profileName = "undefined"
		
		userMap = {}
		counter = 0
		
		print '[INFO] Beginning to parse reviews'
		if not overwritePickle:
			print '[WARNING] This is a test run only! The output will NOT be pickled.'
			
		startTime = time.clock()                 #Time for profiling
		for rawLine in infile:                   #Iterate through every line, one at a time
			if counter >= reviewsToProcess:        #Only check subset of beers                                        
				break
			
			if rawLine.isspace():       #Space separator between reviews to mark end of review
				if profileName not in userMap:  #Note: profileName = user.username
					#Create the review
					user = User(profileName)                                #Create user object with only profile name
					ratedBeer = Beer(name, beerID, brewerID, abv, style)    #Create beer object using parsed beer params
					
					review = Review(user, ratedBeer, aroma, palate, taste, overall, reviewTime, text)   #Create review linking to user and beer
					user.AddReview(review)              #Allow user to track this review
					
					userMap[user.username] = user      #Add this user to usermap
				else:       #Grab user from map and just add another review to him
					user = userMap[profileName]
					ratedBeer = Beer(name, beerID, brewerID, abv, style)    #Create beer object using parsed beer params
					
					review = Review(user, ratedBeer, aroma, palate, taste, overall, reviewTime, text)   #Create review linking to user and beer
					user.AddReview(review)              #Allow user to track this review
				
				#Append these users to tracked lists
				counter += 1
				
			  #Reset parser info
				#Beer Info
				name = ""
				beerID = -1
				brewerID = -1
				abv = 0
				style = "undefined"
				
				#Review Info
				appearance = -1
				aroma = -1
				palate = -1 
				taste = -1
				overall = -1
				reviewTime = 0
				text = "undefined"
				
				#User
				profileName = "undefined"
				
				#Progress bar
				if counter % int(0.01*reviewsToProcess) == 0:
					bar_length = 100
					percent = float(counter) / reviewsToProcess
					hashes = '#' * int(round(percent * bar_length))
					spaces = ' ' * (bar_length - len(hashes))
					sys.stdout.write("\rProgress: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
					sys.stdout.flush()
			
			line = rawLine.rstrip()              #Remove newline & any unnecessary white space
			
			if 'beer/name: ' in line:
				name = line.replace('beer/name: ', '')      #Trim the beer/name text out
			elif 'beer/beerId: ' in line:
				beerID = line.replace('beer/beerId: ', '')
			elif 'beer/brewerId: ' in line:
				brewerID = line.replace('beer/brewerId: ', '')
			elif 'beer/ABV: ' in line:
				abv = line.replace('beer/ABV: ', '')
			elif 'beer/style: ' in line:
				style = line.replace('beer/style: ', '')
			elif 'review/appearance: ' in line:
				appearance = line.replace('review/appearance: ', '')
			elif 'review/aroma: ' in line:
				aroma = line.replace('review/aroma: ', '')
			elif 'review/palate: ' in line:
				palate = line.replace('review/palate: ', '')
			elif 'review/taste: ' in line:
				taste = line.replace('review/taste: ', '')
			elif 'review/overall: ' in line:
				overall = line.replace('review/overall: ', '')
			elif 'review/time: ' in line:
				reviewTime = line.replace('review/time: ', '')
			elif 'review/profileName:' in line:
				profileName = line.replace('review/profileName: ', '')
			
			elif 'review/text: ' in line:
	#             text = line.replace('review/text: ', '')            
				text = ''           #Toss out the review text for sake of memory
								  
	#Display parse performance
	reviewTimeToProcess = time.clock() - startTime
	print '\n[INFO]: Processed ' + str(counter) + ' beer reviews in ' + str(reviewTimeToProcess) + ' seconds'
	print '[INFO] Total of: ' + str(sys.getsizeof(userMap)) + ' bytes'
	print '-----------------------------'

	print '\n[INFO] Trimming users below the review threshold....'
	#Remove users below review threshold
	minReviewThreshold = 100
	usersToDelete = []
	usersInDatabase = 0
	for user in userMap:
		usersInDatabase += 1
		reviewCount = len(userMap[user].reviews)
		if reviewCount < minReviewThreshold:
			usersToDelete.append(user)
			
	print '[INFO] Removing ' + str(len(usersToDelete)) + ' users from the database (of ' + str(usersInDatabase) + ') + that fell below review threshold...'
	for user in usersToDelete:
		del userMap[user]

	print '[INFO] Finished trimming users from the database!'
	print '-----------------------------'

	print '\n[INFO] Assigning each user/beer a unique ID for matrix indexing...'
	uniqueUserIDCounter = 0
	uniqueBeerIDCounter = 0
	beerMap = {}                    #Map beer name to beer object
	for user in userMap:
		userMap[user].matrixIndex = uniqueUserIDCounter
		uniqueUserIDCounter += 1
		
		reviews = userMap[user].reviews
		for review in reviews:
			beer = review.beer      #Grab beer from review
			if beer.name not in beerMap:
				beer.matrixIndex = uniqueBeerIDCounter
				beerMap[beer.name] = beer
				uniqueBeerIDCounter += 1
			else:
				review.beer = beerMap[beer.name]       #overwrite this beer object with the object that was already found (they should have the same stats)
	print '[INFO] All users and beers now have a unique ID!'
	print '-----------------------------'

	#Begin prepping for numpy array translation
	print '\n[INFO] Transferring data into numpy arrays for placement into sparse matrix....'

	#Generate list of users (straight from keys)
	userList = userMap.keys()
		
	#Convert into format of row,column,data coordinates (see: https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html#scipy.sparse.csr_matrix)
	row = []            #Users (this is the Y coordinate of where data goes in the matrix)
	column = []         #Beers (this is the X coordinate of where data goes in the matrix)
	data = []           #Reviews (this is the data in the matrix)

	for user in userList:      #A single row
		for review in userMap[user].reviews:
			userIndex = userMap[user].matrixIndex
			beerIndex = review.beer.matrixIndex
			
	#         if beerIndex == -1:
	#             print '[ERROR] Invalid matrix index for ' + review.beer.name
			if userIndex == -1:
				print '[ERROR] Invalid matrix index for ' + user.username
			
			row.append(userIndex)       #matrix index generated above as row
			column.append(beerIndex)    #matrix index generated above as column
			data.append(review.overall)
	print '[DEBUG] Last mapping: (' + str(row[len(row)-1]) + ', ' + str(column[len(column)-1]) + ')'

	#Convert all to numpy arrays
	numPiRow = np.array(row)
	numPiColumn = np.array(column)
	numpiData = np.array(data)

	#Create sparse array (compressed by row)
	print '[INFO] Creating sparse matrix with dimensions (' + str(len(userList)) + ', ' + str(len(beerMap.keys())) + ')...'
	userBeerReviewArray = csr_matrix((numpiData, (numPiRow, numPiColumn)), shape=(len(userList),len(beerMap.keys())), dtype=int)
	print '[INFO] Sparse matrix created!'
	print '-----------------------------'

	#Dump out to file
	if overwritePickle:
		print '\n[INFO] Pickling sparse matrix, userMap, and beerMap...'
		try:
			matrixDump = open("userBeerReviewMatrix.pickle", 'w')
			#userMapDump = open("userMap.pickle", 'w')
			beerMapDump = open("beerMap.pickle", 'w')

			pickle.dump(userBeerReviewArray, matrixDump)
			print '[INFO] Finished pickling sparse matrix'
			#pickle.dump(userMap, userMapDump)
			#print '[INFO] Finished pickling userMap'
			pickle.dump(beerMap, beerMapDump)
			print '[INFO] Finished pickling beerMap'
			
		except Exception as e:
			print '[ERROR] Pickling operation failed!: ' + str(e)
	else:
		print '\n[INFO] Pickle overwrite disabled. Not writing out to filesystem'
		

