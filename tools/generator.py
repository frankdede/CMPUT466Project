#!/usr/bin/python
import nltk
import numpy

def createFreqMatrix(n,splitedRawData,freqLookupData):

    #size = (len(splitedRawData),n+1)
    size = 500
    freqMatrix = numpy.zeros(size,dtype = ('f4,f4,f4,a1'))

    for entry in range(500):
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
        
        freqMatrix[entry][n] = str(splitedRawData[entry]['sentiment'])
        #print(entry,freqMatrix[entry][n])
    saveMatrix(freqMatrix)
#
def createFeatureBagMatrix(splitedRawData):
    totalLabelSet = set()
    for sentence in splitedRawData:
        totalLabelSet = totalLabelSet.union(set(sentence['sentence']))
    matrix_list= list()
    for sentence in splitedRawData:
        #print(sentence)
        tmp = map(lambda x:1 if x in sentence['sentence'] else 0,totalLabelSet)
        tmp.append(sentence["sentiment"])
        matrix_list.append(tmp)
    matrix_array = numpy.array(matrix_list)
    matrix = numpy.matrix(matrix_array)
    print(matrix.shape)
    numpy.savetxt("matrix2.txt", matrix, delimiter=",",fmt="%s")
    return matrix
def saveMatrix(matrix):
    numpy.savetxt("matrix.txt", matrix, delimiter=",",fmt="%s")

if __name__ == '__main__':
    rawData = [{'sentiment':1,'sentence':["My","name","is","frank","huang",".","lalal","dads","dsddsa"]}]
    rawData.append({'sentiment':2,'sentence':["I","like","this","food"]})
    print(createFeatureBagMatrix(rawData))