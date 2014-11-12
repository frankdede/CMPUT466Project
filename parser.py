#!/usr/bin/python
import errors
import lines
import sys, getopt, exceptions

def processStopWords(text):
    stopWordsList = []
    for line in text:
        stopWordsList.extend(line.strip('\n').split(' '))

def processRawData(text):


def readArgsFromInput(argv):
    rawDataName,stopWordsName,outputName = None
    try:
        opts, args = getopt.getopt(argv,"hr:s:i1o",["rawdata=","stopwords=","ouput="])
    except getopt.GetoptError:
        print 'run parser.py with flag -h to get help doc' 
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Flags List:'
            print '-h Help'
            print '-r <rawdata_filename> Import rawdata' 
            print '-s <stopwords_filename> Import stopwords'
            print '-o <outputfile_filename> Export results' 
            print '-1 Mode 1: Process raw data without stripping the stopwords'
        elif opt in ("-r","--rawdata"):
            rawDataName = arg
        elif opt in ("-s","--stopwords"):
            stopWordsName = arg
        elif opt in ("-o","--output"):
            outputName = arg
        elif opt in ("-i"):
            # TODO:export stats images
            pass
        elif opt in ("-1"):
            # TODO:Mode 1 -- export
            pass 
        else
            sys.exit(2)

    return rawDataName, stopWordsName, outputName, opts

def main(argv):
    try:
        rawDataName, stopWordsName, outputName, opts = readArgsFromInput(argv)
        rawData = open(rawDataName,'r')
        stopWords = open(stopWordsName,'r')
    except IOError as e:
        print "Cannot read:",fileName
    except:
        print "Unexpected error"

if __name__ == "__main__":
    main(sys.argv[1:])