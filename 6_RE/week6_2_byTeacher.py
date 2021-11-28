#!/usr/bin/env python3
# Exercise for Week6: Pattern Matching and Regular Expressions
# 提取 Genbank 文件的信息（accession number, Definition, AA sequence, whole DNA sequence, Coding DNA sequences, etc.）

import sys
import re

# Get input file name
if len(sys.argv) == 1:   # no commandline arguments
    filename = input("Please enter a genbank filename: ")
elif len(sys.argv) == 2: # something is there
    filename = sys.argv[1]
else:
    sys.stderr.write("Usage: extractgenbank.py <filename>\n")
    sys.exit(1)

# Initialize
(accession, definition, organism) = (None, None, None)
medline = []
(aminoflag, dnaflag, joinflag, aminoseq, dnaseq, joinline) = (False, False, False, '', '', '')
try:
    infile = open(filename, 'r')
    for line in infile:
        # Simple extractions
        REresult = re.search("^ACCESSION\s+([A-Z]+\d+)", line)
        if REresult is not None:
            accession = REresult.group(1)

        REresult = re.search("^DEFINITION\s+(.+)", line)
        if REresult is not None:
            definition = REresult.group(1)

        REresult = re.search("^  ORGANISM\s+(.+)", line)
        if REresult is not None:
            organism = REresult.group(1)

        # Medline
        REresult = re.search("^\s+MEDLINE\s+(\d+)", line)
        if REresult is not None:
            medline.append(REresult.group(1))

        # Stateful parsing of translated protein sequence
        # Works on one line and multiple line sequences
        REresult = re.match('^\s+/translation=.([A-Z]+)', line)
        if REresult is not None:			# Green line
            aminoseq = REresult.group(1)
            if line[-2] != '"':				# Possible Red line
                aminoflag = True
        elif aminoflag:
            if line[-2] == '"':				# Definitely Red line
                aminoseq += line.strip()[:-1]
                aminoflag = False
            else:
                aminoseq += line.strip()

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
    infile.close()

except IOError as error:
    sys.stderr.write("Can't read file, reason: " + str(error) + "\n")
    sys.exit(1)

print("Accession number:", accession)
print("Definition:", definition)
print("Organism:", organism)
print("Medline:", ', '.join(medline))
print("Protein sequence:")
for i in range(0, len(aminoseq), 60):
   print(aminoseq[i:i+60])
# Clean dnaseq of spaces
dnaseq = re.sub(r"\s+","", dnaseq)
# Get exons
joinline = joinline[:-1]
exons = joinline.split(',')
print('exons:', exons)
codingseq = ''
for exon in exons:
    pos = exon.split(r'..')
    start = int(pos[0]) - 1
    end = int(pos[1])
    codingseq += dnaseq[start:end]

print("Coding DNA sequence:")
for i in range(0, len(codingseq), 60):
    print(codingseq[i:i+60])
