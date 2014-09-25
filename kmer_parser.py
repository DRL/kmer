#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys, argparse, os

def parse_file(infile):
	kmer_freq = {}
	with open(infile) as fh:
		for line in fh: 
			count = int(line.rstrip("\n").split()[1])
			kmer_freq[count] = kmer_freq.get(count, 0) + 1
	for key in sorted(kmer_freq):
		print str(key) + "\t" + str(kmer_freq[key])

if __name__ == "__main__":
	kmer_file = sys.argv[1]
	parse_file(kmer_file)