#!/usr/bin/env python3
# Exercise for Week7: Sets and Dictionaries
import sys, re

# Ex1: Create a codon-AA dictionary
codonDict = {'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L', 'TTA': 'L', 'TTG': 'L',
'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'TTT': 'F', 'TTC': 'F', 'ATG': 'M', 'TGT': 'C', 'TGC': 'C', 'GCT': 'A',
'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P',
'CCG': 'P', 'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'AGT': 'S',
'AGC': 'S', 'TAT': 'Y', 'TAC': 'Y', 'TGG': 'W', 'CAA': 'Q', 'CAG': 'Q', 'AAT': 'N', 'AAC': 'N', 'CAT': 'H', 'CAC': 'H',
'GAA': 'E', 'GAG': 'E', 'GAT': 'D', 'GAC': 'D',	'AAA': 'K', 'AAG': 'K', 'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
'AGA': 'R', 'AGG': 'R', 'TAA': 'STOP', 'TAG': 'STOP', 'TGA': 'STOP'}



# Ex2: Translate all the entries in dna7.fsa into an output file aa7.fsa
try:
    infile = open('dna7.fsa', 'r')
    outfile = open('aa7.fsa', 'w')
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Initialize the variables
DNAseq = ''
AAseq = ''
for line in infile:
    if line.startswith('>'):
        # write the translated sequence of the previous entry
        if DNAseq != '':
            # translate
            for i in range(0, len(DNAseq)-3, 3):
                if codonDict[DNAseq[i:i+3]] != 'STOP':
                    AAseq += codonDict[DNAseq[i:i+3]]
                else:
                    break
            for i in range(0, len(AAseq), 60):
                outfile.write(AAseq[i:i+60] + '\n')
        # begin with a new entry
        DNAseq = ''
        AAseq = ''
        outfile.write(line)
    else:
        # collect DNA sequence of the present entry
        if re.search(r'[^atcgATCG]+', line) is not None:
            DNAseq += line.strip()
        else:
            print('Wrong DNA sequence!')
            sys.exit(1)

# write sequence of the last entry into the output file
if DNAseq != '':
    for i in range(0, len(DNAseq)-3, 3):
        if codonDict[DNAseq[i:i+3]] != 'STOP':
            AAseq += codonDict[DNAseq[i:i+3]]
        else:
            break
    for i in range(0, len(AAseq), 60):
        outfile.write(AAseq[i:i+60] + '\n')

# Close files
infile.close()
outfile.close()





# Ex3:  Discover which accession numbers in start10.dat did not show up in res10.dat
# Pseudo-code:
# Open two files
# for line in startfile:
    # put each line into set1
# for line in resfile:
    # put the second column of each line into another set2
# Close the files
# missing_acc = set1.difference(set2)

try:
    startfile = open('start10.dat', 'r')
    resfile = open('res10.dat', 'r')
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Buil accesion number sets
start_acc = set()
res_acc = set()
for line in startfile:
    start_acc.add(line.strip())
for line in resfile:
    res_acc.add(line.split()[1])

startfile.close()
resfile.close()

# Find disappearing accession numbers
diff = start_acc.difference(res_acc)
print('The accession numbers that did not produce output are', ', '.join(list(diff)))



# Ex4: Count the duplicates in ex5.acc
# Pseudo-code:
# Open 'ex5.acc' for reading and 'duplicate.acc' for writing
# Extract all acc numbers into a list all_acc
# uniq_acc = set(all_acc)
# for acc in uniq_acc:
    # outfile.write(acc + ' ' + str(all_acc.count(acc)) + '\n')
# Close two files

try:
    infile = open('ex5.acc', 'r')
    outfile = open('duplicate.acc', 'w')
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Extract the lines to a list
all_acc = '\n'.join(infile.readlines()).split()
# Extract unique accession numbers
uniq_acc = set(all_acc)
infile.close()

# Count duplicates
for acc in uniq_acc:
    num = all_acc.count(acc)
    outfile.write(acc + ' ' + str(num) + '\n')
outfile.close()
# By teacher:
# accessions = dict()
# for acc in infile:
#     acc = acc.strip()
#     if acc in accessions:
#         accessions[acc] += 1
#     else:
#         accessions[acc] = 1
# accFile.close()
#
# for acc in accessions.keys():
#    print(acc, accessions[acc])




# Ex5 & 6: List and count the codon used in data?.gb files + Extracts all unique authors from the reference
# Get input file name
if len(sys.argv) == 1:   # no commandline arguments
    filename = input("Please enter a genbank filename: ")
elif len(sys.argv) == 2: # something is there
    filename = sys.argv[1]
else:
    sys.stderr.write("Usage: extractgenbank.py <filename>\n")
    sys.exit(1)

# Reading through iteration
(joinflag, dnaflag, authorflag, joinline, dnaseq) = (False, False, False, '', '')
authors = ''
try:
    infile = open(filename, 'r')
    for line in infile:
        # Stateful parsing of DNA
        if dnaflag:
            if line.startswith('//'):			# Red line
                dnaflag = False
            else:
                REresult = re.search('^\s*\d+\s+([atcgATCGxX ]+)$', line)
                if REresult is not None:
                    dnaseq += REresult.group(1)
                else:
                    sys.stderr.write("Probable error in data format\n" + line)
                    sys.exit(1)
        elif line.startswith('ORIGIN '):		# Green line
             dnaflag = True

        # Find exons - the join line(s)
        REresult = re.search(r'^\s+CDS\s+join\((.+)', line)
        if REresult is not None:
            joinline += REresult.group(1).strip()
            if line[-2] != ')':				# End parenthesis - red line
                joinflag = True
        elif joinflag:
            joinline += line.strip()
            if line[-2] == ')':				# End parenthesis - red line
                joinflag = False

        # Extract AUTHORS
        if authorflag:
            if re.search(r'^\s+TITLE\s+', line) is not None:
                authorflag = False
                authors += ', '
            else:
                authors += ' ' + line.strip()
        REresult = re.search(r'^\s+AUTHORS\s+([A-Z]{1}.+)', line)
        if REresult is not None:
            authors += REresult.group(1).strip()
            authorflag = True
    infile.close()

except IOError as error:
    sys.stderr.write("Can't read file, reason: " + str(error) + "\n")
    sys.exit(1)

# Get DNA sequence
dnaseq = re.sub(r'\s+','', dnaseq)

# Get exons
joinline = joinline[:-1]
exons = joinline.split(',')
codingseq = ''
for exon in exons:
    pos = exon.split(r'..')
    start = int(pos[0]) - 1
    end = int(pos[1])
    codingseq += dnaseq[start:end]

# List codons and appearing times
all_codon = list()
for i in range(0, len(codingseq)-3, 3):
    triplet = codingseq[i:i+3]
    if re.search(r'^[ATCG]{3}$', triplet) is None:
        print("Error, not true codon:", triplet)
        sys.exit(1)
    all_codon.append(triplet)
uniq_codon = set(all_codon)
print('Ex5: The codons and corresponding numbers are')
for codon in uniq_codon:
    print(codon.upper(), str(all_codon.count(codon)))

# Eliminate duplicates in authors and display
authors = authors.replace(' and ', ', ').rstrip(', ').split(', ')
print('\nEx6: The list of non-duplicated authors are')
print(sorted(list(set(authors))))
# By teacher:
# Get rid of duplicate authors
# author_list.sort()
# for i in range(len(author_list)-1, 0, -1):
#     if author_list[i] == author_list[i-1]:
#         del author_list[i]
# print("Author list:\n", '\n'.join(author_list), sep='')
