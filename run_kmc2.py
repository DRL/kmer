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
	parser.add_argument('-i', metavar = 'infiles', default=[''], type = str, nargs='+', help='list of files.')
	parser.add_argument('-fq', action='store_true', help='FASTQ flag.')
	parser.add_argument('-fa', action='store_true', help='FASTA flag.')
	parser.add_argument('-k', metavar = 'kmers' , default=[19], type = int, nargs='+', help='list of k-mers to count.') 
	parser.add_argument('-min', metavar = 'min' , default=2, type = int, help='Min count.') 
	parser.add_argument('-max', metavar = 'max' , default=255, type = int, help='Max count.') 
	parser.add_argument('-o', metavar = 'out' , default='', type = str, help='output prefix.') 

	#parser.add_argument('-t', metavar = 'threads' , default=16, type = int, help='number of threads.') 
	#parser.add_argument('-dry', action='store_true' , help='Set flag for optional dry-run') # dry is for only running until end of cas parsing to output stats and then prompt to continue 

	args = parser.parse_args()

	infiles, kmers, min_count, max_count, fasta_flag, out = args.i, args.k, args.min, args.max, args.fa, args.o
	
	read_file = ''

	if not (out):
		sys.exit("ERROR: Please specify an output prefix")


	if len(infiles) > 1:
  		read_file = 'infile.tmp'
		in_fh = open(read_file, 'w') 
		for infile in infiles:
			in_fh.write(infile + '\n')
		in_fh.close()
	elif len(infiles) == 1:
		read_file = infiles[0]
	else:
		sys.exit("ERROR: Please specify one or more FASTA/FASTQ read files")
  
	return read_file, kmers, min_count, max_count, fasta_flag, out

def run_kmc(reads, kmers):
	prefix = out + "." + reads
	log_file = open(prefix + ".log", 'w')
	benchmark_file = open(prefix + ".benchmark.txt", 'w')
	benchmark_file.write("k,kmers-under-min,kmers-over-max,unique-kmers,unique-kmers-counted,total-kmers,total-reads,total-superkmers,time_1,time_2,total_time,memory\n")
	#kmer_count_file = open(prefix + ".freq.txt", 'w')
	#kmer_count_file.write("k,")
	#for i in range(min_count, max_count):
	#	kmer_count_file.write(str(i) + ",")
   	#kmer_count_file.write("\n")
	
	if reads == 'infile.tmp': 
		reads = '@infile.tmp'

	for kmer in kmers: 

		kmc_out_file = prefix + '.k' + str(kmer) + '.res'
		kmc_dump_file = kmc_out_file + ".txt"
		kmer_count_file = open(kmc_out_file + ".freq.txt", 'w')
		#kmc_freq_file = kmc_out_file + ".freq.txt"

		print "[k = " + str(kmer) + "]",
		if fasta_flag:
			kmc_call = 'kmc -m100 -t24 -k' + str(kmer) + ' -fa ' + reads + ' ' + kmc_out_file + ' .'
			print kmc_call
			kmc_output = subprocess.check_output(kmc_call, shell=True)
		else:
			kmc_call = 'kmc -m100 -t24 -k' + str(kmer) + ' ' + reads + ' ' + kmc_out_file + ' .'
			print kmc_call
			kmc_output = subprocess.check_output(kmc_call, shell=True)
		#print kmc_call
		
		number_re = re.compile(r":\s+(\d+)\s+")
		time_re = re.compile(r"\s+(\d+\.\d+)s\s+")
		memory_re = re.compile(r":\s+(\d+)MB")
		#print kmc_output
		
		number = number_re.findall(kmc_output)
		time = time_re.findall(kmc_output)
		memory = memory_re.findall(kmc_output)

		log_file.write(kmc_output)

		benchmark_string = "k" + str(kmer) + "," + ",".join(number) + "," + ",".join(time) + "," + ",".join(memory) + "\n"
		benchmark_file.write(benchmark_string)

		print "Count.",
		
		kmc_dump(kmc_out_file, kmc_dump_file)

		kmer_freq_dict = get_kmc_dict(kmc_dump_file)
		
		kmer_count_file.write("#k" + str(kmer)+ "\n")
		
		for i in range(min_count, max_count):
			kmer_count_file.write(str(i) + "," + str(kmer_freq_dict.get(i, 0)) + "\n")
		kmer_count_file.write("\n")

		print "Write."
		kmer_count_file.close()
	
	benchmark_file.close()	
	log_file.close()

def kmc_dump(kmc_out_file, kmc_dump_file):
	### KMC dump
	kmc_dump_call = 'kmc_dump ' + kmc_out_file + " " + kmc_dump_file 
	kmc_dump = subprocess.check_output(kmc_dump_call, shell=True)
	print "Dump.",

def get_kmc_dict(kmc_dump_file):
	kmer_freq = {}
	with open(kmc_dump_file) as fh:
		for line in fh: 
			count = int(line.rstrip("\n").split()[1])
			kmer_freq[count] = kmer_freq.get(count, 0) + 1
	print "Summarise.",
	return kmer_freq

if __name__ == "__main__":

	reads, kmers, min_count, max_count, fasta_flag, out = get_input()
  	# min, max multiplicity
	run_kmc(reads, kmers)

	#dump_kmc()