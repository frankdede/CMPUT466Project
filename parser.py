#!/usr/bin/python
import sys, getopt, exceptions, re
import nltk
import json

def createStopWordsList(text):
    stopWordsList = []
    for line in text:
        stopWordsList.extend(line.strip('\n').split(' '))
    return stopWordsList

def createInvertedRawData(text, stopWords = None):
    invertedRawData = {}
    text.readline()
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
        sentenceTokens = re.sub("\s+"," ",sentenceStr).split(' ')

        # if stopwords are required, do the following
        if stopWords:
            sentenceTokens = stripWords(sentenceTokens,stopWords)
        
        # create a sentiment key if doesn't exist
        entry = {"pharseId":pharseId,"sentenceId":sentenceId,"sentence":sentenceTokens}

        if sentiment in invertedRawData:
            # append the sentence to its corresponding sentiment list
            invertedRawData[sentiment].append(entry)
        else:
            invertedRawData[sentiment] = []
            invertedRawData[sentiment].append(entry)

    return invertedRawData

def stripWords(sentenceTokens,wordsList):

    for word in wordsList:
        if word in sentenceTokens:
            sentenceTokens.remove(word)
    return sentenceTokens

def readArgsFromInput(argv):
    rawDataName = stopWordsName = outputName = directory = None 
    # Record the flags that user are using
    usedOpts = []
    try:
        opts, args = getopt.getopt(argv,"hr:s:i1o",["rawdata=","stopwords=","ouput="])
    except getopt.GetoptError:
        print 'run parser.py with flag -h to get help doc' 
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print 'Flags List:'
            print '-h Help' 
            print '-r <rawdata_filename> Import raw data file' 
            print '-s <stopwords_filename> Import stopwords file'
            print "-o <outputfile_filename> Define the name of output file.(It's named as no_stopwords.txt by default)"
            print '-1 Mode 1: Process raw data without stripping the stopwords'
            sys.exit()

        elif opt in ("-r","--rawdata"):
            rawDataName = arg
            usedOpts.append('-r')

        elif opt in ("-s","--stopwords"):
            stopWordsName = arg
            usedOpts.append('-s')

        elif opt in ("-o","--output"):
            outputName = arg
            usedOpts.append('-o')

        elif opt in ("-i"):
            usedOpts.append('-i')
            # TODO:export stats images
            pass
        elif opt in ("-1"):
            usedOpts.append('-1')
            # TODO:Mode 1 -- Process raw data without stripping the stopwords
            pass 
        else:
            sys.exit("Invalid Flag(s)")

    # pareser wihout flag -o, then the output will be named as this by default
    if '-o' not in usedOpts:
        outputName = 'default_invertedRawdata.json'

    # cannot proceed without filename of raw data
    if rawDataName == None:
        sys.exit("Cannot proceed wihout the filename of raw data")

    return rawDataName, stopWordsName, outputName, usedOpts

def main(argv):
    
    rawDataName, stopWordsName, outputName, usedOpts = readArgsFromInput(argv)
    # load raw data
    try:
        rawDataFile = open(rawDataName,'r')
        
        # parser is in mode 1 then prcoess raw data without stripping the stopwords
        if '-1' in usedOpts:
            invertedRawData = createInvertedRawData(rawDataFile)
        else:
            stopWordsFile = open(stopWordsName,'r')
            stopWordsList = createStopWordsList(stopWordsFile)
            invertedRawData = createInvertedRawData(rawDataFile,stopWordsList)
            stopWordsFile.close()
        
        jsonRawData = json.dumps(invertedRawData)
        
        rawDataFile.close()
        output = open(outputName, 'w')
        output.write(jsonRawData)
        output.close()
        
    except IOError as e:
        print "Cannot read raw data file or stop-word file" 

if __name__ == "__main__":
    main(sys.argv[1:])