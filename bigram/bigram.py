#!/usr/bin/python
import nltk

# use of frequency distribution : freqTable[0].freq(('abc','def'))
def getFrequencyDist(bigramsCollection):
    print("********** Creating Frequency Distribution **********")
    freqDist = {}
    for sentiment in bigramsCollection:
        print("Processing sentiment " + str(sentiment) )
        frequency = nltk.FreqDist(bigramsCollection[sentiment])
        freqDist[sentiment] = frequency
    print("Done")
    return freqDist

def extractBigramsFromInvertedRawData(invertedRawData):
    bigramsCollection = {}
    print("********** Converting Sentence to Bigrams for Inverted Raw Data **********")
    for sentiment in invertedRawData:
        print("Processing sentiment " + str(sentiment) )
        if sentiment not in bigramsCollection:
            bigramsCollection[sentiment] = []

        for entry in invertedRawData[sentiment]:
            # E.g. the bigrams of ['a','b','c']
            # will look like this [('a', 'b'), ('b', 'c'), ('c', 'd')]
            bigramsTupleList= list(nltk.bigrams(entry['sentence']))
            bigramsCollection[sentiment].extend(bigramsTupleList)
    print("Done")
    return bigramsCollection

def extractBigramsFromRawData(rawData):

    for entry in rawData:
        bigramsTupleList= list(nltk.bigrams(entry['sentence']))
        entry['sentence'] = bigramsTupleList
    return rawData