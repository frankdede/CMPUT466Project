#!/usr/bin/python
import operator
from tools import out
from sklearn.feature_extraction.text import TfidfVectorizer

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
        answer[i] = [sum(answer[i])/float(len(answer[i])), len(answer[i])]

    sortedAvg = sorted(answer.items(), key=lambda (k, v): v[1], reverse = True)
    print("Done")
    return sortedAvg, list(answer.keys())

def getTFIDF(rawData):
    print("============== Getting tf-idf ==============")
    list = []
    for entry in rawData:
        sentence = " ".join(entry["sentence"])
        list.extend(sentence)

    tfidf = TfidfVectorizer()
    response = tfidf.fit_transform(list)
    words = tfidf.get_feature_names()
    dict = {}
    for i in response.nonzero()[1]:
        dict[words[i]] = response[0,i]
    return dict




