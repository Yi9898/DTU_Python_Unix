#!/usr/bin/env python3
# Exercise for Week9: Python and Advanced Data Structures
# Answer from the teacher

import sys

# Ex1:
### Functions ###

def read_data(filename, sums, counts):
    """Function to add the content of an experiment file to the data dict"""
    try:
        infile = open(filename, 'r')
    except IOError as e:
        print("Can't open file, Reason: " + str(e))
        sys.exit(1)
    for line in infile:
        tmp = line.split()
        mysum = 0
        for number in tmp[1:]:
            mysum += float(number)
        if tmp[0] in sums:
            sums[tmp[0]] += mysum
            counts[tmp[0]] += len(tmp) - 1
        else:
            sums[tmp[0]] = mysum
            counts[tmp[0]] = len(tmp) - 1
    infile.close()

### Main code ###

# Get the files
if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = input('Enter a set of space separated file names: ').split()

# Main data structures can be declared here, if they are used as parameters in functions
sums = dict()
counts = dict()

# Read the files
for filename in files:
    read_data(filename, sums, counts)

# Calculate average, print to screen
for key in sums:
    print(key, "{:.4f}".format(sums[key]/counts[key]), sep='\t')









# Ex2:
### Functions ###

# Reading the file line by line, splitting on whitespace. The split lines becomes rows in the matrix.
# A lot of the code is really just input control, because if the input is well-formed, the rest of the code is easier.
def read_matrix_file(filename):
    """Function for reading a matrix containing only numbers"""
    try:
        infile = open(filename, 'r')
    except IOError as error:
        sys.stderr.write("Can't read file (" + filename +"), reason: " + str(error) + "\n")
        sys.exit(1)

    matrix = list()
    row_size = None
    for line in infile:
        row = line.split()
        if row_size is None:
            row_size = len(row)
        if row_size != len(row):
            sys.stderr.write("Not same number of columns in each row.\n")
            sys.exit(1)
        matrix.append(list())
        for number in row:
            try:
                number = float(number)
            except ValueError:
                sys.stderr.write("Some fields in matrix does not contain numbers\n")
                sys.exit(1)
            matrix[-1].append(number)
    infile.close()
    return(matrix)

# Print a matrix using join trick to avoid extra tab at the end of line
def print_matrix(matrix):
    """Function for printing a matrix tab separated"""
    for row in matrix:
        stringrow = list()
        for number in row:
            stringrow.append("{:.2f}".format(number))
        print("\t".join(stringrow))

# Trivial transposition by creating a new matrix and populating the
# rows with the original matrix's columns.
def transpose(matrix):
    """Function for transposing a matrix, returns transposed matrix"""
    # Make a new matrix with the right height
    new_matrix = list()
    for x in range(len(matrix[0])):
        new_matrix.append(list())
    # This method does not work as you wil get the SAME empty list x times
    # new_matrix = len(matrix[0]) * [list()]
    # Transpose
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            new_matrix[y].append(matrix[x][y])
    return new_matrix


### Main program ###

# Get input file name
if len(sys.argv) == 1:
    filename = input("Please enter a matrix file: ")
elif len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    sys.stderr.write("Usage: transpose_matrix.py <filename>\n")
    sys.exit(1)

# The main code is simple to understand, test and modify, because functions are used.
matrix = read_matrix_file(filename)
matrix = transpose(matrix)
#transpose_inline(matrix)
print_matrix(matrix)
