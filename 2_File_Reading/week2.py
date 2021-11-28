#!/usr/bin/env python3
#Author: Yi
#Exercise for Week2: Python simple file reading

print('Question 1')
with open('ex1.acc', 'r') as infile:
	for line in infile:
		print(line, end='') #不换行输出
infile.close()

print('Question 2')
filename = input('Enter a file name from ex1.acc/ex1.dat: ')
with open(filename, 'r') as infile:
	for line in infile:
		print(line)
infile.close()

print('\nQuestion 3-9')
#I have used "cut -f" command to construct three files called 'col1.dat', 'col2.dat' and 'col3.dat', respectively. Also, I have constructed a file called 'test.txt' containing number 9-1.

filename = input('Enter a file name from col1.dat/col2.dat/col3.dat: ')
with open(filename, 'r') as infile:
	count = 0                 #line numbers
	sum = 0                   #sum of the numbers
	neg = 0                   #negative number
	pos = 0                   #positive number
	zero = 0                  #number of zeros
	num_list = []             #a list of numbers in the file
	for line in infile:
		count += 1
		sum += float(line.strip()) #convert string to number
		if float(line.strip()) < 0:
			neg += 1
		elif float(line.strip()) > 0:
			pos += 1
		else:
			zero += 1
		num_list.append(float(line.strip()))
	max_num = max(num_list)
	min_num = min(num_list)
	print('3. The number of lines is', count)
	print('4. The sum of the numbers is', sum)
	print('5. The mean value is', sum / count)
	print('6. The negative, positive and zero numbers are', neg, ',', pos, ',', zero)
	print('7. The maximum number is', max_num)
	print('8. The minimum number is', min_num)
	print('9. It has already been done')
infile.close()

###Code from Peter:
# Initializing values
positive = 0
negative = 0
zero = 0
minimum = None
maximum = None
count = 0
thesum = 0.0
# Ask for filename
filename = input("Categorizing lines. Enter file name: ")
# Open file
with open(filename, 'r') as infile:
    for line in infile:
        number = float(line)
        if minimum is None:
            minimum = number
            maximum = number
        elif number < minimum:
            minimum = number
        elif number > minimum:
            maximum = number
        if number > 0:
            positive += 1
        elif number < 0:
            negative += 1
        else:
            zero += 1
        count += 1
        thesum += number

if count == 0:
    print("Empty file")
else:
    print("The sum is:", thesum)
    print("Number of lines:", count)
    print("The mean is:", thesum/count)
    print("Maximum is:", maximum)
    print("Minimum is:", minimum)
    print("Positives:", positive)
    print("Negatives:", negative)
    print("Zeroes:", zero)

print('\nQuestion 10')
#In this case I only consider the situation of guessing an integer, otherwise the difficulty increases as the number of decimal places increases, and random, math libraries, and so on are used.

print('Please think of an integer between 1 and 10 right now.')
i = 5
print('Is number', i, '?')
answer = input('Enter yes/higher/lower: ')
while answer != 'yes':
	if answer == 'higher':
		i += 1
		print('Is number', i, '?')
		answer = input('Enter yes/higher/lower: ')
	if answer == 'lower':
		i -= 1
		print('Is number', i, '?')
		answer = input('Enter yes/higher/lower: ')
print('I guess right!')
