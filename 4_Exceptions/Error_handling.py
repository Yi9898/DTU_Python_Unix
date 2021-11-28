#!/usr/bin/env python3


import sys
try:
    number = int(input('Please input a small positive number:'))
    assert number > 0 and number < 10, 'Number out of range'
except ValueError:
    print('You don’t know what a number is')
    sys.exit(1)
except AssertionError as err:
    print(str(err))
