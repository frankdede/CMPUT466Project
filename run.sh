#!/bin/bash

#python parser.py -r dataset/train.tsv -s dataset/stopwords_default.txt

python parser.py -r dataset/train.tsv -t dataset/test.tsv -s dataset/stopwords_default.txt -m