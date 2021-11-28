#!/usr/bin/env python3
# Exercise for Exceptions and Bug Handling

# Exercise 2-5
import sys

# Get filename and open file
filename = input('Enter a SwissProt file: ')
try:
    infile = open(filename, 'r')
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

#Initialize variables
AA = ''
flag = False
# Iteration through file
for line in infile:

    #Ex2: Read and print ID
    # extract ID from the line
    if line[0:2] == 'ID':
        # find start of id
        pos1 = 2
        while line[pos1] == ' ':
            pos1 += 1
        pos2 = pos1 + 1
        # find end of id
        while line[pos2] != ' ':
            pos2 +=1
        id = line[pos1:pos2]

    # Ex3: Read and print accession number
    # extract AC from the line
    if line[0:2] == 'AC':
        # find start of AC
        start = 2
        while line[pos] == ' ':
            start += 1
        stop = start + 1
        # find end of AC
        while line[stop] != ';':
            stop += 1
        accno = line[start:stop]


    #Ex4: Read and print the amino sequence using sateful parsing
    # Red line
    if line[0:2] == '//':
        flag = False
    # Collect data
    if flag:
        AA += line
    # Green line
    if line[0:2] == 'SQ':
        flag = True
        # # Read the AA number in SQ line
        # pos = 16 #尽量避免这种精确数字的出现，因为有可能不适用于所有情况
        # while line[pos] != ' ':
        #     pos += 1
        # AA_num = int(line[16:pos+1])

        # By teacher:
        start = 2
        while line[start] == ' ':
            start += 1
        while line[start] != ' ':
            start += 1
        while line[start] == ' ':
            start += 1
        stop = start + 1
        while line[stop] != ' ':
            stop += 1
        AA_num = int(line[start:stop])
infile.close()




#Ex5: Verify the number of amino acids
# Count the AA number in the string variable and assign the letters to a new variable AA_clean
count = 0
AA_clean = ''
for i in AA:
    if i != ' ' and i != '\n':
        count += 1
        AA_clean += i

# Error Handling and output
try:
    if flag:
        raise ValueError("Sequence did not end correctly")
    if AA == '':
        raise ValueError('Sequence does not exist!')
    if count != AA_num:
        raise ValueError('The real number of the sequence does not match the number in SQ line')
except ValueError as err:
    print(str(err)) # By teacher: sys.stderr.write(str(error) + "\n")
    sys.exit(1)
else:
    print('The ID is', id)
    print('The accession number is', acc)
    print('The amino acid sequce is:\n', AA)


# Ex6: Save ID, accession number and AA sequence to sprot.fsa
try:
    outfile = open('sprot.fsa', 'w')
except IOError as err:
    print('Cannot write file, reason:', str(err))
    sys.exit(1)
# Write the file
outfile.write('>' + acc + ' ' + id + ' ' + str(AA_num) + 'AA' + '\n')
for i in range(0, len(AA_clean), 60):
    outfile.write(AA_clean[i:i+60] + '\n')
outfile.close()


# Ex7: Find the positions of ATG in dna.fsa
# Open the file
try:
    infile = open('dna.fsa', 'r')
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Read the file
#infile.readline() # Split the first line (但是有可能出现第一个带有">"的行出现之前，前面有很多行的情况)
# By teacher:
# Skip lines until header is found, line can not be None
line = 'dummy'
while len(line) > 0 and line[0] != '>':
    line = infile.readline()

sequence = ''
for line in infile:
    sequence += line[:-1] #不要把行末的提行符一起提取出来了
infile.close()

# Find start codons in sequence
for i in range(len(sequence)-2):
    if sequence[i:i+3] == 'ATG':
        print(i+1) #将最中间“T”的位置作为出现“ATG”的位置


# Ex8: Find the first stop codon
# Pseudocode
# for i in range(first_ATG_position + 2, sequence_length, 3)
#   stop if find STOP codon at postion i
# print stop codon and the position

# for i in range(85, len(sequence)-2, 3):
#     if sequence[i:i+3] in ('TAA', 'TAG', 'TGA'):
#         print('The first stop codon is', sequence[i:i+3])
#         print('The position is', i)
#         break

# By teacher: we can also use while instead of break
# Assuming there are no spaces in the sequence
start = 0
while start < len(dnaseq)-2 and dnaseq[start:start+3] != 'ATG':
    start += 1

# Looking for the associated stop
stop = start + 3
while stop < len(dnaseq)-2 and dnaseq[stop:stop+3] not in ('TAG', 'TGA', 'TAA'):
    stop += 3

if stop < len(dnaseq)-2:
    sys.stdout.write("Start codon at " + str(start+1) + "\n")
    sys.stdout.write("Stop codon in frame at " + str(stop+1) + "\n")
else:
    sys.stdout.write("No ORF found\n")




# Ex9: Count the number of lines with input organism in orphans.sp
#Pseudocode
# Ask for input organism
# Open orphans.sp
# for line in file
    # if line contains '>'
        # Skip to next line
    # if line contains organism
        # count the number
# Close file

# Ask for input organism and open the file
organism = input('Enter an organism, like HUMAN or RAT: ')
try:
    infile = open('orphans.sp', 'r')
except IOError as err:
    print('Cannot open file, reason:', str(err))
    sys.exit(1)

# Count the number of organism (Bad method!!! 因为其他行也可能会有很多input organism出现，需要限制范围！)
# count = 0
# for line in infile:
#     if line[0] == '>':
#         continue
#     if organism.upper() in line:
#         count += 1
# print('The number of', organism, 'is', count)
# infile.close()

# By teacher: 定位出现下划线的位置
# Reading the file and counting
count = 0
for line in infile:
    spacepos = 0
    underscorepos = -1
    #找出每一行下划线以及第一个空格的位置
    while spacepos < len(line) and line[spacepos] != ' ':
        if line[spacepos] == '_':
            underscorepos = spacepos
        spacepos += 1
    # If underscorepos is -1 the line does not contain a swissprot id
    if underscorepos != -1 and line[underscorepos+1:spacepos] == organism:
        count += 1
infile.close()




# Ex10: Gussing number game
# Assign the initial value and guess for the first time
min_num = 1
max_num = 10
print('Please think of an integer between 1 and 10 right now.')
number = int((min_num + max_num) / 2)
print('Is number', number, '?')
attempt = 1
answer = input('Enter yes/higher/lower: ')

# Continue guessing until the answer is 'yes'
while answer != 'yes':
    if answer == 'higher':
        min_num = number + 1
        number = int((min_num + max_num) / 2)
        print('Is number', number, '?')
        attempt += 1
        answer = input('Enter yes/higher/lower: ')
    if answer == 'lower':
        max_num = number - 1
        number = int((min_num + max_num) / 2)
        print('Is number', number, '?')
        attempt += 1
        answer = input('Enter yes/higher/lower: ')
print('I guess right!')
print('I have guessed', attempt, 'times')

# By teacher:
# The starting interval, both inclusive
low = 1
high = 10
print("Think of a number between ", low, "and", high, "(both inclusive)")
answer = input("Press <Enter> when you are ready ")
count = 0
# Guessing loop
while answer != 'Y' and low < high:
    guess = int((high+low)/2)
    # what says the user, ensure well defined answers
    answer = 'Guess'
    while answer not in ('Y', 'H', 'L'):
        if answer != 'Guess':
            print "Stop writing nonsense to me."
        answer = input("Is it " + str(guess) + "?? Answer yes, higher or lower: ")
        # Translating first char of answer into uppercase.
        answer = answer[0].upper()
    # narrow down interval
    if answer == 'H':
        low = guess + 1
    if answer == 'L':
        high = guess - 1
    count += 1

if high < low:
    print("You are a lier.")
else:
    if high == low:
        count += 1      # This is arguable, after all - this is not a guess.
        print("You are thinking of", low, "or you have lied to me.")
    else:
        print("That was lucky.")
    print("I used", count, "guesses.")
