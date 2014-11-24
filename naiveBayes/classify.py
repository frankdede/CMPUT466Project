from sklearn.naive_bayes import GaussianNB
class naiveBayes:
	gnb = None
	x = []
	y = []
	def __init__(self,filename):
		self.gnb = GaussianNB()
		with open(filename) as f:
			for line in f:
				if line[0]>='0' and line[0]<='9':
					tmp = line.strip('\n').split(',')
					tmp = map(lambda x:float(x),tmp)
					self.x.append(tmp[:-1])
					self.y.append(tmp[-1])
	def train(self):
		self.gnb.fit(self.x,self.y)
	def predict(self,input):
		return self.gnb.predict(input)
if __name__ == '__main__':
	nb = naiveBayes("../decisionTree/trainingSet/train_500.txt");
	nb.train()
	print(nb.predict(nb.x[0]))
