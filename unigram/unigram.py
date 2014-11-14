#!/usr/bin/python
import nltk
def extractUnigrams(invertedRawData):
	print(len(invertedRawData))
	unigramCollection = {}
	#print(invertedRawData[0])
	counter = 0
	for sentiment in invertedRawData.keys():
		print("hello Processing sentiment " + str(sentiment) )
        	if sentiment not in unigramCollection:
        		unigramCollection[sentiment] = []
        	for entry in invertedRawData[sentiment]:
        		unigramCollection[sentiment].extend(entry['sentence'])
	print(len(unigramCollection.keys()))
	return unigramCollection
