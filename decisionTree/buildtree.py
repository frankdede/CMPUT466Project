#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
# work with python 2.7


import argparse
from sklearn import tree
from sklearn.externals.six import StringIO
#from scipy.io.arff import loadarff
import pydot
import sys

import scipy as sp
import numpy as np

class tree_builder:

    def __init__(self, depth = -1):
        """Init the tree."""
        if depth > 0:
            self.tree = tree.DecisionTreeClassifier(max_depth=depth)
        else:
            self.tree = tree.DecisionTreeClassifier()
        self.data = [] 
        self.attr = {}
        self.dot_data = StringIO()
        self.trained = False
    
    def dump_tree(self, path):
        '''Dump the tree object to path'''
        from sklearn.externals import joblib
        joblib.dump(self.tree, path)
    
    def classerify(self, x):
        assert self.trained is True , "You need train data first!"
        return self.tree.predict(x)

    def build_fit_data(self):
        if self.trained == True:
            return 
        for item in self.attr:
            index = self.attr[item]['order']
            if self.attr[item]['reverse']:
                re_index = lambda x: self.attr[item]['re_index'][x]

                for x in xrange(len(self.data)):
                    self.data[x][index] = re_index(self.data[x][index])
            elif self.attr[item]['type'] == "INT":
                for x in xrange(len(self.data)):
                    self.data[x][index] = int(self.data[x][index]) 
            elif self.attr[item]['type'] == 'DOUBLE':
                for x in xrange(len(self.data)):
                    self.data[x][index] = float(self.data[x][index])

        self.trained = True
    
    def fit_part(self, pos, length):
        self.build_fit_data()
       
        end = pos + length if length != -1 else None

        x_func = lambda x: x[:-1]
        y_func = lambda x: str( x[-1:])
        x = map(x_func, self.data[pos:end])
        y = map(y_func, self.data[pos:end])

        self.tree.fit(x, y)

    def fit(self):
        #self.build_fit_data()
        #x_func = lambda x: x[:-1]
        #y_func = lambda x: str( x[-1:])
        #x = map(x_func, self.data)
        #y = map(y_func, self.data)
        
        return self.fit_part(0, -1) 

    def load_data_from_file(self, path):
        """load data from file"""
        self.attr_order = 0;
        current_work = -1 
        for line in open(path,'r'):
            line = line.strip()
            
            if line == "":
                continue

            elif line[0] == "#":
                continue

            elif line[0] == "@":
                #set for current work set
                if line[1:] == "attribute":
                    current_work = 'attr' 
                elif line[1:] == "data":
                    current_work = 'data'
                continue

            else:
                if current_work == -1:
                    print "ERROR IN READ FILE"
                    sys.exit() 
               
                if current_work == 'attr':
                    self.process_attr_line(line)
                elif current_work == 'data':
                    self.process_data_line(line)

    def load_data_from_dict(self, data):
        pass

    def process_data_line(self, line):
        line_set = line.split(",");
        self.data.append(line_set);    

    def process_attr_line(self, line):
        attr_set = line.replace(" ","").split("|")
        
        if len(attr_set) < 2:
            print "ERROR: Parse attribute error with line [%s]" % line
            sys.exit()
        
        attr_dict = {}
        attr_dict['name'] = attr_set[0]
        attr_dict['type'] = attr_set[1]
        attr_dict['order'] = self.attr_order 
        if attr_set[1] == "STRING":
            attr_dict['reverse'] = 1     
            attr_dict['index'] = attr_set[2][1:-1].split(',')
            attr_dict['re_index'] = {} 
            #build reverse index
            for i in xrange(len(attr_dict['index'])):
                p = attr_dict['index'][i]
                attr_dict['re_index'][p] = i
        else:
            attr_dict['reverse'] = 0
        
        self.attr[attr_set[0]] = attr_dict
        self.attr_order += 1

    def build_attr_index(self):   
        r = [None] * len(self.attr)
        for key in self.attr:
            r[self.attr[key]['order']] = key

        return r

    def build_polt(self):
        tree.export_graphviz(self.tree, self.dot_data,
                             self.build_attr_index())

    def plot_pdf(self, path):
        self.build_polt()
        graph = pydot.graph_from_dot_data(self.dot_data.getvalue())
        graph.write_pdf(path)
    
    def plot_png(self, path):
        self.build_polt()

        c = open(".tmp.dot",'w')
        c.write(self.dot_data.getvalue())
        from urllib import urlencode, quote
        import os
        post = "chl=%s&cht=gv" % quote(self.dot_data.getvalue())
        os.popen("curl -d '%s' https://chart.googleapis.com/chart -o %s"
                %( post, path))



def main():

    parser = argparse.ArgumentParser(description='Build Tree and output tree \
            graph')

    parser.add_argument('INPUT', nargs=1, help="Input data file")
    parser.add_argument("OUTPUT", nargs=1, help="Output tree graph pdf")
    parser.add_argument("-d",dest='depth', default=-1 , help="max depth", type=int)    
    args = parser.parse_args(sys.argv[1:])
     
    t = tree_builder(args.depth)
    t.load_data_from_file(args.INPUT[0])
    t.fit()

    t.dump_tree('./tree_dump/tree.pkl')
    t.plot_pdf(args.OUTPUT[0])
    #t.plot_png(args.OUTPUT[0])
        
def test():
    t = tree_builder()
    t.load_data_from_file('test/test1.txt')
    t.fit()
    t.plot_png('test.png')

if __name__ == '__main__':
    main()

