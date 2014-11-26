#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
# work with python 2.7

import sys
import argparse
import buildtree as bt


def get_accuray_socre(t, pos, length, size):
    data_length = len(t.data)
    end = pos + length

    right = 0.0
    wrong_set = {}
    index = t.attr['sentiment']['index']
    for i in index:
        wrong_set[i] = {}
        for j in index:
            wrong_set[i][j] = 0

    for i in range(data_length):
        if i > pos and i < end:
            continue
        row = t.data[i]
        r = t.classerify(row[:-1])

        real_r = str(row[-1])
        pref_r = str(r[0][1])

        if real_r == pref_r:
            right += 1

        try:
            wrong_set[real_r][pref_r] += 1
        except:
            print r, real_r, pref_r

    accuracy = right / (data_length - length)
    return (accuracy, wrong_set)


def mk_test(t, freg_size):
    data_length = len(t.data)

    freg_count = data_length / freg_size
    pos = [freg_count * i for i in xrange(freg_size)]

    result = {'accuracy': [], 'error_set': []}

    for i in pos:
        t.fit_part(i, freg_count)
        accuracy, error_set = get_accuray_socre(t, i, freg_count, freg_size)
        result['accuracy'].append(accuracy)
        result['error_set'].append(error_set)

    return result


def print_wrong_matrix(error_set):

    # print wrong predict keys
    print "\t\t",
    for i in sorted(error_set.keys()):
        print "%s\t\t" % i,

    print ""

    # print error matrix
    for row in sorted(error_set.keys()):
        print "%s\t\t" % row,
        error_col = error_set[row]
        for col in sorted(error_col.keys()):
            print "%s\t\t" % error_col[col],
        print ""

    print "Note: Row is the expeced label, colum is predict label."


def main():

    parser = argparse.ArgumentParser(description='To find the best accuracy \
        socre for different size of fregment.')

    parser.add_argument('INPUT', nargs=1, help="Input data file")
    parser.add_argument(
        "-d", dest='depth', default=-1, help="max depth", type=int)
    args = parser.parse_args(sys.argv[1:])

    t = bt.tree_builder(args.depth)
    t.load_data_from_file(args.INPUT[0])

    # freg_fit_result={}
    max_socre = 0
    max_socre_idx = -1
    for i in xrange(2, 21):
        r = mk_test(t, i)
        m = max(r['accuracy'])
        index = r['accuracy'].index(m) + 1
        print "\nsplit data into %02d fregment has high score %f with freg %d"\
            % (i, m, index)
        print_wrong_matrix(r['error_set'][index - 1])

        # freg_fit_result['i']['accuracy'] = m
        # freg_fit_result['i']['index'] = index
        # freg_fit_result['i']['freq'] = i
        if m > max_socre:
            max_socre = m
            max_socre_idx = i
            max_socre_index = index

    print "The high score accuracy is %s into %d block with index at %s" %\
        (max_socre, max_socre_idx, max_socre_index)


if __name__ == '__main__':
    main()
