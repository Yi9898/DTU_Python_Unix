#!/usr/bin/env python3
#Author: Yi
#Exercise for Week3: Python Input-Output

#1. Calculate mean value for two input integers
num1 = int(input('Enter the first integer: '))
num2 = int(input('Enter the second integer: '))
mean_value = (num1 + num2) / 2
print('1. The integers and their mean value are', num1, ',', num2, ',', int(mean_value))

#2. I used "vi integer.txt" to make a file containing two integers.
import sys
num1 = int(sys.stdin.readline())
num2 = int(sys.stdin.readline())
mean_value = (num1 + num2) / 2
print('2. The integers and their mean value are', num1, ',', num2, ',', int(mean_value))
# You need to use the following command to run this code:
# week3.py < integer.txt

#3. Count the number of negative numbers in ex1.dat
infile = open('ex1.dat', 'r')
neg = 0
for line in infile:
        for i in range(len(line)):
                if line[i] == '-':
                        neg += 1
print('3. The negative numbers are', neg)
infile.close()

#4. Convert Fahrenheit to Celsius or visa versa
temp = input('Enter either a Fahrenheit or Celsius temperature: ')
if temp[-1] == 'F':
        C = (float(temp[:-1]) - 32) * 5 / 9
        print(temp, 'is', str(C)+'C')
else:
        F = (float(temp[:-1]) * 9 / 5) + 32
        print(temp, 'is', str(F)+'F')



#5. Find all the accession number
infile = open('orphans.sp', 'r')
outfile = open('accession.txt', 'w')
for line in infile:
        if line[0] == '>':
                outfile.write(line[1:15]+'\n') #beacuse all the accession numbers are 14 in length
infile.close()
outfile.close()

# -----Code from teacher:----- (找到含有accession number的每一行第一次出现的空格，然后将'>'和空格之间的accession number提取出来)
infile = open('orphans.sp', 'r')
outfile = open('orphans.acc', 'w')
# Read the file, find accession lines
for line in infile:
    if line[0] == '>':
        # OK this is acc.no line, now find the first space in the line
        i = 1
        accession = ''
        while i < len(line) and line[i] != ' ':
            accession += line[i]
            i += 1
        outfile.write(accession + "\n")
infile.close()
outfile.close()



#6. Concatenate each row of two input files

# The pseudocode is shown below:
# Ask for two file names one by one
# Open two input files and one empty file
# Read line of the first file
# Read line of the second file
# while line of the first and second file != ''
#         Write two lines into empty file
#         Read next line of the first file
#         Read next line of the second file
# close all the files

# The real code is show below:
f1 = input('Enter the first file name: ')
f2 = input('Enter the second file name: ')
infile1 = open(f1, 'r')
infile2 = open(f2, 'r')
outfile = open('concat.txt', 'w')
content1 = infile1.readline().strip()  #delete the '\n' in each line
content2 = infile2.readline()
while content1 != '' and content2 != '':
        print(content1, content2, file=outfile)
        content1 = infile1.readline().strip()
        content2 = infile2.readline()
infile1.close()
infile2.close()
outfile.close()

# -----Code from teacher:----- (使用sys.stdout.write()，并考虑如果两个文件的其中一个文件比另一个文件的行数要多的情况)
import sys
# Ask for filenames
filename1 = input("Enter first file: ")
filename2 = input("Enter second file: ")

# Open files
filehandle1 = open(filename1, 'r')
filehandle2 = open(filename2, 'r')

# Read files simultaneously
line1 = filehandle1.readline()
line2 = filehandle2.readline()
while line1 != '' and line2 != '':
    sys.stdout.write(line1[:-1] + "\t" + line2);
    line1 = filehandle1.readline()
    line2 = filehandle2.readline()
while line1 != '':
    sys.stdout.write(line1[:-1] + "\t\n");
    line1 = filehandle1.readline()
while line2 != '':
    sys.stdout.write("\t" + line2);
    line2 = filehandle2.readline()

# Close files
filehandle1.close()
filehandle2.close()






#7. Make complement strand of DNA
import sys

# Open the file and store DNA to a variable
infile = open('dna.dat', 'r')
dna = ''
for line in infile:
        dna += line.strip()
infile.close()

# Change all the base-pairs to complements and store them in another variable
complement_dna = ''
for base in dna:
        if base == 'A':
                complement_dna += 'T'
        elif base == 'T':
                complement_dna += 'A'
        elif base == 'G':
                complement_dna += 'C'
        elif base == 'C':
                complement_dna += 'G'
        else:
                print('You got wrong DNA sequence!')
                sys.exit(1)
print('7. The complements DNA is:\n', complement_dna)

#8. Reverse the complement sequence
reverse_dna = complement_dna[::-1]
print('8. The reverse DNA is:\n', reverse_dna)

#9. Write reverse DNA to revdna.dat
outfile = open('revdna.dat', 'w')
i = 0
while i < len(reverse_dna):
        outfile.write(reverse_dna[i:i+60]+'\n')
        i += 60
outfile.close()
print('9. The results are stored in revdna.dat')

#10. Keep the first line and reverse complement the sequence in dna.fsa
import sys

# Open the file and store DNA to a variable
infile = open('dna.fsa', 'r')
dna = ''
first_line = ''
for line in infile:
        if '>' in line:
                first_line += line.strip()
        else:
                dna += line.strip()
infile.close()

# Change all the base-pairs to complements and store them in another variable
complement_dna = ''
for base in dna:
        if base == 'A':
                complement_dna += 'T'
        elif base == 'T':
                complement_dna += 'A'
        elif base == 'G':
                complement_dna += 'C'
        elif base == 'C':
                complement_dna += 'G'
        else:
                print('You got wrong DNA sequence!')
                sys.exit(1)
reverse_dna = complement_dna[::-1]

# Write the first line and sequence into revdna.fsa
outfile = open('revdna.fsa', 'w')
outfile.write(first_line+' ComplementStrand\n')
i = 0
while i < len(reverse_dna):
        outfile.write(reverse_dna[i:i+60]+'\n')
        i += 60
outfile.close()

#11. Count ATCG in dna.fsa
import sys

infile = open('dna.fsa', 'r')
infile.readline()   #skip the first line
A_num = 0
T_num = 0
G_num = 0
C_num = 0
for line in infile:
        for i in range(len(line)):
                if line[i] == 'A':
                        A_num += 1
                elif line[i] == 'T':
                        T_num += 1
                elif line[i] == 'G':
                        G_num += 1
                elif line[i] == 'C':
                        C_num += 1
                else:
                    print('Unknown base')
                    sys.exit(1)
print('11. The number of ATGC are', A_num, ',', T_num, ',', G_num, ',', C_num)
infile.close()

#12. Build the bullseye
import math

# Regulate the size of the bullseye
rows = 40
cols = 40

# Name the x and y coordinates of the center point
x0 = rows/2
y0 = cols/2
max_distance = math.sqrt(x0 ** 2 + y0 ** 2);

# Begin to put the symbol on each position
for x in range(0, rows+1):
    for y in range(0, cols+1):
        distance = math.sqrt((x - x0) ** 2 + (y - y0) ** 2);
        percent = distance/max_distance;
        # Rank each point according to its distance from the center
        if percent < 0.1:
            char = '#'
        elif percent < 0.3:
            char = '.'
        elif percent < 0.5:
            char = '+'
        elif percent < 0.7:
            char = '*'
        else:
            char = ' '
        print(char, end='')
