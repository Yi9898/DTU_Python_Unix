#!/usr/bin/env python3
# Exercise for Week6: Pattern Matching and Regular Expressions
# This script only covers the exercises from 5-9
import sys, re

if len(sys.argv) != 2:  # no arguments or wrong number of arguments in command line
    print('Usage: week6_2.py <Genbank file>')
    sys.exit(1)
else:
    try:
        infile = open(sys.argv[1], 'r')
    except IOError as err:
        print('Cannot open file, reason:', str(err))
        sys.exit(1)

#Initialize variables
medline = ''
# AAflag = False
# DNA = ''
# DNAflag = False
(AAflag, DNAflag, AA, DNA) = (False, False, '', '')
for line in infile:
    # ex5: Accession number extraction
    result = re.search(r'^ACCESSION\s+([A-Z]+\d+)\s+', line)
    if result is not None:
        Acc = result.group(1)

    # ex5: Definition extraction
    result = re.search(r'^DEFINITION\s+(.+)', line)
    if result is not None:
        Def = result.group(1)

    # ex5: Organism extraction
    result = re.search(r'^\s+ORGANISM\s+(.+)', line)
    if result is not None:
        Org = result.group(1)

    # ex6: MEDLINE number extraction
    result = re.search(r'^\s+MEDLINE\s+(\d+)', line)
    if result is not None:
        medline += (result.group(1)+' ')

    # ex7: Translated gene extraction
    result = re.search(r'^\s+/translation=.([A-Z]+)', line)
    if result is not None:
        AA = result.group(1)
        if line[-2] != '"':
            AAflag = True
            continue
    if AAflag:
        if line[-2] == '"':
            AA += line.strip()[:-1]
            AAflag = False
        else:
            AA += line.strip()

    # ex8: DNA extraction
    if DNAflag:
        if line.startswith('//'):
            DNAflag = False
        else:
            result = re.search(r'^\s*\d+\s+([atcgx ]+)$', line)
            if result is not None:
                DNA += result.group(1)
            else:
                print('Can not find DNA sequences!')
                sys.exit(1)
    if line.startswith('ORIGIN'):
        DNAflag = True

    # ex9: Coding DNA extraction
    if re.search(r'^\s+CDS\s+join.', line) is not None:
        coding_index = re.findall(r'(\d+)', line)

infile.close()

# extract each coding DNA by two combinations of coding index
DNA = re.sub(r"\s+","", DNA)
print(coding_index)
coding_DNA = ''
for i in range(0, len(coding_index), 2):
    coding_DNA += DNA[int(coding_index[i])-1:int(coding_index[i+1])-1] + '\n\n'

print('Accession number:', Acc, '\nDefinition:', Def, '\nOrganism:', Org)
print('MEDLINE number:', medline)
print('The translated gene is')
print(AA)
print('The DNA sequence is:')
print(DNA)
print('The coding DNA sequence is:')
print(coding_DNA)
