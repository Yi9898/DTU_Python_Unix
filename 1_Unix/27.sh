#!/bin/bash
#Author: Yi 
#Date: 30/08/2021
#The first six lines are to extract the positive and negative number from every column and save them into new files. k1 means the first column, etc.
#The middle two lines are to merge the negative and positive number of each lineto new files.
#The last line is to remove the temporary files that were created previously.

cut -f1 ex1.dat | grep "-" > k1.neg    
cut -f1 ex1.dat | grep -v "-" > k1.pos
cut -f2 ex1.dat | grep -v "-" > k2.pos
cut -f2 ex1.dat | grep "-" > k2.neg
cut -f3 ex1.dat | grep "-" > k3.neg
cut -f3 ex1.dat | grep -v "-" > k3.pos

cat k1.neg k2.neg k3.neg > ex1.neg2
cat k1.pos k2.pos k3.pos > ex1.pos2

rm k1.neg k1.pos k2.neg k2.pos k3.neg k3.pos 
