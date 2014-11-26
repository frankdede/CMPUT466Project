from sklearn import svm
import numpy as nu
import sys
from sklearn import cross_validation as cv
from sklearn import metrics
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
	def crossValidate(self,test_size=None):
		if len(self.x)==0 or len(self.y) ==0:
			sys.stderr.write("Uninitialized object")
			return
		crossv = cv.ShuffleSplit(len(self.x), n_iter=3,test_size=0.3, random_state=0)
		print(crossv)
		scores = cv.cross_val_score(self.clf,self.x,self.y,cv=crossv)
		#clf = self.clf.fit(X_train, y_train)
		return scores 
if __name__ == "__main__":
	svm = SVM("../decisionTree/trainingSet/train_500.txt")
	svm.train()
	#for size in range(2,11):
	print("test size:",svm.crossValidate())
