#!/usr/bin/python
import nltk
import numpy
import StringIO
def createFreqMatrix(n,splitedRawData,freqLookupData):
    print("====== Creating Frequency Training Set ======= ")
    size = (len(splitedRawData))
    
    freqMatrix = numpy.zeros(size,dtype = ('f4,f4,f4,a1'))

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
            # get 
            partAverage = total/float(len(splitedRawData[entry]['sentence']))
            freqMatrix[entry][part] = partAverage
        
        freqMatrix[entry][n] = str(splitedRawData[entry]['sentiment'])
        print(entry,freqMatrix[entry][n])
    
    saveMatrix('matrix.txt',freqMatrix,None)
    print("Done")

def createFeatureBagMatrix(splitedRawData,totalLabelSet=None):
    print("============== Creating Bag of Words Matrix ==============")

    if(totalLabelSet!=None):
        totalLabelSet = set()
        header = StringIO.StringIO()
        for sentence in splitedRawData:
            totalLabelSet = totalLabelSet.union(set(sentence['sentence']))

    header.write("@attribute\n");
    map(lambda x:header.write(x+"|DOUBLE|\n"),totalLabelSet)
    header.write("sentiment|DOUBLE|{0,1,2,3,4}\n");
    header.write("\n@data\n");

    matrix_list= list()
    for sentence in splitedRawData:
        tmp = map(lambda x:1 if x in sentence['sentence'] else 0,totalLabelSet)
        tmp.append(sentence["sentiment"])
        matrix_list.append(tmp)
    matrix_array = numpy.array(matrix_list)
    matrix = numpy.matrix(matrix_array)
    print(matrix.shape)
    saveMatrix("matrix2.txt",matrix,header.getvalue())
    header.close()

    print("Done")
    return matrix

def saveMatrix(fileName,matrix,header):
    if header is None:
        numpy.savetxt(fileName, matrix, delimiter=",",fmt="%s")
    else:
        numpy.savetxt(fileName, matrix, delimiter=",",header=header,fmt="%s")

if __name__ == '__main__':
    rawData = [{'sentiment':1,'sentence':["My","name","is","frank","huang",".","lalal","dads","dsddsa"]}]
    rawData.append({'sentiment':2,'sentence':["I","like","this","food"]})
    print(createFeatureBagMatrix(rawData))
