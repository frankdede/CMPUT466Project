#!/usr/bin/python
import nltk
import numpy
import StringIO
from subprocess import call

def createFreqMatrix(n,splitedRawData,freqLookupData,isTestData = False):

    dtype = 'f4,' * n
    size = (len(splitedRawData))

    if isTestData:
        print("============= Create Frequency Test Set ==============")
        # exclude the last comma
        dtype = dtype[0:-1]
    else:
        print("============== Create Frequency Training Set ==============")
        # add a1 type to dtype
        dtype = dtype + 'a1'

    print("Creating...")

    # create placeholder based on size and dtype info
    freqMatrix = numpy.zeros(size,dtype = (dtype))

    for entry in range(len(splitedRawData)):
        size = (1,len(splitedRawData[entry]['sentence']))
        for part in range(len(splitedRawData[entry]['sentence'])):
            total = 0;
            for gram in splitedRawData[entry]['sentence'][part]:
                f0 = freqLookupData[0].freq(gram)
                f1 = freqLookupData[1].freq(gram)
                f2 = freqLookupData[2].freq(gram)
                f3 = freqLookupData[3].freq(gram)
                f4 = freqLookupData[4].freq(gram)
                values = [f0,f1,f2,f3,f4]

                # find the highest value
                highestSentiment = values.index(max(values))
            # sum up
            total += highestSentiment

            partAverage = total/float(len(splitedRawData[entry]['sentence']))
            freqMatrix[entry][part] = partAverage
        
        if not isTestData:
            freqMatrix[entry][n] = str(splitedRawData[entry]['sentiment'])

        # print(entry,freqMatrix[entry][n])
    if not isTestData:
        header = StringIO.StringIO()
        header.write("@attribute\n");
        for i in range(n):
            header.write("part" + str(i+1)+"|DOUBLE|\n")
        header.write("sentiment|STRING|{0,1,2,3,4}\n");
        header.write("\n@data");

        saveMatrix('freq_test', freqMatrix, header.getvalue())
    else:
        saveMatrix('freq_train', freqMatrix)

    print("Done")

def createFeatureBagMatrix(splitedRawData,totalLabelSet=None):
    print("============== Create Bag of Words Training Set ==============")
    header = StringIO.StringIO()
    if(totalLabelSet==None):
        totalLabelSet = set()
        for sentence in splitedRawData:
            totalLabelSet = totalLabelSet.union(set(sentence['sentence']))

    header.write("@attribute\n");
    map(lambda x:header.write(x+"|DOUBLE|\n"),totalLabelSet)
    header.write("sentiment|STRING|{0,1,2,3,4}\n");
    header.write("\n@data");

    matrix_list= list()
    for sentence in splitedRawData:
        tmp = map(lambda x:1 if x in sentence['sentence'] else 0,totalLabelSet)
        tmp.append(sentence["sentiment"])
        matrix_list.append(tmp)
    matrix_array = numpy.array(matrix_list)
    matrix = numpy.matrix(matrix_array)
    print(matrix.shape)
    print("Done")
    saveMatrix("bag_train", matrix, header.getvalue())
    header.close()
    

def saveMatrix(fileName,matrix,header=None):
    print("~~~~~~~~~~~ Saving '" + fileName + "'~~~~~~~~~~~")
    if header is None:
        numpy.savetxt(fileName, matrix, delimiter=",",fmt="%s")
    else:
        numpy.savetxt(fileName, matrix, delimiter=",",header=header,fmt="%s")
    print("Done")
    removeHashTag(fileName,fileName + ".txt")
    

def removeHashTag(inputName, outputName):
    print("~~~~~~~~~~~ Removing Hash Tags From '" + inputName + "'~~~~~~~~~~~")
    f = open(outputName,'w')
    call(["sed", "s/# //",inputName], stdout = f)
    print("Cleanning temporary files ...")
    call(["rm",inputName])
    print("Done")

if __name__ == '__main__':
    rawData = [{'sentiment':1,'sentence':["My","name","is","frank","huang",".","lalal","dads","dsddsa"]}]
    rawData.append({'sentiment':2,'sentence':["I","like","this","food"]})
    print(createFeatureBagMatrix(rawData))
