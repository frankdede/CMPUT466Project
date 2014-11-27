#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
# work with python 2.7

from buildtree import tree_builder
import gzip
import argparse
import sys


def load_test_data(path, tree):

    test_data = {}
    for i in open(path):
        p_set = i.strip().split(',')

        if len(p_set) != tree.attr_length:
            raise Exception("Test data feature length not equal to",
                            " attr length")

        test_id = int(p_set[0])
        data = map(float, p_set[0])
        test_data[test_id] = {'data': data, 'result': None}

    return test_data


def main():
    '''main: Main function

    Description goes here.
    '''
    parser = argparse.ArgumentParser(description='Get socre from test files.')
    parser.add_argument('TRAIN_INPUT', nargs=1, help="Input data file")
    parser.add_argument('TEST_INPUT', nargs=1)
    parser.add_argument("OUTPUT", nargs=1, help="Output tree graph pdf")
    parser.add_argument(
        "-d", dest='depth', default=-1, help="max depth", type=int)
    parser.add_argument('-g', default=False, action='store_true')
    args = parser.parse_args(sys.argv[1:])

    t = tree_builder(args.depth)
    t.load_data_from_file(args.TRAIN_INPUT[0], args.g)

    test_data = load_test_data(args.TEST_INPUT[0], t)

    print "Finish load test_data with %d entries" % len(test_data)

    for i in test_data:
        result = t.classerify(test_data[i]['data'])

        test_data[i]['result'] = result

    print "Finish classification"

    fp = open(args.OUTPUT[0], "w")

    for i in sorted(test_data.keys()):
        fp.write("%s,%s\n" % (i, test_data[i]['result']))

    fp.close()

    print "Done!"


if __name__ == '__main__':
    main()
