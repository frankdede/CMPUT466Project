#!/usr/bin/python
import nltk
def extractUnigramFromInvertedRawData(invertedRawData):
    print("********** Extracting Unigram from Raw Data **********")
    unigramCollection = {}
    #print(invertedRawData[0])
    counter = 0
    for sentiment in invertedRawData.keys():
        print("Processing sentiment " + str(sentiment) )
        if sentiment not in unigramCollection:
            unigramCollection[sentiment] = []
        for entry in invertedRawData[sentiment]:
            unigramCollection[sentiment].extend(entry['sentence'])
    return unigramCollection

def extractBigramsFromRawData(rawData):

    for entry in rawData:
        bigramsTupleList= list(nltk.bigrams(entry['sentence']))
        entry['sentence'] = bigramsTupleList
    print entry
    return rawData