#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys, argparse, os
import matplotlib.pyplot as plt

def parse_file(infile):
	print "\tParsing ...",
	plt.axes(axisbg=background_grey)
	plt.ylim(ymax = 10000000, ymin = 10)
	plt.xlim(xmax = 75, xmin = 2)
	plt.axes(axisbg=background_grey, yscale = 'log')
	
	x = []
	y = []
	k = ''
	
	with open(infile) as fh:
		for line in fh: 
			temp = line.rstrip("\n").split(",")
			if x == []:
				x = map(int, temp[1:])
			else:
				k = temp[0]
				y = map(int, temp[1:])
			if not y == []:
				plt.plot(x, y, label=k, marker = 'o', ms = 1)
				plt.legend()
				plt.savefig(infile + "." + str(k) + ".png", format="png")
	plt.show()

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
	black, grey, background_grey, white = '#262626', '#d3d3d3', '#F0F0F5', '#ffffff'
	kmer_file = sys.argv[1]
	freq_dict = parse_file(kmer_file)
	#plot_freq(freq_dict)
	#print_freq(freq_dict) 
