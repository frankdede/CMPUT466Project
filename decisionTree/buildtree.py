#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
# work with python 2.7


import argparse
from sklearn import tree
from sklearn.externals.six import StringIO
import pydot

class tree_builder:

    def __init__(self):
        """Init the tree."""
        self.tree = tree.DecisionTreeClassifier()
        self.data = {}
        self.dot_data = StringIO()

    def load_data_from_file(self, path):
        """load data from file"""
        pass

    def load_data_from_dict(self, data):
        pass

    def plot_pdf(self, path):
        tree.export_graphviz(self.tree, self.dot_data)

        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        graph.write_pdf(path)


def main():
   
    parser = argparse.ArgumentParser(description='Build Tree and output tree \
            graph')

    parser.add_argument('INPUT', help="Input data file")
    parser.add_argument("OUTPUT", help="Output tree graph pdf")

    args = parser.parse_args()

    t = tree_builder()


if __name__ == '__main__':
    main()

