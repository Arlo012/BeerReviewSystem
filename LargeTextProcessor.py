import time

class User:
    '''
    Contains profile information about a user.
    '''

    def __init__(self, ID):
        self.ID = ID
        self.beersConsumed = []
        
        #TODO beer preference mapping?
    
    
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
        self.ID = ID
        self.brewerID = bID
        self.abv = abv
        self.style = style
    
class Review:
    '''
    A review is made up of one reviewer, one beer, and one set of
    beer rated parameters.
    '''
    
    def __init__(self, user, beer, aroma, palate, taste, overall, reviewTime, text):
        self.user = user
        self.beer = beer
        self.aroma = aroma
        self.palate = palate
        self.taste = taste
        self.overall = overall
        self.reviewTime = reviewTime
        self.text = text


'''
Do line-by-line read of the file (won't load it all into memory) and store
in above class structures.
'''
#CHANGE FILEPATH HERE FOR YOUR MACHINE
with open("/media/eljefe/BC7A0ADA7A0A9176/beeradvocate.txt") as infile:
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
    
    reviewList = []
    beersToProcess = 70000
    counter = 0
    
    #Create a unique user ID starting at 0
    actualUserIDtoSetID = {}
    userIDCounter = 0           #For unique user ID
    
    #Create a unique beer ID starting at 0
    actualBeerIDtoSetID = {}
    userBeerCounter = 0           #For unique beer ID
    
    startTime = time.clock()                 #Time for profiling
    for rawLine in infile:                   #Iterate through every line, one at a time
        if counter >= beersToProcess:        #Only check subset of beers                                        
            break
        line = rawLine.rstrip()              #Remove newline & any unnecessary white space
        
        if 'beer/name: ' in line:
            name = line.replace('beer/name: ', '')      #Trim the beer/name text out
        elif 'beer/beerId: ' in line:
            beerID = line.replace('beer/beerId: ', '')
            
            if beerID in actualBeerIDtoSetID:          #Check if we have already created unique profile ID for this beer
                beerID = actualBeerIDtoSetID[beerID]
            else:
                actualBeerIDtoSetID[beerID] = userBeerCounter
                beerID = userBeerCounter
                userBeerCounter += 1
                
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
            if profileName in actualUserIDtoSetID:          #Check if we have already created unique profile ID for this username
                profileName = actualUserIDtoSetID[profileName]
            else:
                actualUserIDtoSetID[profileName] = userIDCounter
                profileName = userIDCounter
                userIDCounter += 1
            
        elif 'review/text: ' in line:
            text = line.replace('review/text: ', '')            
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
             
            if counter % 1000 == 0:
                print 'Processed ' + str(counter)

#Display parse performance
reviewTimeToProcess = time.clock() - startTime
print '[INFO]: Processed ' + str(len(reviewList)) + ' beer reviews in ' + str(reviewTimeToProcess) + ' seconds'

#Update users to have unique, sequential IDs

#Example user-beer mapping
userBeerMap = {}
for review in reviewList:
    user = review.user
    if user not in userBeerMap:     #Add user to user-beer mapping
        userBeerMap[user] = [review.beer]
    else:                           #User already in dictionary; add another beer they reviewed
        userBeerMap[user].append(review.beer)
 
#Example user-review mapping
userReviewMap = {}
for review in reviewList:
    user = review.user
    if user not in userReviewMap:     #Add user to user-review mapping
        userReviewMap[user] = [review]
    else:                             #User already in dictionary; add another one of their reviews
        userReviewMap[user].append(review)

#Find a beer by beer ID
for review in reviewList:
    if review.user == 0:
        print review.beer.name
    

#Average score calculation
goodProfiles = 0
totalUsers = 0
for user in userReviewMap:
    totalUsers += 1
    netScore = 0
    reviewCount = 0
    for review in userReviewMap[user]:
        reviewCount += 1
    if reviewCount >= 2:
        goodProfiles += 1
print 'Total profiles with >1 review: ' + str(goodProfiles)
print 'Total users: ' + str(totalUsers)



