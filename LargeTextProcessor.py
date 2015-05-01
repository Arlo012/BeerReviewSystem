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
    
class Review:
    '''
    A review is made up of one reviewer, one beer, and one set of
    beer rated parameters.
    '''
    
    def __init__(self, user, beer, aroma, palate, taste, overall, reviewTime, text):
        self.user = user
        self.beer = beer
        self.aroma = int8(float(aroma)*10)       #Convert to int 0-50 to save on memory
        self.palate = int8(float(palate)*10)
        self.taste = int8(float(taste)*10)
        self.overall = int8(float(overall)*10)
        self.reviewTime = long(reviewTime)
        self.text = text


beersToProcess = 1586300/64             #How many reviews to we want to process
overwritePickle = False              #Overwrite the pickle output file with this run?

'''
Do line-by-line read of the file (won't load it all into memory) and store
in above class structures.
'''
#CHANGE FILEPATH HERE FOR YOUR MACHINE
with open("/media/eljefe/BC7A0ADA7A0A9176/beeradvocate.txt") as infile:
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
    
    reviewList = []
    counter = 0
    
    #Create a unique user ID starting at 0
    originalUsernameToNewUserIDMap = {}
    userReviewCount = np.zeros(30000)
    userIDCounter = 0           #For unique user ID
    
    #Create a unique beer ID starting at 0
    originalBeerIDtoNewBeerIDMap = {}
    beerIDCounter = 0           #For unique beer ID
    
    print '[INFO] Beginning to parse reviews'
    if not overwritePickle:
        print '[WARNING] This is a test run only! The output will NOT be pickled.'
        
    startTime = time.clock()                 #Time for profiling
    for rawLine in infile:                   #Iterate through every line, one at a time
        if counter >= beersToProcess:        #Only check subset of beers                                        
            break
        
        if rawLine.isspace():       #Space separator
            #Create the review
            review = Review(profileName, ratedBeer, aroma, palate, taste, overall, reviewTime, text)
            reviewList.append(review)
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
            
            if counter % int(0.01*beersToProcess) == 0:
                bar_length = 100
                percent = float(counter) / beersToProcess
                hashes = '#' * int(round(percent * bar_length))
                spaces = ' ' * (bar_length - len(hashes))
                sys.stdout.write("\rProgress: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
                sys.stdout.flush()
        
        line = rawLine.rstrip()              #Remove newline & any unnecessary white space
        
        if 'beer/name: ' in line:
            name = line.replace('beer/name: ', '')      #Trim the beer/name text out
        elif 'beer/beerId: ' in line:
            beerID = line.replace('beer/beerId: ', '')
            
            if beerID in originalBeerIDtoNewBeerIDMap:          #Check if we have already created unique profile ID for this beer
                beerID = originalBeerIDtoNewBeerIDMap[beerID]
            else:
                originalBeerIDtoNewBeerIDMap[beerID] = beerIDCounter
                beerID = beerIDCounter
                beerIDCounter += 1
                
        elif 'beer/brewerId: ' in line:
            brewerID = line.replace('beer/brewerId: ', '')
        elif 'beer/ABV: ' in line:
            abv = line.replace('beer/ABV: ', '')
        elif 'beer/style: ' in line:
            style = line.replace('beer/style: ', '')
            ratedBeer = Beer(name, beerID, brewerID, abv, style)    #All beer info before this; create obj
       
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
            if profileName in originalUsernameToNewUserIDMap:          #Check if we have already created unique profile ID for this username
                profileName = originalUsernameToNewUserIDMap[profileName]   #Use this mapping for the new profile name
                userReviewCount[profileName] += 1   #Track how many reviews on this user by index
            else:                                                    #Create new mapping of real user ID to next unique ID
                originalUsernameToNewUserIDMap[profileName] = userIDCounter
                profileName = userIDCounter             #Replace real username with user ID
                userReviewCount[profileName] += 1       #Track how many reviews on this user by index
                userIDCounter += 1
        
        elif 'review/text: ' in line:
#             text = line.replace('review/text: ', '')            
            text = ''           #Toss out the review text for sake of memory
                  
                
#Display parse performance
reviewTimeToProcess = time.clock() - startTime
print '\n[INFO]: Processed ' + str(len(reviewList)) + ' beer reviews in ' + str(reviewTimeToProcess) + ' seconds'
print '[INFO] Total of: ' + str(sys.getsizeof(reviewList)) + ' bytes'
print '-----------------------------'


#User-review mapping 
#FIXME trimming users like this leaves some beers with no reviews
print '\n[INFO] Building user review map and trimming users below minimum review threshold...'
userReviewMap = {}
minimumReviewThreshold = 1      #Set higher to trim
trimmedReviewCount = 0
for review in reviewList:
    user = review.user
    if int(userReviewCount[user]) < minimumReviewThreshold:
        if user not in userReviewMap:     #Add user to user-review mapping
            userReviewMap[user] = [review]
        else:                             #User already in dictionary; add another one of their reviews
            userReviewMap[user].append(review)
    else:
        trimmedReviewCount += 1
        '[DEBUG] User ' + str(user) + ' did not meet minimum review requirement'
  
print '[INFO] Trimmed ' + str(trimmedReviewCount) + ' reviews below from users below review threshold from the database from total of ' + str(counter) + ' reviews.'
 
print '\n[INFO] Rebuilding valid users into new dictionary mapping...'
uniqueIDCounter = 0     #A counter to build a unique ID now for only VALID users (above review threshold)
trimmedUserReviewMap = {}
users = userReviewMap.keys()
for user in users:
    trimmedUserReviewMap[uniqueIDCounter] = user              #Track old ID for reverse lookup
    userReviewMap[uniqueIDCounter] = userReviewMap[user]      #Update new unique ID to be key over old one
    uniqueIDCounter += 1
         
print '[INFO] Finished building valid user unique ID map'

#Begin prepping for numpy array translation
print '\n[INFO] Transferring data into numpy arrays for placement into sparse matrix....'

#Generate list of beers
beerList = []
for i in range(0,beerIDCounter):
    beerList.append(i)
    
if(len(beerList) != len(set(beerList))):
    print '[ERROR] Duplicate beers found in the beer list!'

#Generate list of users (straight from keys)
userList = []
for user in userReviewMap:
    userList.append(user)
    
if(len(userList) != len(set(userList))):
    print '[ERROR] Duplicate users found in the user list!'
    
#Convert into format of row,column,data coordinates (see: https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html#scipy.sparse.csr_matrix)
row = []            #Users (this is the Y coordinate of where data goes in the matrix)
column = []         #Beers (this is the X coordinate of where data goes in the matrix)
data = []           #Reviews (this is the data in the matrix)

#TODO there are some beers that have only been reviewed by the people we just deleted (if review threshold >1)....

for user in userList:      #A single row
    for review in userReviewMap[user]:
        row.append(user)            #User ID as row
        column.append(review.beer.ID)
        data.append(review.overall)
# print '[DEBUG] Last mapping: (' + str(row[len(row)-1]) + ', ' + str(column[len(column)-1]) + ')'

#Check if user has at least one review:
for user in userReviewMap:
    if len(userReviewMap[user]) == 0:
        print '[ERROR] A user was pulled from the database with no reviews. What happened?! This will break the analyzer with divide by zero problems'

#Convert all to numpy arrays
numPiRow = np.array(row)
numPiColumn = np.array(column)
numpiData = np.array(data)

#Create sparse array (compressed by row)
print '[INFO] Creating sparse matrix with dimensions (' + str(len(userList)) + ', ' + str(len(beerList)) + ')'
userBeerReviewArray = csr_matrix((numpiData, (numPiRow, numPiColumn)), shape=(len(userList),len(beerList)), dtype=int)

#Dump out to file
if overwritePickle:
    print '[INFO] Pickling sparse matrix out to beerArray.pickle'
    try:
        dumpfile = open("beerArray.pickle", 'w')
        pickle.dump(userBeerReviewArray, dumpfile)
        print '[INFO] Finished pickling sparse matrix'
    except Exception as e:
        print '[ERROR] Pickling operation failed!: ' + str(e)
else:
    print '[INFO] Pickle overwrite disabled. Not writing out to filesystem'
    

