from sklearn.naive_bayes import GaussianNB
import numpy as nu
import sys
from sklearn import cross_validation as cv
from sklearn import metrics
class naiveBayes:
	gnb = None
	x = []
	y = []
	labels=[0,1,2,3,4]
	def __init__(self,filename):
		self.gnb = GaussianNB()
		with open(filename) as f:
			is_attr = False;
			for line in f:
				if line == '@attribute\n':
					is_attr = True
				if line == '@data\n':
					is_attr = False
					continue
				if is_attr: continue
				if line[0]>='0' and line[0]<='9':
					tmp = line.strip('\n').split(',')
					tmp = map(lambda x:float(x),tmp)
					self.x.append(tmp[:-1])
					self.y.append(tmp[-1])
	def train(self):
		self.gnb.fit(self.x,self.y)
	def predict(self,input):
		return self.gnb.predict(input)
	def crossValidate(self,test_size=None,confusion_matrux=False):
		if len(self.x)==0 or len(self.y) ==0:
			sys.stderr.write("Uninitialized object")
			return
		#randomly draw from sample
		X_train, X_test, y_train, y_test = cv.train_test_split(self.x, self.y, test_size=0.2, random_state=0)
		self.gnb.fit(X_train,y_train)
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
if __name__ == '__main__':
	#nb = naiveBayes("../decisionTree/trainingSet/train_500.txt");
	nb = naiveBayes("bag_train.txt")
	nb.train()
	print("Overall correct percentage:",nb.crossValidate(confusion_matrux=True))
