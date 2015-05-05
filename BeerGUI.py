import Tkinter
import tkMessageBox
import ttk
from LargeTextProcessor import Beer
from Recommender import Recommender
import pickle

class User():
	def __init__(self, _name):
		self.name = _name
		self.reviews = {}

	def addBeer(beer, rating):
		self.reviews['beer'] = [beer, rating]

	def getReviews():
		return self.reviews

class BeerGUI(Tkinter.Tk):
	def __init__(self, parent):
		Tkinter.Tk.__init__(self, parent)

		self.parent = parent
		self.grid()
		self.userList = {}
		try:
			userFile = open("profiles.pickle", 'r')
			self.userList = pickle.load(userFile)
		except Exception as e:
			pass
		beerFile = open("beerMap-T5.pickle", 'r')
		self.beerList = pickle.load(beerFile)

		self.background = Tkinter.PhotoImage(file = "beer_PNG.png")
		self.backgroundLabel = Tkinter.Label(parent, image = self.background)
		self.backgroundLabel.place(x = 0, y = 0)
		self.geometry("600x500")

		recommendationButton = Tkinter.Button(self, text = "Get a Recommendation", command = self.RecommendationClick)
		rateButton = Tkinter.Button(self, text = "Rate a Beer", command = self.RateClick)
		myBeersButton = Tkinter.Button(self, text = "My Beers", command = self.GetMyBeers)
		recommendationButton.grid(column = 0, row = 0)
		rateButton.grid(column = 1, row = 0)
		myBeersButton.grid(column = 2, row = 0)

		asLabel = Tkinter.Label(self, text = "As:")
		asLabel.grid(column = 3, row = 0)

		self.profileDropDown = ttk.Combobox(self, width = 12)
		self.profileDropDown.grid(column = 4, row = 0)
		if len(self.userList) > 0:
			names = self.userList.keys()
			self.profileDropDown['values'] = names
			self.profileDropDown.current(0)


		createButton = Tkinter.Button(self, text = "Create Profile", command = self.CreateProfile)
		createButton.grid(column = 5, row = 0)

		self.protocol("WM_DELETE_WINDOW", self.Save)

	def Save(self):
		print "SAVING"
		try:
			profilesFile = open("profiles.pickle", 'w')
			pickle.dump(self.userList, profilesFile)
			self.destroy()
		except Exception as e:
			print e

	def RecommendationClick(self):
		if len(self.userList) == 0:
			tkMessageBox.showwarning("Beer", "Please Create a Profile...")
		else:
			userName = self.profileDropDown.get()
			user = self.userList[userName]

			if len(user.reviews) == 0:
				tkMessageBox.showwarning("No Reviews", "Please review a beer before asking for a recommendation...")
			recommendations = Recommender(user.reviews)

			recommendationBox = Tkinter.Toplevel()
			recommendationBox.title("You should try:...")
			recommendationBox.grid()
			labels = []
			for i in range(0, len(recommendations)):
				nextLabel = Tkinter.Label(recommendationBox, text = recommendations[i])
				nextLabel.grid(column = 0, row = i)
				labels.append(nextLabel)



	def RateClick(self):
		name = None
		rating = 0
		if len(self.userList) == 0:
			tkMessageBox.showwarning("Beer", "Please Create a Profile...")
		else:
			def GetEntry(event):
				try: 
					beerName = beerNameBox.get()
					user = self.profileDropDown.get()
					rating = float(beerRating.get())*10
					rating = int(rating)
					if 0 <= rating <= 50:
						currentUser = self.userList[user]
						print currentUser.reviews
						currentUser.reviews[beerName] = [beerName, rating]
						entryBox.destroy()
					else:
						raise Exception()
				except Exception as e:
					tkMessageBox.showwarning("Beer", "Rating must be a number from 0 to 5")
					print e

			def CheckBeer(event):
				beerName = beerNameBox.get()
				if beerName not in self.beerList:
					tkMessageBox.showwarning("Invalid Beer", "Sorry, that Beer is not in our data base")
					beerNameBox.focus_set()
					entryBox.attributes('-topmost', 1)

			entryBox = Tkinter.Toplevel()
			entryBox.title("Enter a Beer and a Rating")
			beerNameBox = Tkinter.Entry(entryBox)
			beerRating = Tkinter.Entry(entryBox)
			entryBox.grid()
			beerNameBox.grid(column = 1, row = 0)
			beerNameBox.focus_set()
			beerNameBox.bind("<Tab>", CheckBeer)
			beerNameBox.bind("<Return>", CheckBeer)
			beerRating.grid(column = 1, row = 1)
			beerRating.bind("<Return>", GetEntry)
			nameLabel = Tkinter.Label(entryBox, text = "Beer Name")
			ratingLabel = Tkinter.Label(entryBox, text = "Beer Rating")
			nameLabel.grid(column = 0, row = 0)
			ratingLabel.grid(column = 0, row = 1)


	def GetMyBeers(self):
		if len(self.userList) == 0:
			tkMessageBox.showwarning("Beer", "Please Create a Profile...")
		else:
			userName = self.profileDropDown.get()
			user = self.userList[userName]
			if len(user.reviews) > 0:
				userName = self.profileDropDown.get()
				user = self.userList[userName]
				myBeersBox = Tkinter.Toplevel()
				myBeersBox.geometry("300x100")
				myBeersBox.title("My Beers")
				myBeersBox.grid()

				iterator = iter(user.reviews)
				count = 0
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
			self.profileDropDown['values'] = names
			self.profileDropDown.current(0)

		newProfileBox = Tkinter.Toplevel()
		newProfileBox.title("Enter a User Name:")
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