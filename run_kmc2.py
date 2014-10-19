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
		#time_re = re.compile(r"Total\s+:\s+(\S+)")
		#mem_re = re.compile(r"Tmp size\s+:\s+(\S+)")
		#kmer_min_re = re.compile(r"\s+No\. of k-mers below min\. threshold\s+:\s+(\d+)")
		#kmer_max_re = re.compile(r"\s+No\. of k-mers above min\. threshold\s+:\s+(\d+)")
		#kmer_unique_re = re.compile(r"\s+No\. of unique k-mers\s+:\s+(\d+)")
		#kmer_unique_counted_re = re.compile(r"\s+No\. of unique counted k-mers\s+:\s+(\d+)")
		#kmer_total_re = re.compile(r"\s+Total no\. of k-mers\s+:\s+(\d+)")
		#reads_total_re = re.compile(r"\s+Total no\. of reads\s+:\s+(\d+)")
		#superkmer_total_re = re.compile(r"\s+Total no\. of super-k-mers\s+:\s+(\d+)")
		number_re = re.compile('\d+\.d+')
		kmc_out = number_re.findall(kmc_output)
		#time = re.match(time_re, str(kmc_output)).group()
		#mem = re.match(mem_re, str(kmc_output)).group()
		#kmer_min = re.match(kmer_min_re, str(kmc_output)).group()
		#kmer_max = re.match(kmer_max_re, str(kmc_output)).group()
		#kmer_unique = re.match(kmer_unique_re, str(kmc_output)).group()
		#kmer_unique_counted = re.match(kmer_unique_counted_re, str(kmc_output)).group()
		#kmer_total = re.match(kmer_total_re, str(kmc_output)).group()
		#reads_total = re.match(reads_total_re, str(kmc_output)).group()
		#superkmer_total = re.match(superkmer_total_re, str(kmc_output)).group()

		print kmc_output
		print kmc_out
		#print time
		#print mem
		#print kmer_min
		#print kmer_max
		#print kmer_unique
		#print kmer_unique_counted
		print kmer_total
		print reads_total
		print superkmer_total


if __name__ == "__main__":

	reads, kmers = get_input()
  
	run_kmc(reads, kmers)

	#dump_kmc()