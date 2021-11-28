#!/usr/bin/env python3
low = 1
high = 10
print("Think of a number between", low, "and", high, "(both inclusive)")
answer = input("Press <Enter> when you are ready ")
guess = int((low+high)/2)
# Guess loop
while answer != 'yes':
    answer = input("Is it " + str(guess) +" ?? Answer yes, higher or lower ")
    if answer == 'lower':
        guess -= 1
    if answer == 'higher':
        guess += 1
    # Infer answer in the extremes
    if guess == high or guess == low:
        answer = 'yes'  
print("I guessed it. It is", guess)
