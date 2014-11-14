#!/usr/bin/python

def splitSentence(n,rawData):
    for entry in rawData:
        length = len(entry['sentence'])
        partLen = length/n
        partsList = {}
        if length > n:
            for i in range(n):
                partsList[i] = entry['sentence'][i*partLen:(i+1)*partLen]

            if (length / n) > 0:
                partsList[n] = entry['sentence'][n*partLen:]    
        else:
            for i in range(length):
                partsList[i] = entry['sentence'][i]
        entry['sentence'] = partsList
    return rawData

# rawData = [{'sentenceId':1,'sentence':["a","b","c","d","e"]}]
# print(len(rawData[0]['sentence']))
# print(splitSentence(3,rawData))

