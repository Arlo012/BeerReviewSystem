import time

class User:
    '''
    Contains profile information about a user.
    '''

    def __init__(self, ID):
        self.ID = ID
        self.beersConsumed = []
        
    def AddBeerConsumd(self, beer):
        self.beersConsumed.append(beer)
    
    
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
    beersToProcess = 20000
    counter = 0
    
    startTime = time.clock()
    for rawLine in infile:                          
        if counter >= beersToProcess:        #Only check subset of beers                                        
            break
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
        elif 'review/reviewTime :' in line:
            reviewTime = line.replace('review/reviewTime: ', '')
        elif 'review/profileName:' in line:
            profileName = line.replace('review/profileName: ', '')
        elif 'review/text: ' in line:
            text = line.replace('review/text: ', '')            
            review = Review(profileName, ratedBeer, aroma, palate, taste, overall, reviewTime, text)
            reviewList.append(review)
            
#             print '[INFO]: Found new beer review: ' + name
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
            
reviewTimeToProcess = time.clock() - startTime
print '[INFO]: Processed ' + str(len(reviewList)) + ' beer reviews in ' + str(reviewTimeToProcess) + ' seconds'

#EXAMPLE READOUT
strongAleCount = 0
for review in reviewList:
    if review.beer.style == 'English Strong Ale':
        strongAleCount += 1
print 'Found ' + str(strongAleCount) + ' reviews for English strong ales!'
            
            
            
            