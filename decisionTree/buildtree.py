#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
# work with python 2.7


import argparse
from sklearn import tree
from sklearn.externals.six import StringIO
import pydot
import sys
import gzip
from hashlib import sha1


class tree_builder:

    def __init__(self, depth=-1):
        """Init the tree."""
        if depth > 0:
            self.tree = tree.DecisionTreeClassifier(max_depth=depth)
        else:
            self.tree = tree.DecisionTreeClassifier()

        self.attr_size = 0
        self.feature_size = 0
        self.data_size = 0
        self.data = []
        self.attr = {}
        self.dot_data = StringIO()
        self.trained = False

    def dump_tree(self, path):
        '''Dump the tree object to path'''
        from sklearn.externals import joblib
        joblib.dump(self.tree, path)

    def classerify(self, x):
        assert self.trained is True, "You need train data first!"
        return self.tree.predict(x)

    def build_fit_data(self):
        if self.trained:
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

    def cross_validation_test(self, chunk_count, index):
        self.build_fit_data()

        data_length = len(self.data)
        left = (data_length / chunk_count) * index
        right = (data_length / chunk_count) * (index + 1)

        data_set = []
        for i in xrange(data_length):
            if i < left or i >= right:
                data_set.append(self.data[i])

        x_func = lambda x: x[:-1]
        y_func = lambda x: str(x[-1:])
        x = map(x_func, data_set)
        y = map(y_func, data_set)

        self.tree.fit(x, y)

    def fit_part(self, pos, length):
        self.build_fit_data()

        end = pos + length if length != -1 else None

        x_func = lambda x: x[:-1]
        y_func = lambda x: str(x[-1:])
        x = map(x_func, self.data[pos:end])
        y = map(y_func, self.data[pos:end])

        self.tree.fit(x, y)

    def fit(self):
        # self.build_fit_data()
        #x_func = lambda x: x[:-1]
        #y_func = lambda x: str( x[-1:])
        #x = map(x_func, self.data)
        #y = map(y_func, self.data)

        return self.fit_part(0, -1)

    def load_data_from_file(self, path, g=False, duplicate=0):
        """load data from file 
            when duplicate = 0, do not remove duplicate   
            duplicate = 1, remove same feature with same socre
            duplicate = 2, remove same feature and average duplicate socre
        """
        self.attr_order = 0
        current_work = -1

        if duplicate:
            self.duplicate_set = {}
            print "Work in duplicate reduce mode [%d]" % duplicate
        if g:
            fp = gzip.open(path)
        else:
            fp = open(path)

        for line in fp:
            line = line.strip()

            if line == "":
                continue

            elif line[0] == "#":
                continue

            elif line[0] == "@":
                # set for current work set
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
                    self.attr_size += 1
                    self.process_attr_line(line)
                elif current_work == 'data':
                    self.process_data_line(line, duplicate)

        # update the socre with duplicate == 2
        if duplicate == 1:
            self.duplicate_set = dict(filter(lambda (k, v): v > 1,
                                      self.duplicate_set.iteritems()))

        elif duplicate == 2:
            # update the socre for duplicate item
            self.duplicate_set = dict(filter(lambda (k, v): v['count'] > 1,
                                      self.duplicate_set.iteritems()))
            for hash, record in self.duplicate_set.iteritems():
                average_score = sum(record['score']) / record['count']

                # convert score to int
                average_score = int(average_score)

                index = self.data.index(record['record'])
                self.data[index][-1] = str(average_score)

        fp.close()

    def load_data_from_dict(self, data):
        pass

    def process_data_line(self, line, duplicate):
        line_set = line.split(",")

        if len(line_set) != self.attr_size:
            raise Exception("feature size[%d] not match attribute size[%d]"
                            % (len(line_set), self.attr_size))

        if duplicate == 1:   # remove duplicate feature with same socre
            hash = sha1("".join(line_set)).hexdigest()
            if hash in self.duplicate_set:
                self.duplicate_set[hash] += 1
                return

            else:
                self.duplicate_set[hash] = 1

        elif duplicate == 2:   # remove duplicate feature then average socre
            hash = sha1("".join(line_set[:-1])).hexdigest()
            if hash in self.duplicate_set:
                self.duplicate_set[hash]['count'] += 1
                self.duplicate_set[hash]['score'].append(int(line_set[-1]))
                return

            else:
                self.duplicate_set[hash] = {}
                self.duplicate_set[hash]['count'] = 1
                self.duplicate_set[hash]['score'] = [int(line_set[-1])]
                self.duplicate_set[hash]['record'] = line_set

        self.data_size += 1
        self.data.append(line_set)

    def process_attr_line(self, line):
        attr_set = line.replace(" ", "").split("|")

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
            # build reverse index
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

        c = open(".tmp.dot", 'w')
        c.write(self.dot_data.getvalue())
        graph = pydot.graph_from_dot_data(self.dot_data.getvalue())
        graph.write_pdf(path)

    def plot_png(self, path):
        self.build_polt()

        c = open(".tmp.dot", 'w')
        c.write(self.dot_data.getvalue())
        from urllib import quote
        import os
        post = "chl=%s&cht=gv" % quote(self.dot_data.getvalue())
        os.popen("curl -d '%s' https://chart.googleapis.com/chart -o %s"
                 % (post, path))


def main():

    parser = argparse.ArgumentParser(description='Build Tree and output tree \
            graph')

    parser.add_argument('INPUT', nargs=1, help="Input data file")
    parser.add_argument("OUTPUT", nargs=1, help="Output tree graph pdf")
    parser.add_argument(
        "-d", dest='depth', default=-1, help="max depth", type=int)
    parser.add_argument('-g', default=False, action='store_true')
    args = parser.parse_args(sys.argv[1:])

    t = tree_builder(args.depth)
    t.load_data_from_file(args.INPUT[0], args.g)
    t.fit()

    t.dump_tree('./tree_dump/tree.pkl')
    t.plot_pdf(args.OUTPUT[0])
    # t.plot_png(args.OUTPUT[0])


def test():
    from sklearn import cross_validation as cv
    t = tree_builder()
    t.load_data_from_file("./freq_train-1.txt")
    test_y = map(lambda x:x[-1],t.data)
    test_x = map(lambda x:x[:-1],t.data)
    X_train, X_test, y_train, y_test = cv.train_test_split(test_x,test_y, test_size=0.2, random_state=0)
    t.tree.fit(X_train,y_train)
    out = t.tree.predict(X_test)
    total_correct = 0
    for i in range(len(out)):
        if out[i] == y_test[i]:
            total_correct += 1
    print("randomly select:", float(total_correct) / len(out))
    scores = cv.cross_val_score(t.tree, test_x, test_y, cv=5)
    print("Fixed CV:", scores)

if __name__ == '__main__':
    main()
