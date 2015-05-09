import Tkinter
import tkMessageBox
import ttk
from LargeTextProcessor import Beer
from Recommender import Recommender
import pickle

class User():					# the user object that is used for creating profiles within the system
	def __init__(self, _name):
		self.name = _name
		self.reviews = {}

	def addBeer(beer, rating):
		self.reviews['beer'] = [beer, rating]

	def getReviews():
		return self.reviews

class BeerGUI(Tkinter.Tk):				#creates the class that inherits Tkinter, acts as the main window
	def __init__(self, parent):
		Tkinter.Tk.__init__(self, parent)

		self.parent = parent
		self.grid()
		self.userList = {}				#the map of all the usersnames to user objects for quick reference - keys can be used in the combo box
		try:
			userFile = open("profiles.pickle", 'r')
			self.userList = pickle.load(userFile)			#loads the file of the users - This saves the beer preferences of each user
		except Exception as e:
			pass
		beerFile = open("beerMap-T5.pickle", 'r')
		self.beerList = pickle.load(beerFile)				#retrieves all the beers from the file

		self.background = Tkinter.PhotoImage(file = "beer_PNG.png")
		self.backgroundLabel = Tkinter.Label(parent, image = self.background)
		self.backgroundLabel.place(x = 0, y = 0)		#adds the background image
		self.geometry("600x500+0+0")					#sets the size of the screen

		recommendationButton = Tkinter.Button(self, text = "Get a Recommendation", command = self.RecommendationClick)
		rateButton = Tkinter.Button(self, text = "Rate a Beer", command = self.RateClick)
		myBeersButton = Tkinter.Button(self, text = "My Beers", command = self.GetMyBeers)				#creates all the buttons on the top 
		recommendationButton.grid(column = 0, row = 0)
		rateButton.grid(column = 1, row = 0)
		myBeersButton.grid(column = 2, row = 0)				#sets the locations of the buttons

		asLabel = Tkinter.Label(self, text = "As:")			#An asthetic Label
		asLabel.grid(column = 3, row = 0)

		self.profileDropDown = ttk.Combobox(self, width = 12)		#creates a combo box with all the users in it
		self.profileDropDown.grid(column = 4, row = 0)
		if len(self.userList) > 0:				#if there are users, add them to the drop down menu
			names = self.userList.keys()
			self.profileDropDown['values'] = names
			self.profileDropDown.current(0)			#set the current selction to the first user in the list


		createButton = Tkinter.Button(self, text = "Create Profile", command = self.CreateProfile)		#button to make the program
		createButton.grid(column = 5, row = 0)

		self.protocol("WM_DELETE_WINDOW", self.Save)		#this is a command that intercepts the exit button on the top left

	def Save(self):				#this runs when the window is closed
		print "SAVING"
		try:
			profilesFile = open("profiles.pickle", 'w')
			pickle.dump(self.userList, profilesFile)		#saves all the users
			self.destroy()		#kills the window
		except Exception as e:
			print e

	def RecommendationClick(self):					#activated to make a recommendation
		if len(self.userList) == 0:
			tkMessageBox.showwarning("Beer", "Please Create a Profile...")
		else:
			userName = self.profileDropDown.get()
			user = self.userList[userName]		#gets the current user

			if len(user.reviews) == 0:
				tkMessageBox.showwarning("No Reviews", "Please review a beer before asking for a recommendation...")

			recommendations = Recommender(user.reviews)		#runs the recommendation program

			recommendationBox = Tkinter.Toplevel()			#makes a popup window for the recommendations
			recommendationBox.geometry("+0+0")
			recommendationBox.title("You should try:...")
			recommendationBox.grid()
			labels = []
			for i in range(0, len(recommendations)):		#adds a bunch of labels for the recommendations
				nextLabel = Tkinter.Label(recommendationBox, text = recommendations[i])
				nextLabel.grid(column = 0, row = i)
				labels.append(nextLabel)



	def RateClick(self):			#activated when wanting to rate a beer
		name = None
		rating = 0
		if len(self.userList) == 0:
			tkMessageBox.showwarning("Beer", "Please Create a Profile...")
		else:
			def GetEntry(event):		#when the user inputs valid information and hits enter
				try:
					beerName = beerNameBox.get()
					user = self.profileDropDown.get()
					rating = float(beerRating.get())*10
					rating = int(rating)
					if 0 <= rating <= 50:
						currentUser = self.userList[user]
						print currentUser.reviews
						currentUser.reviews[beerName] = [beerName, rating]		#adds the beer rating to the list of ratings by the user
						entryBox.destroy()
					else:
						raise Exception()
				except Exception as e:
					tkMessageBox.showwarning("Beer", "Rating must be a number from 0 to 5")
					print e

			def CheckBeer(event):
				def getSelection():
					beerNameBox.delete(0, Tkinter.END)		#activated by the suggestion select button 
					beerNameBox.insert(0, suggestionCombo.get())		#puts the selected beer in the entry box
					suggestionBox.destroy()

				beerName = beerNameBox.get()			#creates a new popup for giving suggestions
				if beerName not in self.beerList:
					suggestionBox = Tkinter.Toplevel()
					suggestionBox.title("Beer Suggestions")
					suggestionBox.geometry("+0+0")
					suggestionLabel1 = Tkinter.Label(suggestionBox, text = "Sorry that beer was not in our data base \n did you mean one of these?")
					suggestionLabel1.pack()
					suggestionCombo = ttk.Combobox(suggestionBox, width = 30)
					suggestionCombo.pack()
					entryBox.attributes('-topmost', 1)
					entryBox.attributes('-topmost', 0)
					suggestionBox.attributes('-topmost', 1)

					suggestionSelect = Tkinter.Button(suggestionBox, text = "Select", command = getSelection)  #button that will insert the text from the selction into the entry box for the name of the beer
					suggestionSelect.pack()

					possibleBeers = []		#searches for beers that the user could be looking for
					iterator = iter(self.beerList)
					for iterator in self.beerList:
						if beerName.lower() in self.beerList[iterator].name.lower():
							possibleBeers.append(self.beerList[iterator].name)

					suggestionCombo['values'] = possibleBeers
					suggestionCombo.current(0)		#and puts the beers in the combo box

			entryBox = Tkinter.Toplevel()				#makes a box with two entry areas, for the beer name and the beer rating
			entryBox.title("Enter a Beer and a Rating")
			entryBox.geometry("+0+0")
			beerNameBox = Tkinter.Entry(entryBox)
			beerRating = Tkinter.Entry(entryBox)
			entryBox.grid()
			beerNameBox.grid(column = 1, row = 0)
			beerNameBox.focus_set()
			beerNameBox.bind("<Tab>", CheckBeer)		#if you hit tab or enter from the name box, then it will check the name in the beerlist
			beerNameBox.bind("<Return>", CheckBeer)
			beerRating.grid(column = 1, row = 1)
			beerRating.bind("<Return>", GetEntry)
			nameLabel = Tkinter.Label(entryBox, text = "Beer Name")
			ratingLabel = Tkinter.Label(entryBox, text = "Beer Rating")
			nameLabel.grid(column = 0, row = 0)
			ratingLabel.grid(column = 0, row = 1)


	def GetMyBeers(self):				#creates a box to display all the beers for a select profile
		if len(self.userList) == 0:
			tkMessageBox.showwarning("Beer", "Please Create a Profile...")
		else:
			userName = self.profileDropDown.get()
			user = self.userList[userName]
			if len(user.reviews) > 0:
				userName = self.profileDropDown.get()
				user = self.userList[userName]
				myBeersBox = Tkinter.Toplevel()
				myBeersBox.geometry("+0+0")
				myBeersBox.title("My Beers")
				myBeersBox.grid()

				iterator = iter(user.reviews)

				titleLabel = Tkinter.Label(myBeersBox, text = "Beer Name:")
				ratingLabel = Tkinter.Label(myBeersBox, text = "Rating:")
				titleLabel.grid(column = 0, row = 0)
				ratingLabel.grid(column = 2, row = 0)
				count = 1
				for iterator in user.reviews:
					nextBeerLabel = Tkinter.Label(myBeersBox, text = user.reviews[iterator][0])
					nextRatingLabel = Tkinter.Label(myBeersBox, text = float(user.reviews[iterator][1])/10)
					fillLabel = Tkinter.Label(myBeersBox, text = "--------->")
					nextBeerLabel.grid(column = 0, row = count)
					fillLabel.grid(column = 1, row = count)
					nextRatingLabel.grid(column = 2, row = count)
					count += 1

			else:
				tkMessageBox.showwarning("Beer", "No Beers to Display")


	def CreateProfile(self):

		def GetName(event):
			profileName = profileEntry.get()
			newUser = User(profileName)
			
			newProfileBox.destroy()
			self.userList[profileName] = newUser
			names = self.userList.keys()
			self.profileDropDown['values'] = names		#saves it into the list of users
			self.profileDropDown.current(0)

		newProfileBox = Tkinter.Toplevel()
		newProfileBox.title("Enter a User Name:")			#asks the user to give a name, goes to the Getname method above
		newProfileBox.geometry("+0+0")
		profileEntry = Tkinter.Entry(newProfileBox)
		profileEntryLabel = Tkinter.Label(newProfileBox, text = "User ID:")

		newProfileBox.grid()
		profileEntryLabel.grid(column = 0, row = 0)
		profileEntry.grid(column = 1, row = 0)
		profileEntry.focus_set()

		profileEntry.bind("<Return>", GetName)


if __name__ == "__main__":
	GUI = BeerGUI(None)
	GUI.title("Beer Recommender")
	GUI.mainloop()