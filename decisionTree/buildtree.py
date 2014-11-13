#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
# work with python 2.7

from sklearn import tree

class tree_builder:

    def __init__(self):
        """Init the tree."""
        self.tree = tree.DecisionTreeClassifier()
        self.data = {}

    def load_data_from_file(self, path):
        """load data from file"""
        pass

    def load_data_from_dict(self, data):



def main():
    '''main: Main function

    Description goes here.
    '''
    print 'main'


if __name__ == '__main__':
    main()

