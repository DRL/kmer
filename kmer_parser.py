#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys, argparse, os

def parse_file(infile):
	print "\tParsing ...",
	kmer_freq = {}
	with open(infile) as fh:
		for line in fh: 
			count = int(line.rstrip("\n").split()[1])
			kmer_freq[count] = kmer_freq.get(count, 0) + 1
	print "Done."
	return kmer_freq

def plot_freq(kmer_freq):
	print "\tPlotting ...",
	plt.plot(kmer_freq.keys(), kmer_freq.values(), '-ro', ms=2.0)
	plt.savefig(kmer_file + ".png", format="png")
	plt.close()
	print "Done."

def print_freq(kmer_freq):
	print "\tWriting freqs ...",
	with open(kmer_file + '.freq.txt', 'w') as fh:
		for key in sorted(kmer_freq):
			fh.write(str(key) + "\t" + str(kmer_freq[key]) + "\n")
	print "Done."

if __name__ == "__main__":
	kmer_file = sys.argv[1]
	freq_dict = parse_file(kmer_file)
	#plot_freq(freq_dict)
	print_freq(freq_dict) 
