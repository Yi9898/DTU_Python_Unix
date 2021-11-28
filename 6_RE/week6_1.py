#!/usr/bin/env python3
# Exercise for Week6: Pattern Matching and Regular Expressions
# This script only covers the exercises from 1-3

import sys, re

# EX1: Use regular expressions (RE) to determine if the input is a number
string = input('Please enter whatever you want: ')
if re.search(r'^[+-]?\d+(\.\d+)?$', string):
    print('It is a number!')
else:
    print('It is not a number!')





# Ex2: Improve exercise 5.6(week4) by using regular expressions to find the ID, accession number and amino acid sequence,
# and write them all into an output file.
# Get filename and open file
filename = input('Enter a SwissProt file: ')
try:
    infile = open(filename, 'r')
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

#Initialize variables
AA = ''
flag = False

# Iteration through file
for line in infile:
    # extract ID from the line using RE
    result = re.search(r'^ID\s+(\w+)', line)
    if result is not None:
        id = result.group(1)

    # extract accession number from the line
    if re.search(r'^AC\s+(\w+)', line):
        acc_list = line.split()[1:]
        acc = ' '.join(acc_list)

    # read and print the amino sequence
    # if re.search(r'^SQ\s+', line):
    #     AA_num = int(line.split()[2])
    # if re.search(r'^\s+', line):
    #     AA += line.strip().replace(' ', '')

    # By Teacher: (read and print AA using "stateful parsing")
    # Find sequence (and length)
    if line == "//\n":
        flag = False
    if flag:
        AA += re.sub('\s', '', line)
    result = re.search("^SQ\s+SEQUENCE\s+(\d+)\s+AA;", line)
    if result is not None:
        AA_num = result.group(1)
        flag = True
infile.close()

# Error handling
try:
    if id is None:
        raise ValueError("No SwissProt ID found")
    if acc is None:
        raise ValueError("No Accession number found")
    if AA == '':
        raise ValueError("No sequence found")
    if len(AA) != int(AA_num):
        raise ValueError("Given length of amino sequence does not match real length")
except ValueError as err:
    sys.stderr.write("Format error: " + str(err) + "\n")
    sys.exit(1)

# Write the output file
try:
    outfile = open('sprot.fsa', 'w')
    outfile.write('>' + 'Accession number: ' + acc + ' ID: ' + id + ' ' + str(AA_num) + 'AA' + '\n')
    for i in range(0, len(AA), 60):
        outfile.write(AA[i:i+60] + '\n')
    outfile.close()
except IOError as err:
    sys.stderr.write("Can't write file, reason: " + str(err) + "\n")
    sys.exit(1)






# Ex3: Improve exercise 4.10 (week3) to make a new .fsa file that contains the reverse complement sequence of each ectry
# pseudocode:
# Ask for input filename (dna7.fsa)
# infile = open(filename, 'r')
# outfile = open('revdna.fsa', 'w')
# seq = ''
# make complement table
# for line in infile:
    # if line starts with '>':
        # if seq == '':
            # write line into outfile
        # else:
            # make reverse complement strand using seq.translate
            # write complement strand to output file
            # reset seq = ''
    # if line starts with 'A/T/C/G':
        # add line to seq
# write sequence of the last entry into the output file
# close file

filename = input('Enter a fasta file: ')
try:
    if '.fsa' not in filename:
        raise ValueError('The file format is not correct')
    infile = open(filename, 'r')
    outfile = open('revdna.fsa', 'w')
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Initialize the variables
seq = ''
complement_table = str.maketrans('ATCGatcg', 'TAGCtagc')
for line in infile:
    if line.startswith('>'):
        # write the sequence of the previous entry
        if seq != '':
            seq = seq.translate(complement_table)[::-1]
            for i in range(0, len(seq), 60):
                outfile.write(seq[i:i+60] + '\n')
        # begin with a new entry
        seq = ''
        outfile.write(line[:-1] + ' Complement Strand\n')
    else:
        # Collect DNA sequence of the present entry
        if re.search(r'[^atcgATCG]+', line) is not None:
            seq += line.strip()
        else:
            print('Wrong DNA sequence!')
            sys.exit(1)

# write sequence of the last entry into the output file
if seq != '':
    seq = seq.translate(complement_table)[::-1]
    for i in range(0, len(seq), 60):
        outfile.write(seq[i:i+60] + '\n')

infile.close()
outfile.close()
