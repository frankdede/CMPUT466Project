def saveWordSentiment(list,name):
    with open(name,'w') as f:
        for entry in list:
            f.write("%s %f %d \n" %(entry[0],entry[1][0],entry[1][1]))
    f.close()
