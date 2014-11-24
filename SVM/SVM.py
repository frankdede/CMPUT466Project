from sklearn import svm
import numpy as nu
class SVM:
	x=[]
	y=[]
	clf = None
	def __init__(self,filename):
		with open(filename) as f:
			for line in f:
				if(line[0]>='0' and line[0]<='9'):
					#print(line)
					tmp = line.strip('\n').split(',')
					tmp = map(lambda x:float(x),tmp)
					self.x.append(tmp[:-1])
					self.y.append(tmp[-1])
		self.clf = svm.SVC()
	def train(self):
		self.clf.fit(self.x,self.y)
	def predict(self,input):
		return self.clf.predict(input)
if __name__ == "__main__":
	svm = SVM("../decisionTree/trainingSet/train_500.txt")
	svm.train()
	print(svm.x[0])
	print(svm.predict(svm.x[0]))
