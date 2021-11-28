#!/usr/bin/env python3
#Author: Yi
#Exercise2: Python Basics

print('1.') #The first question
print('Hello', 'World')

print('\n2.') #The second question, etc
for i in range(10):
	print('Hello', 'World')

print('\n3.')
i = 1
while i <= 10:
	print(i)
	i += 1

print('\n4.')
name = input('What is you name: ')
print('Nice to meet you', name, '!')

print('\n5.')
num1 = input('Enter the first number: ')
num2 = input('Enter the second number: ')
print('The numbers are', num1, 'and', num2)
print('The sum of these two numbers is', float(num1)+float(num2))

print('\n6.')
num1 = int(input('Enter the first number: '))
num2 = int(input('Enter the second number: '))
Op = input('Enter a operation from +,-,*,/: ')
if Op == '+':
	print('The result is', num1 + num2)
if Op == '-':
	print('The result is', num1 - num2)
if Op == '*':
	print('The result is', num1 * num2)
if Op == '/':
	print('The result is', num1 / num2)

print('\n7. and 8.')
num1 = int(input('Enter the first integer: '))
num2 = int(input('Enter the second integer: '))
if num1 < num2:
	for i in range(num1, num2+1):
		print(i)
if num1 > num2:
	for i in range(num2, num1+1):
		print(i)
if num1 == num2:
	print(num1)

print('\n9.')
num1 = int(input('Enter a number: '))
num2 = int(input('Enter a number: '))
while num2 >= num1:
	num3 = int(input('Enter a number: '))
	num1 = num2
	num2 = num3

print('\n10.')
result = 1
num = int(input('Enter a positive integer: '))
if num < 0:
	print('error')
elif num == 0:
	print('The result is 1')
else:
	for i in range(1, num+1):
		result = result * i
	print('The result is', result)

print('\n11.')
result = 0
num = int(input('Enter an integer: '))
if num < 0:
	for i in range(num, 1):
		result += i
	print('The result is', result)
if num == 0:
	print('The result is', result)
if num > 0:
	for i in range(0, num+1):
		result += i
	print('The result is', result)

