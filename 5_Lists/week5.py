#!/usr/bin/env python3
# Exercise for Lists/Sequences
import sys

# Ex1: Save the input words to a file until it is "STOP"
# Ask for words and append them to a list
word_list = []
word = ''
while word.upper() != 'STOP':
    word = input('Enter a word you like or STOP: ')
    word_list.append(word)

# Add the words to the file
try:
    outfile = open('words.txt', 'w')
    for word in word_list[:-1]: # remove "STOP"
        outfile.write(word + '\n')
    outfile.close()
except IOError as err:
    print('Cannot write file, reason:', str(err))
    sys.exit(1)



# Ex2
# Read the file and make the list
word_list = []
try:
    infile = open('words.txt', 'r')
    for line in infile:
        word_list.append(line[:-1])
    infile.close()
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Sort and reverse the list
word_list.sort(reverse=True)

# Write the list back to file
try:
    outfile = open('words.txt', 'w')
    outfile.write(' '.join(word_list))
    outfile.close()
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)



# Ex3: Find and clean the overlapped accession numbers
# Read the accession number into a list
try:
    infile = open('ex5.acc', 'r')
    acc_list = infile.readlines()
    acc_list = ' '.join(acc_list).split() # delelte all the "\n"
    infile.close()
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Sort and find duplicates
acc_list.sort(key=str.lower)
clean_list = []
for i in range(len(acc_list)-1):
    if acc_list[i] == acc_list[i+1]:
        continue
    clean_list.append(acc_list[i])

# # By teacher:
# previous = ''
# cleanlist = []
# for accno in acclist:
#     if previous != accno:
#         cleanlist.append(accno)
#         previous = accno

# Write the list to the file
try:
    outfile = open('clean.acc', 'w')
    outfile.write(' '.join(clean_list))
    outfile.close()
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)



# Ex4: Improve/change the previous exercise by using the pop method to eliminate duplicates.
# Read the accession number into a list
try:
    infile = open('ex5.acc', 'r')
    acc_list = infile.readlines()
    acc_list = ' '.join(acc_list).split() # delelte all the "\n"
    infile.close()
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Sort and delete duplicates using pop (只要第一个位置和第二位置的acc相等，就去掉第一个，这时第二个位置就成了第一个位置)
acc_list.sort(key=str.lower)
i = 0
while i < len(acc_list)-1:
    if acc_list[i] == acc_list[i+1]:
        acc_list.pop(i)
    else:
        i += 1

# Write the list to the file
try:
    outfile = open('clean.acc', 'w')
    outfile.write(' '.join(acc_list))
    outfile.close()
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)



# Ex5: Check whether the input accession number is in clean.acc
# Pseudocode below:
# Open and read file
# Save each accession number into a clean_list
# Ask for input acc_num
# while acc_num != STOP:
    # flag = False
    # for i in range(len(clean_list)):
        # if clean_list[i] == acc_num:
            #flag = True
            # print('exist')
    # if flag = False:
        # print('does not exist')
    # Ask for input acc_num again

# Read clean accession number into a list
try:
    infile = open('clean.acc', 'r')
    clean_list = infile.readlines()
    clean_list = ' '.join(clean_list).split() # delelte all the "\n"
    infile.close()
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Ask for input accession number
acc_num = input('Enter an accession number or STOP: ')
while acc_num.upper() != 'STOP':
    flag = False
    # find identical acc_num one by one in the list
    for i in range(len(clean_list)):
        if clean_list[i] == acc_num:
            flag = True
            print(acc_num, 'is found in the list')
    # situatioin that acc_num is not found
    if flag == False:
        print(acc_num, 'is not in the list')
    # Ask input again until it is "STOP"
    acc_num = input('Enter an accession number or STOP: ')



# Ex6: Repeat Ex5 again but using binary search this time
# Read clean accession number into a list
try:
    infile = open('clean.acc', 'r')
    clean_list = infile.readlines()
    clean_list = ' '.join(clean_list).split() # delelte all the "\n"
    infile.close()
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Ask for acc_num until it is "STOP"
while True:
    acc_num = input('Enter an accession number or STOP: ')
    if acc_num.upper() == "STOP":
        break
    # Find acc_num using binary search
    left = 0
    right = len(clean_list) - 1
    # Shrink the searching range until acc_num is found
    while left <= right:
        mid = left + (right - left) // 2
        if clean_list[mid] < acc_num:
            left  = mid + 1
        elif clean_list[mid] > acc_num:
            right = mid - 1
        else:
            print(acc_num, 'is found in the list')
            break
    if left > right:
        print(acc_num, 'is not in the list')




# Ex7: Improve some of the old programs by adding a command line interface

# Improve exercise 4.2: Find mean value of two numbers in the file integer.txt
if len(sys.argv) == 1:                   # Useage: ./week5.py < integer.txt
    num1 = int(sys.stdin.readline())
    num2 = int(sys.stdin.readline())
elif len(sys.argv) == 3:                 # Useage: python week5.py 78 42
    num1 = int(sys.argv[1])
    num2 = int(sys.argv[2])
else:
    print('Wrong use of the command!')
    sys.exit(1)
mean_value = (num1 + num2) / 2
print('4.2 The integers and their mean value are', num1, ',', num2, ',', int(mean_value))


# Improve exercise 4.3: Count the number of negative numbers in ex1.dat
if len(sys.argv) == 1:                      # Usage: python week5.py
    filename = input('Give me the filename that you want to execute: ')
elif len(sys.argv) == 2:                    # Usage: python week5.py ex1.dat
    filename = sys.argv[1]
else:
    print('Wrong use of the command!')
    sys.exit(1)
infile = open(filename, 'r')
neg = 0
for line in infile:
        for i in range(len(line)):
                if line[i] == '-':
                        neg += 1
print('4.3 The negative numbers are', neg)
infile.close()




# Ex8: Make a Python program that works a bit like unix cut.
if len(sys.argv) == 1:                  # situation of no arguments
    print('Usage: week5.py <columns you want to cut> <filename>')
    sys.exit(1)
elif len(sys.argv) > 1:                 # situation of having arguments
    try:
        infile = open(sys.argv[-1], 'r')
        outfile = open('columns.dat', 'w')
    except IOError as err:
        print('Cannot open file, reason:', str(err))
        sys.exit(1)

    # ensure which columns to extract
    col = sys.argv[1:-1]
    # extract each element of the columns line by line
    for line in infile:
        new_line = []
        for i in range(len(col)):
            new_line.append(line.split('\t')[int(col[i])-1])
        outfile.write('\t'.join(new_line) + '\n')
    infile.close()
    outfile.close()




# Ex9: Calculate the three sums of the three columns in one reading of the file ex1.dat
# Read the file
if len(sys.argv) != 2:                  # situation of no arguments
    print('Usage: week5.py <filename>')
    sys.exit(1)
if len(sys.argv) == 2:
    try:
        infile = open(sys.argv[1], 'r')
    except IOError as err:
        print('Cannot open file, reason:', str(err))
        sys.exit(1)

    # Calculate the sum of each column
    sum1 = 0
    sum2 = 0
    sum3 = 0
    for line in infile:
        sum1 += float(line.split('\t')[0])
        sum2 += float(line.split('\t')[1])
        sum3 += float(line.split('\t')[2])
    print('The sums of each column are', sum1, sum2, sum3, ',', 'respectively.')




# Ex10: Calculates the sum of all columns in the file
# Read the file
if len(sys.argv) != 2:                  # situation of no arguments
    print('Usage: week5.py <filename>')
    sys.exit(1)
if len(sys.argv) == 2:
    try:
        infile = open(sys.argv[1], 'r')
    except IOError as err:
        print('Cannot open file, reason:', str(err))
        sys.exit(1)

    # Read the first line to initialize sum_list
    sum_list = []
    line1 = infile.readline()
    for i in range(len(line1.split())):
        sum_list.append(float(line1.split()[i]))
    # Calculate the sum of each column
    for line in infile:
        for i in range(len(line.split())):
            sum_list[i] += float(line.split()[i])
    # Print results
    print('The sums of each colum in the file are\n')
    for sum in sum_list:
        print(sum)
