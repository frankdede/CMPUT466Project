#!/usr/bin/python

def splitSentence(n,rawData):
    for entry in rawData:
        length = len(entry['sentence'])
        partLen = length/n
        partsList = []
        if length > n:
            for i in range(n):
                partsList.append(entry['sentence'][i*partLen:(i+1)*partLen])

            if (length % n) > 0:
                partsList[n-1].extend(entry['sentence'][n*partLen:])    
        else:
            for i in range(length):
                partsList.append(entry['sentence'][i])
        entry['sentence'] = partsList
    return rawData

# Here are some tesing code
# rawData = [{'sentenceId':1,'sentence':["My","name","is","frank","huang",".","lalal","dads","dsddsa"]}]
# rawData.append({'sentenceId':2,'sentence':["I","like","this","food"]})
# print(splitSentence(3,rawData))
