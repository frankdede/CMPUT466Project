import nltk

def getOccuranceRateForTuple(tuple,bigramsCollection):
    rate = {}
    for sentiment in bigramsCollection:
        freqDist = FreqDist(bigramsCollection[bigramsCollection])
        rate[sentiment] = 


def extractBigram(invertedWords):
    bigramsCollection = {}
    for sentiment in invertedWords:
        if sentiment not in bigramsCollection:
            bigramsCollection = {sentiment:[]}

        for entry in invertedWords[sentiment]:
            # E.g. the bigrams of ['a','b','c']
            # will look like this [('a', 'b'), ('b', 'c'), ('c', 'd')]
            bigramsTupleList= list(nltk.bigrams(entry['sentence']))
            bigramsCollection[sentiment].extend(bigramsTupleList)
    return bigramsCollection