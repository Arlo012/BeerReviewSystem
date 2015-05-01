import time
import numpy as np
import sys
from scipy.sparse import *
from numpy import int8
from scipy import float16
import pickle

calculateMagnitudeVector = False        #Re-calculate magnitude vector
doBigMatrixDotProduct = True            #Multiply transpose & matrix

#Open the serialized user-beer review sparse array from pickled file
try:
    print '[INFO] Reading serialized (PICKLED!) user-beer-review array.....'
    file = open("beerArray.pickle", 'r')
    userBeerReviewArray = pickle.load(file)
    print '[INFO] Successfully opened pickled user-beer-review array!'
except Exception as e:
    print '[ERROR] Opening pickled filed failed!: ' + str(e)

#Calculate/load magnitude vector
if calculateMagnitudeVector:
    rowMagnitudes = []
    print '\n[INFO] Calculating magnitude vectors.....'
    for i in range(0, userBeerReviewArray.shape[0]):
        row = userBeerReviewArray.getrow(i)
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
        if i % int(0.01*userBeerReviewArray.shape[0]) == 0:
            bar_length = 100
            percent = float(i) / userBeerReviewArray.shape[0]
            hashes = '#' * int(round(percent * bar_length))
            spaces = ' ' * (bar_length - len(hashes))
            sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
            sys.stdout.flush()
            
    print '\n[INFO] Finished calculated review magnitude vector'
    rowMagnitudeArray = np.array(rowMagnitudes)
    
    try:
        print '[INFO] Pickling the row magnitude array out to magnitudeVector.pickle....'
        #Dump out to file
        dumpfile = open("magnitudeVector.pickle", 'w')
        pickle.dump(rowMagnitudeArray, dumpfile)
        print '[INFO] Pickling successful'
        
    except Exception as e:
        print '[ERROR] Pickling unsuccessful: '
        print e
else:
    try:
        print '\n[INFO] Reading serialized (PICKLED!) magnitude vector....'
        file = open("magnitudeVector.pickle", 'r')
        rowMagnitudeArray = pickle.load(file)
        print '[INFO] Successfully opened pickled magnitude vector!'
    except Exception as e:
        print '[ERROR] Opening pickled filed failed!: ' + str(e)
    
#Calculate/load dot product
if doBigMatrixDotProduct:
    print '\n[INFO] Performing multiplication on transpose....'
    startTime = time.clock()                 #Time for profiling
    transpose = userBeerReviewArray.transpose(copy=True)

    resultantMatrix = userBeerReviewArray * transpose
    
    reviewTimeToProcess = time.clock() - startTime
    print '[INFO] Completed multiplication on transpose in ' + str(reviewTimeToProcess) + ' seconds'
    
    #Pickle the dot product
    try:
        print '[INFO] Pickling the dot product matrix out to dotProductMatrix.pickle'
        #Dump out to file
        dumpfile = open("dotProductMatrix.pickle", 'w')
        pickle.dump(resultantMatrix, dumpfile)
        print '[INFO] Pickling successful'
     
    except Exception as e:
        print '[ERROR] Pickling unsuccessful: '
        print e
    
else:
    try:
        print '\n[INFO] Reading serialized (PICKLED!) dot product matrix....'
        file = open("dotProductMatrix.pickle", 'r')
        resultantMatrix = pickle.load(file)
        print '[INFO] Successfully opened pickled dot product matrix!'
    except Exception as e:
        print '[ERROR] Opening pickled filed failed!: ' + str(e)
    
    
#Split array into manageable parts in memory (rows x #beers)
rows = 100
maxRows = resultantMatrix.shape[1]
rowMagnitudeArrayDivisor = 1/rowMagnitudeArray      #Divisor for converting to cosine form    

# print '\n[INFO] Beginning to calculate user similarity matrix...'
# for i in range(0,100,maxRows):
#     slicedMatrix = resultantMatrix[i:i+rows]
#     
#     slicedMatrix = slicedMatrix.multiply(rowMagnitudeArrayDivisor)
#     
#     testArrayTrans = slicedMatrix.transpose()                       #Transpose in order to multiply by sliced row magnitude
#     slicedRowMag = rowMagnitudeArrayDivisor[i:i+rows]                 #Slice by subset
#     testArrayTrans = np.multiply(testArrayTrans, slicedRowMag)      #By ELEMENT multiplication
#     
#     restoredMatrix = testArrayTrans.transpose()                     #Back to original dimensions
#     
#     resultantMatrix[i:i+rows] = restoredMatrix
#     
#     if i % int(0.01*maxRows) == 0:
#         bar_length = 100
#         percent = float(i) / maxRows.shape[0]
#         hashes = '#' * int(round(percent * bar_length))
#         spaces = ' ' * (bar_length - len(hashes))
#         sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
#         sys.stdout.flush()
# 
# print '[INFO] Similarity matrix complete!'

# print str(testArrayTrans[0][0]) + ', ' + str(testArrayTrans[0][0])
    
# #Divide by magnitudes
# print '[INFO] Dividing multiplied matrix by magnitude array (part 1)'
# rowMagnitudeArrayDivisor = 1/rowMagnitudeArray
# resultantMatrix.multiply(rowMagnitudeArrayDivisor)
# 
# print '[INFO] Dividing multiplied matrix by magnitude array (part 2)'
# rowMagnitudeArrayDivisor.transpose()
# resultantMatrix.multiply(rowMagnitudeArrayDivisor)
# 
# print '[INFO] Resultant matrix division complete!'


