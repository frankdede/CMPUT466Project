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


def getWordAverageScore(rawData):
    answer=[]
    for entry in range(len(rawData)):
        sentiment = entry['sentiment']
        for token in range(len(entry["sentence"])):
            if token in answer:
                answer[token].append(score)
            else:
                answer[token] = [score]
    for i in answer:
        answer(i) = sum(answer[i])/len(answer[i])

    return answer