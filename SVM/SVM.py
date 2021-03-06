from sklearn import svm
import numpy as nu
import sys
from sklearn import cross_validation as cv
from sklearn import metrics
class SVM:
	x=[]
	y=[]
	labels=[0,1,2,3,4]
	clf = None
	def __init__(self,filename):
		is_attr = False;
		with open(filename) as f:
			for line in f:
				if line == '@attribute\n':
					is_attr = True
				if line == '@data\n':
					is_attr = False
					continue
				if is_attr: continue
				tmp = line.strip('\n').split(',')
				tmp = map(lambda x:float(x),tmp)
				self.x.append(tmp[:-1])
				self.y.append(tmp[-1])
		print(len(self.x))
		self.clf = svm.SVC()
		print(self.labels)
	def train(self):
		self.clf.fit(self.x,self.y)
	def predict(self,input):
		return self.clf.predict(input)
	def crossValidate(self,test_size=None,confusion_matrux=False):
		if len(self.x)==0 or len(self.y) ==0:
			sys.stderr.write("Uninitialized object")
			return
		#randomly draw from sample
		X_train, X_test, y_train, y_test = cv.train_test_split(self.x, self.y, test_size=0.2, random_state=0)
		self.clf.fit(X_train,y_train)
		out = self.predict(X_test)
		if confusion_matrux:
			self.comput_confusion_matrix(out,y_test)
		total_correct = 0
		for i in range(len(out)):
			if out[i] == y_test[i]:
				total_correct +=1
		return float(total_correct)/len(out)
	def comput_confusion_matrix(self,y_out,y_test):
		matrix = nu.zeros((len(self.labels),len(self.labels)),dtype=nu.int)
		for i in xrange(len(y_out)):
			matrix[y_test[i]][y_out[i]] +=1
		print "     0   1   2   3   4 predict value"
		for row_label, row in zip(self.labels, matrix):
			print '%s [%s]' % (row_label, ' '.join('%03s' % i for i in row))
		print "Expected"
if __name__ == "__main__":
	#svm = SVM("../decisionTree/trainingSet/train_500.txt")
	svm = SVM("bag_train.txt")
	svm.train()
	#for size in range(2,11):
	print("Overall correct percentage:",svm.crossValidate(confusion_matrux=True))
