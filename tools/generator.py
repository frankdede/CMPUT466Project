#!/usr/bin/python
import nltk
import numpy

def createFreqMatrix(n,splitedRawData,freqLookupData):

    size = (len(splitedRawData),n)
    freqMatrix = numpy.zeros(size)

    for entry in range(len(splitedRawData)):
        size = (1,len(splitedRawData[entry]['sentence']))
        for part in range(len(splitedRawData[entry]['sentence'])):
            total = 0;
            for gram in splitedRawData[entry]['sentence'][part]:
                f0 = freqLookupData[0].freq(gram)
                f1 = freqLookupData[1].freq(gram)
                f2 = freqLookupData[2].freq(gram)
                f3 = freqLookupData[3].freq(gram)
                f4 = freqLookupData[4].freq(gram)
                values = [f0,f1,f2,f3,f4]
                # find the highest value
                highestSentiment = values.index(max(values))

            # sum up
            total += highestSentiment
            # get 
            partAverage = total/float(len(splitedRawData[entry]['sentence']))
            freqMatrix[entry][part] = partAverage
        
        freqMatrix[entry][n] = splitedRawData[entry]['sentiment']
        print(entry,partAverage,splitedRawData[entry]['sentiment'])
    saveMatrix(freqMatrix)


def saveMatrix(matrix):
    numpy.savetxt("matrix.txt", matrix, delimiter=",")
