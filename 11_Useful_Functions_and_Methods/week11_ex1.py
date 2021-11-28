#!/usr/bin/env python3
# Exercise for Week11: Useful Functions and Methods
# Ex1: Deal with appendix1.txt(Swissprot file).
#      Extract the original AA sequence, mutated AAs and mutated positions.
#      Write the orignal sequences and mutated sequences together into an output file.
import sys
import re


# Get input file name
if len(sys.argv) == 2:
    filename = sys.argv[1]
elif len(sys.argv) == 1:
    filename = input("Please enter a swissprot file: ")
else:
    sys.stderr.write("Usage: extraxt_variants.py <filename>\n")
    sys.exit(1)

try:
    infile = open(filename, 'r')
except IOError as error:
    sys.stderr.write("Can't read file (" + filename +"), reason: " + str(error) + "\n")
    sys.exit(1)

# read file
flag, sequence, seqLength, identifier = False, '', 0, ''
changelist = list()
for line in infile:
    if line.startswith('ID'):
        identifier = line.split()[1]
    if line.startswith('//'):
        flag = False
    if flag:
        sequence += line
    if line.startswith('SQ'):
        flag = True
        matchObj = re.search(r'SEQUENCE\s+(\d+)\s+AA;', line)
        if matchObj is not None:
            seqLength = int(matchObj.group(1))
    matchObj = re.search(r'^FT\s+(?:VARIANT|MUTAGEN)\s+(\d+)\s+\d+\s+[A-Z]\s*->\s*([A-Z])', line)
    if matchObj is not None:
        changelist.append((int(matchObj.group(1)), matchObj.group(2))) # eg.[(309,'R'), (310,'V'), (318,'S')]
infile.close()

# quick way of getting rid of whitespace
sequence = ''.join(sequence.split())

# Error checking
if identifier == '':
    sys.stderr.write("Could not find identifier, is this a swissprot entry?\n")
    sys.exit(1)
if flag is True:
    sys.stderr.write("File is not in proper swissprot format.\n")
    sys.exit(1)
if len(sequence) != seqLength:
    sys.stderr.write("Actucal length and stated length of sequence does not match.\n")
    sys.exit(1)
'''
The obvious error checks are when opening files. I have checked that the identifier exists, the sequence length macthes and the stateful parsing ends properly, hence the entry looks sound. It is not considered an eror if there are no variant features. I have made the following assumptions:
1) The sequence is a protein sequence with no "strange" chars.
2) The acid changed is the acid stated in the feature line.
3) The replacement positions are inside the sequence.
These assumptions can be removed by making appropiate checks.
'''

def outputFasta(fastafile, header, sequence):
    print(">" + header, file=fastafile)
    for i in range(0, len(sequence), 60):
        print(sequence[i:i+60], file=fastafile)

# open output file
try:
    fasta = open('fasta', 'w')
except IOError as error:
    sys.stderr.write("Can't write file, reason: " + str(error) + "\n")
    sys.exit(1)

outputFasta(fasta, identifier + ' Original', sequence)
counter = 1
for item in changelist:
    newseq = sequence[:item[0]-1] + item[1] + sequence[item[0]:]
    outputFasta(fasta, identifier + '_' + str(counter) + ' Variation ' +
        str(item[0]) + ' ' + sequence[item[0]-1] + ' -> ' + item[1], newseq)
    counter += 1
fasta.close()
