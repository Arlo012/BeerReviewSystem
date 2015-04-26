import time
import numpy as np
import sys
from scipy.sparse import *
from numpy import int8
from scipy import float16
import pickle

file = open("beerArray.pickle", 'r')
userBeerReviewArray = pickle.load(file)
print userBeerReviewArray[0]