#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File    	: run_kmc2.py
Author  	: Dominik R. Laetsch, dominik.laetsch at gmail dot com 
Version 	: 0.1
Description : run_kmc2.py
Beware of 	: 
To do 		: 
"""

from __future__ import division
import os, re, sys, argparse, subprocess, itertools, commands
from itertools import izip

def get_input():
	'''Gets, checks and returns input'''
	parser = argparse.ArgumentParser(
		prog='run_kmc2.py',
		usage = '%(prog)s -i -k [-h]',
		add_help=True)
	parser.add_argument('-i', metavar = 'infiles', default=[''], type = str, nargs='+', help='list of FASTQ files.')
	parser.add_argument('-k', metavar = 'kmers' , default=[19], type = int, nargs='+', help='list of k-mers to count.') 
	#parser.add_argument('-m', metavar = 'memory' , default=100, type = int, help='allocated memory in Gbytes.') 
	#parser.add_argument('-t', metavar = 'threads' , default=16, type = int, help='number of threads.') 
	#parser.add_argument('-dry', action='store_true' , help='Set flag for optional dry-run') # dry is for only running until end of cas parsing to output stats and then prompt to continue 

	args = parser.parse_args()

	infiles, kmers = args.i, args.k

	if len(infiles) > 1:
		read_file = '@infile.tmp'
		in_fh = open(read_file, 'w') 
		for infile in infiles:
			in_fh.write(infile + '\n')
		in_fh.close()
	elif len(infiles) == 1:
		read_file = infiles[0]
	else:
		sys.exit("ERROR: Please specify one or more FASTA/FASTQ read files")

	return read_file, kmers

def run_kmc(reads, kmers):

	for kmer in kmers: 
		kmc_call = 'kmc -m100 -t24 -k' + str(kmer) + ' ' + reads + ' ' + reads + '.' + str(kmer) + '.res' + ' .'
		#print kmc_call
		kmc_output = subprocess.check_output(kmc_call, shell=True)
		print kmer
		print kmc_output
		#reads_re = re.compile(r" -q -i (\S+) (\S+)")

if __name__ == "__main__":

	reads, kmers = get_input()
  
	run_kmc(reads, kmers)

	#dump_kmc()