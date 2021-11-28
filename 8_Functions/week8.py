#!/usr/bin/env python3
# Exercise for Week8: Python Functions
import sys, re, math

# Ex1: Make a function that take a DNA sequence (string) as parameter and return the reverse complement strand.
       # Use it to improve 6.3 which works on dna7.fsa.
# Define function
def rev_complement(dnaseq):
    """Reuturn the reverse comoplement strand of the input DAN sequence"""
    complement_table = str.maketrans('ATCGatcg', 'TAGCtagc')
    try:
        seq = dnaseq.translate(complement_table)[::-1]
        return seq
    except ValueError as err:
        print(str(err), ' : Wrong DNA sequence!')
        sys.exit(1)

# Open the files
filename = input('Enter a fasta file: ')
try:
    if '.fsa' not in filename:
        raise ValueError('The file format is not correct')
    infile = open(filename, 'r')
    outfile = open('revdna.fsa', 'w')
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Call function and write outfile
seq = ''
for line in infile:
    if line.startswith('>'):
        # write the sequence of the previous entry
        if seq != '':
            seq = rev_complement(seq)
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
    seq = rev_complement(seq)
    for i in range(0, len(seq), 60):
        outfile.write(seq[i:i+60] + '\n')

infile.close()
outfile.close()






# Ex2: Improve on 1.10 by making a function that calculates the factorial.
def factorial(num):
    """Return the factorial of the input positive integer """
    result = 1
    if num <= 0:
        raise ValueError("Not a positive integer: " + num + "\n")
    else:
        for i in range(1, num+1):
            result = result * i
        return result

# Ask for input number
num = int(input('Enter a positive integer: '))
print('Ex2: The factorial of', num, 'is ', factorial(num))





# Ex3: Make a function that returns the relevant one-letter designation for the correct ammino acid.
def to_AA(codon):
    """Return the one-letter designation for AA of the input 3-base codon"""
    # Create a codon-AA dictionary
    codonDict = {'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L', 'TTA': 'L', 'TTG': 'L',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'TTT': 'F', 'TTC': 'F', 'ATG': 'M', 'TGT': 'C', 'TGC': 'C', 'GCT': 'A',
    'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P',
    'CCG': 'P', 'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'AGT': 'S',
    'AGC': 'S', 'TAT': 'Y', 'TAC': 'Y', 'TGG': 'W', 'CAA': 'Q', 'CAG': 'Q', 'AAT': 'N', 'AAC': 'N', 'CAT': 'H', 'CAC': 'H',
    'GAA': 'E', 'GAG': 'E', 'GAT': 'D', 'GAC': 'D',	'AAA': 'K', 'AAG': 'K', 'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AGA': 'R', 'AGG': 'R', 'TAA': 'STOP', 'TAG': 'STOP', 'TGA': 'STOP'}
    try:
        std_codon = str(codon).upper()
        return codonDict[std_codon]
    except KeyError as err:
        sys.stderr.write("Codon dose not exist, reason: " + str(err) + "\n")
        sys.exit(1)

# Call the function
cod = input('Enter a codon: ')
print('Ex3: The corresponding AA is', to_AA(cod))





# Ex4: Calculate the the standard deviation (1.8355) of the numbers in ex1.dat.
def std(num_list):
    """Return the standard deviation of the numbers in the input list"""
    n = len(num_list)
    mean = sum(num_list) / n
    tmp = list()
    for num in num_list:
        tmp.append((num - mean) ** 2)
    result = math.sqrt(sum(tmp) / n)
    return result

# File reading and function calling
try:
    infile = open('ex1.dat', 'r')
    numbers = list()
    for line in infile:
        for i in line.split():
            numbers.append(float(i))
    print('Ex4: The standard deviation of is', '{:.4f}'.format(std(numbers)))
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)





# Ex5: Improve 7.4 to make the program print the list ordered by the occurrence of accession number
def sort_dict(dictionary):
    """Return the ordered list of keys according to the sorting of values"""
    key_list = sorted(dictionary.keys(), key=dictionary.get, reverse=True)
    return key_list

try:
    infile = open('ex5.acc', 'r')
    outfile = open('duplicate.acc', 'w')
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Create the dictionary of unique accession numbers
accessions = dict()
for acc in infile:
    acc = acc.strip()
    if acc in accessions:
        accessions[acc] += 1
    else:
        accessions[acc] = 1
infile.close()

# Call function
print('Ex5: The sorted list by the occurance of accession numbers is')
print(sort_dict(accessions))
