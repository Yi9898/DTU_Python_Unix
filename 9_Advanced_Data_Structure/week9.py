#!/usr/bin/env python3
# Exercise for Week9: Python and Advanced Data Structures

import sys, math

# Ex1: Calculating the average of numbers from all experiments for each accession number in test1.dat. test2.dat and test3.dat
# Pseudo code:
# Open three input files for reading and oen output file for writing
# data = dict()
# for line in three infiles:
    # if accession number not in data.keys():
        # data[accession number] = line.split()[1:]
    # else:
        # data[accession number] += line.split()[1:]
# for key, value in data.items():
    # calculate the average of each value list
    # write the key and average value into output file
# Close all the files

try:
    infile1 = open('test1.dat', 'r')
    infile2 = open('test2.dat', 'r')
    infile3 = open('test3.dat', 'r')
    outfile = open('average.dat', 'w')
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Read the files by iteration
data = dict()
filename = [infile1, infile2, infile3]
for file in filename:
    for line in file:
        content = line.split()
        # Make data dict with accession numbers as keys, list of numbers as values
        if content[0] not in data.keys():
            data[content[0]] = content[1:]
        else:
            data[content[0]] += content[1:]
for file in filename:
    file.close()

# Compute the mean value
for key, value in data.items():
    sum = 0
    for num in value:
        sum += float(num)
    # Write the ourput file
    outfile.write(key + ' ' + str(round(sum / len(value), 2)) + '\n')

outfile.close()





# Ex2: Make a function to transpose the matrix
def transpose(matrix_file):
    try:
        infile = open(matrix_file, 'r')
    except IOError as err:
        print('Cannot open file, reason:', str(err))
        sys.exit(1)

    # Add the matrix to an advanced list structure
    matrix = list()
    for line in infile:
        matrix.extend([line.split()])

    # Initialize transpose matrix
    trans_matrix = list()
    row = len(matrix)
    col = len(matrix[0])
    for i in range(col):
        trans_matrix.extend([[0]*row])
    # Transpose
    for i in range(row):
        for j in range(col):
            trans_matrix[j][i] = matrix[i][j]

    # Print the result
    for row in trans_matrix:
        print('\t'.join(row))

# Call function
transpose('matrix.dat')
