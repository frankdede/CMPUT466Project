#!/usr/bin/python

def lenLongestSentence(invertedRawData):
    longestLen = 0
#!/usr/bin/python
    for sentiment in invertedRawData:
        for entry in invertedRawData[sentiment]:
            if len(entry["sentence"]) > longestLen:
                longestLen = len(entry["sentence"])
    return longestLen

def countForEachSentiment(invertedRawData):
    count = {}

    for sentiment in invertedRawData:
        count[sentiment] = len(invertedRawData[sentiment])
    return count

def getAvgSentenceLengthOfRawData(invertedRawData):
    totalLen = 0 
    count = 1

    for sentiment in invertedRawData:
        for entry in invertedRawData[sentiment]:
            totalLen = totalLen + len(entry["sentence"])
            count = count + 1

    return totalLen/count


def report(invertedRawData):

    longestLength = lenLongestSentence(invertedRawData)
    count = countForEachSentiment(invertedRawData)
    average = getAvgSentenceLengthOfRawData(invertedRawData)
    print("============== Statistics ==============")
    print("Longest Sentence:"+ str(longestLength))
    for sentiment in count:
        print("Sentiment:" + str(sentiment) + " has "+ str(count[sentiment]) +" lines of sentence")
    print("Average Sentiment Length:" + str(average)) 
    print("========================================")