from sklearn import svm
x= [[0,0],[1,2]]
y = [0,1]
clf = svm.SVC()
clf.fit(x,y)
clf.predict([[2,2]])