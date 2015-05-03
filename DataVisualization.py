'''
User-to-User Correlation Matrix Visualization using plotly library
Reference: https://plot.ly/python/2D-Histogram/
'''

import plotly.plotly as py
from plotly.graph_objs import *
import numpy as ny 

#Assume users will come as a list of IDs
'''
users = correlationMatrix.keys()
'''
users = [0, 1, 2, 3, 4]

#Assume data is given as dictionary where keys are user IDs
#and each ID gives a list of correlation values
'''
userCorrelation = []
for row in correlationMatrix.keys():
	userCorrelation.append(correlationMatrix[row])
'''
userCorrelation = [[1, 0.1, 0, 1, 0.05], [0.1, 1, 0.3, 0.1, 0.7], [0, 0.3, 1, 0.2, 0], [1, 0.1, 0.2, 1, 0.25], [0.05, 0.7, 0, 0.25, 1]]

data = Data([Heatmap(z= userCorrelation,x = users, y=users)])

plot = py.plot(data, filename = 'userCorrelationVisualization')