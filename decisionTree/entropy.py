import math
import operator
def calcEntropyValue(dataSet):
	numEntries=len(dataSet)
	labelCounts={}
	for featVec in dataSet:
		currentLabel=featVec[-1]
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel]=0
		labelCounts[currentLabel]+=1
	Ent=0.0
	for key in labelCounts:
		prob =float(labelCounts[key])/numEntries
		Ent-=prob*math.log(prob,2)
	return Ent 
