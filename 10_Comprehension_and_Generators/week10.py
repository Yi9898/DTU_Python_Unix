#!/usr/bin/env python3
# Exercise for Week10: Comprehension and Generators
import sys, re


# Ex1: Make a program that calculates the product of two matrices and prints it on STDOUT (the screen).
### Functions
def read_matrix(matrix_file):
    '''Return the list form of the matrix'''
    try:
        infile = open(matrix_file, 'r')
        # Add the matrix to an advanced list structure
        matrix = list()
        for line in infile:
            matrix.append([float(ele) for ele in line.split()])
        return matrix

    except IOError as err:
        print('Cannot open file, reason:', str(err))
        sys.exit(1)


def matrix_product(M1, M2):
    '''Return the product of two matrices'''
    if len(M1[0]) != len(M2):
        raise ValueError('Wrong dimension or wrong order of the two matrices!')
    result = []
    # Iterate through rows of M1
    for i in range(len(M1)):
        result.append([])
        # Iterate through columns of M2
        for j in range(len(M2[0])):
            number = 0
            # Iterate through rows of M2
            for k in range(len(M2)):
                number += M1[i][k] * M2[k][j]
            result[-1].append(number)
    return result


def print_result(matrix):
    '''Print the input matrix on the screen'''
    for row in matrix:
        if not isinstance(row, list):
            raise ValueError('Your input is not a matrix!')
        print('\t'.join(["{:.2f}".format(ele) for ele in row]))

### Main program
mat1 = read_matrix('mat1.dat')
mat2 = read_matrix('mat2.dat')
product = matrix_product(mat1, mat2)
print_result(product)






# Ex2: Ask for accession number, find corresponding number in dna-array.dat
#      and extract the numbers of cancer patient(0) in one column, the numbers of control group(1) in another column.

# Get input accession number
if len(sys.argv) == 1:
    filename = input('Please enter a DNA array data file: ')
    acc = input('Please enter an accession number: ')
elif len(sys.argv) == 3:
    filename = sys.argv[1]
    acc = sys.argv[2]
else:
    sys.stderr.write("Usage: week10.py <accession number>\n")
    sys.exit(1)


# Find acc in the file
try:
    infile = open(filename, 'r')
    flag = False
    for line in infile:
        # Extract class number
        if line.split()[0] == 'COL_CLASSES':
            class_list = line[:-1].split()[1:]
        # Extract numbers of corresponding acc
        elif line.split()[1] == acc:
            flag = True
            numbers = re.findall(r'\s+(-?\d{1}.\d{2})', line)
            break

    # If not found
    if flag == False:
        raise ValueError('The accession number does not exist!')
        sys.exit(1)
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)


# Extract numbers corresponding to 0 and 1, respectively
zero_list = []
one_list = []
for i in range(len(class_list)):
    if class_list[i] == '0':
        zero_list.append(numbers[i])
    elif class_list[i] == '1':
        one_list.append(numbers[i])
    else:
        raise ValueError('Wrong class list!')
        sys.exit(1)


# Print the two columns
max_len = max(len(zero_list), len(one_list))
print('Cancer\tControl')
for i in range(max_len):
    if i < len(zero_list) and i < len(one_list):
        print(zero_list[i], '\t', one_list[i])
    elif i < len(zero_list):
        print(zero_list[i], '\t')
    else:
        print('\t', one_list[i])
