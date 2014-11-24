#!/usr/bin/python
import operator

def lenLongestSentence(invertedRawData):
    longestLen = 0
    for sentiment in invertedRawData:
        print sentiment
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
    
    print("Longest Sentence:"+ str(longestLength))
    for sentiment in count:
        print("Sentiment:" + str(sentiment) + " has "+ str(count[sentiment]) +" lines of sentence")
    print("Average Sentiment Length:" + str(average)) 
    print("========================================")


def getWordAverageSentiment(rawData, threshold):
    print("============== Getting Word Average Sentiment ==============")
    answer = {}
    for entry in rawData:
        sentiment = entry['sentiment']
        for token in entry['sentence']:
            if token in answer:
                answer[token].append(sentiment)
            else:
                answer[token] = [sentiment]
    answer = {k :v for k, v in answer.items() if len(v) > threshold}
    for i in answer:
        answer[i] = [sum(answer[i])/float(len(answer[i])),len(answer[i])]

    sortedAvg = sorted(answer.items(), key=lambda (k, v): v[1], reverse = True)
    print("Done")
    return sortedAvg