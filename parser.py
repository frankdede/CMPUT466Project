#!/usr/bin/python

import sys, getopt, exceptions, re, time 
import json
from bigram import bigram
from unigram import unigram
from stats import stats
from tools import splitter, generator ,out
from nltk.stem.lancaster import LancasterStemmer

def timeExec(func):
    def wrapper(*arg):
        start = time.clock()
        a = func(*arg)
        end =time.clock()
        print 'used:', end - start
        return a
    return wrapper

def writeFile(name,content):
    print("====== Writing '"+ name +"' to the disk ======")
    output = open(name, 'w')
    output.write(content)
    output.close()    
    print("Done")
    
def createStopWordsList(text):
    stopWordsList = []

    for line in text:
        stopWordsList.extend(unicode(line, errors='ignore').strip('\n').split())
    return stopWordsList


def extractRawTrainingData(text, stopWords, stemming):
    st = LancasterStemmer()
    rawData = []
    text.readline()
    print("********** Extract From Raw Training Data **********")

    if stopWords:
        sign = 'ON'
    else:
        sign = 'OFF'
    print("Stopwords:" + sign)

    if stemming:
        sign = 'ON'
    else:
        sign = 'OFF'
    print("Stemming:" + sign)

    prevId = 0
    print("Extracting...")
    for line in text:

        lineTokens = line.strip('\n').split('\t')
        sentenceId = int(lineTokens[1])

        if sentenceId > prevId:

            prevId = sentenceId
            sentenceStr = lineTokens[2]
            sentiment = int(lineTokens[3])

            sentenceTokens = re.sub("\s+", " ", sentenceStr).split(' ')

            if stemming:
                sentenceTokens = map(lambda x:unicode(st.stem(x).lower()),sentenceTokens)
            else:
                sentenceTokens = map(lambda x:unicode(x.lower()),sentenceTokens)

            sentenceTokens = stripWords(sentenceTokens,stopWords)
            entry = {"sentenceId":sentenceId, "sentence":sentenceTokens, "sentiment":sentiment}
            rawData.append(entry)

    print("Done")
    return rawData
        
#@timeExec
def extractRawTestData(text):

    testData = []
    text.readline()
    print("********** Extracting From Raw Test Data **********")
    print("Extracting...")
    for line in text:

        lineTokens = line.strip('\n').split('\t')

        pharseId = int(lineTokens[0])
        sentenceStr = lineTokens[2]

        sentenceTokens = re.sub("\s+"," ",sentenceStr).split(' ')
        sentenceTokens = map(lambda x:unicode(x.lower()),sentenceTokens)
        entry = {"pharseId":pharseId,"sentence":sentenceTokens}
        testData.append(entry)

    print("Done")
    return testData

def createInvertedTestData(text):
    return createInvertedTrainingData(text, None, None);


def createInvertedTrainingData(text, stopWords, stemming):
    st = LancasterStemmer()

    invertedRawData = {}
    text.readline()
    print("********** Create Inverted Raw Training Data **********")
    
    if stopWords:
        sign = 'ON'
    else:
        sign = 'OFF'
    print("Stopwords:" + sign)

    if stemming:
        sign = 'ON'
    else:
        sign = 'OFF'
    print("Stemming:" + sign)
    print("Creating...")

    for line in text:
        # Split line
        lineTokens = line.strip('\n').split('\t')

        # get PharseId
        pharseId = int(lineTokens[0])

        # get SentenceId
        sentenceId = int(lineTokens[1])

        # get sentence
        sentenceStr = lineTokens[2]

        # get sentiment
        sentiment = int(lineTokens[3])

        # replace one or more spaces by single space
        # then split
        sentenceTokens = re.sub("\s+"," ",sentenceStr).split()
        
        if stemming:
            sentenceTokens = map(lambda x:unicode(st.stem(x).lower()),sentenceTokens)
        else:
            sentenceTokens = map(lambda x:unicode(x.lower()),sentenceTokens)

        sentenceTokens = stripWords(sentenceTokens,stopWords)
        
        # create a sentiment key if doesn't exist
        entry = {"pharseId":pharseId,"sentenceId":sentenceId,"sentence":sentenceTokens}

        if sentiment in invertedRawData:
            # append the sentence to its corresponding sentiment list
            invertedRawData[sentiment].append(entry)
        else:
            invertedRawData[sentiment] = []
            invertedRawData[sentiment].append(entry)
    print("Done")
    return invertedRawData



def stripWords(sentenceTokens,wordsList):
    
    return filter(lambda x: x not in wordsList, sentenceTokens)

def readArgsFromInput(argv):
    testDataName = rawDataName = stopWordsName = outputName = directory = None 
    # Record the flags that user are using
    usedOpts = []
    try:
        opts, args = getopt.getopt(argv,"hr:s:mio:t:",["rawdata=","stopwords=","ouput=","testdata="])
    except getopt.GetoptError:
        print 'run parser.py with flag -h to get help doc' 
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print 'Flags List:'
            print '-h Help' 
            print '-r <rawdata_filename> Import raw training data file' 
            print '-s <stopwords_filename> Import stopwords file'
            print '-m Stemming enabled'
            print '-t <test_filename> Import test data file'
            print "-o <outputfile_filename> Define the name of output file.(It's named as no_stopwords.txt by default)"
            sys.exit()

        elif opt in ("-r", "--rawdata"):
            rawDataName = arg
            usedOpts.append('-r')

        elif opt in ("-s", "--stopwords"):
            stopWordsName = arg
            usedOpts.append('-s')

        elif opt in ("-m", "--stemming"):
            usedOpts.append('-m')

        elif opt in ("-t", "--testdata"):
            testDataName = arg
            usedOpts.append('-t')

        elif opt in ("-o", "--output"):
            outputName = arg
            usedOpts.append('-o')

        elif opt in ("-i"):
            usedOpts.append('-i')
            # TODO:export stats images
            pass
        else:
            sys.exit("Invalid Flag(s)")

    # pareser wihout flag -o, then the output will be named as this by default
    if '-o' not in usedOpts:
        outputName = 'default_invertedRawdata.json'

    # cannot proceed without filename of raw data
    if rawDataName == None or stopWordsName == None or testDataName == None:
        sys.exit("Cannot proceed wihout the raw data and/or stopwords")

    return testDataName, rawDataName, stopWordsName, outputName, usedOpts
def main(argv):
    
    testDataName, rawDataName, stopWordsName, outputName, usedOpts = readArgsFromInput(argv)
    # load raw data
    try:
        rawDataFile = open(rawDataName,'r')
        rawTestDataFile = open(testDataName,'r')
        stopWordsFile = open(stopWordsName,'r')

        # create stopwords list
        stopWordsList = createStopWordsList(stopWordsFile)
        # create invertedRawData
        if '-m' in usedOpts:
            stemming = True
        else:
            stemming = False

        invertedRawData = createInvertedTrainingData(rawDataFile, stopWordsList, stemming)
        rawDataFile.close()

        rawDataFile = open(rawDataName,'r')
        # extract rawData from rawDataFile
        rawTrainingData = extractRawTrainingData(rawDataFile, stopWordsList, stemming)
        rawDataFile.close()

        average, featuresList = stats.getWordAverageSentiment(rawTrainingData, 50)

        out.saveWordSentiment(average, "average.txt")
            
        # Now bag of words is ready for feature construction
        #generator.createFeatureBagMatrix(rawTrainingData,featuresList)
        
        # extract the bigrams from inverted raw data
        bigramsInvertedCollection = bigram.extractBigramsFromInvertedRawData(invertedRawData)
        biFreqDist = bigram.getFrequencyDist(bigramsInvertedCollection)

        #extract the unigrams from inverted raw data
        #unigramsInvertedCollection = unigram.extractUnigramsFromInvertedRawData(invertedRawData)
        #uniFreqDist = bigram.getFrequencyDist(unigramsInvertedCollection)
        
        # extract the bigrams from raw data
        bigramsRawData = bigram.extractBigramsFromRawData(rawTrainingData)

        # bigram sentences by n
        splitedBigramRawData = splitter.splitSentence(3,bigramsRawData)
        generator.createFreqMatrix(3, splitedBigramRawData, biFreqDist)
        
        rawTestData = extractRawTestData(rawTestDataFile)
        bigramsRawData = bigram.extractBigramsFromRawData(rawTestData)
        splitedBigramRawData = splitter.splitSentence(3, bigramsRawData)
        #generator.createFreqMatrix(3, splitedBigramRawData, biFreqDist, isTestData = True)

        rawDataFile.close()
        stopWordsFile.close()
        rawTestDataFile.close()

    except IOError as e:
        print "Cannot read raw data file or stop-word file" 
if __name__ == "__main__":
    main(sys.argv[1:])
