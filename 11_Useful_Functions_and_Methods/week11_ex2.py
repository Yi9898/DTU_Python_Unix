#!/usr/bin/env python3
# Exercise for Week11: Useful Functions and Methods
# Ex2: Find the accession numbers with the highest and lowest average scores in appendix3.txt,
#      but exclude the genes in appendix4.txt by finding the corresponding Swiss ID in appendix5.txt.

import sys

# Here I am just using the filenames directly
# read negative file
try:
    infile = open('appendix4.txt', 'r')
except IOError as error:
    sys.stderr.write("Can't read file (appendix4.txt), reason: " + str(error) + "\n")
    sys.exit(1)

negativeSet = set()
for line in infile:
    negativeSet.add(line.strip())
infile.close()

# read translation file
try:
    infile = open('appendix5.txt', 'r')
except IOError as error:
    sys.stderr.write("Can't read file (appendix5.txt), reason: " + str(error) + "\n")
    sys.exit(1)

newNegativeSet = set()
for line in infile:
    fields = line.split()
    if fields[0] in negativeSet:
        newNegativeSet.add(fields[2])
infile.close()
del negativeSet

# read data file
try:
    infile = open('appendix3.txt', 'r')
except IOError as error:
    sys.stderr.write("Can't read file (appendix3.txt), reason: " + str(error) + "\n")
    sys.exit(1)

data = dict()
for line in infile:
    fields = line.split()
    if fields[0] not in newNegativeSet:
        average = sum([float(no) for no in fields[1:]]) / (len(fields) - 1)
        data[fields[0]] = average
infile.close()

# The sorting step
keyList = list(data.keys())
keyList.sort(key=data.get)
# 或者直接用下面的一行代码搞定
# key_list = sorted(data.keys(), key=data.get)


# output
print("Biggest average:", keyList[-1], 'Value:', data[keyList[-1]])
print("Smallest average:", keyList[0], 'Value:', data[keyList[0]])
