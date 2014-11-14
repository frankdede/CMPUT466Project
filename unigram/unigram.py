#!/usr/bin/python
import nltk
def extractUnigrams(invertedRawData):
	print(len(invertedRawData))
	unigramCollection = {}
	#print(invertedRawData[0])
	for sentiment in invertedRawData:
		print("hello Processing sentiment " + str(sentiment) )
        #if sentiment not in unigramCollection:
        unigramCollection[str(sentiment)] = 'abc'
        #for entry in invertedRawData[sentiment]:
 		#	pass
        	#unigramCollection[sentiment].extend(entry['sentence'])
	for i in unigramCollection:
		print i
	return unigramCollection