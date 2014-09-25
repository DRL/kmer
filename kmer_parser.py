#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys, argparse, os

import numpy as np
import matplotlib.pyplot as plt

def parse_file(infile):
	kmer_freq = {}
	with open(infile) as fh:
		for line in fh: 
			count = int(line.rstrip("\n").split()[1])
			kmer_freq[count] = kmer_freq.get(count, 0) + 1
	#for key in sorted(kmer_freq):
	#	print str(key) + "\t" + str(kmer_freq[key])
	return kmer_freq

def plot(kmer_freq):
	for key in sorted(kmer_freq):
		plt.scatter(key, kmer_freq[key])
	plt.show()

if __name__ == "__main__":
	kmer_file = sys.argv[1]
	freq_dict = parse_file(kmer_file)

	plot(freq_dict)
