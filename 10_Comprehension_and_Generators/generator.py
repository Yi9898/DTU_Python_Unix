#!/usr/bin/env python3
#Week10: Examples for building generators


# Eg1.
def myrange(number):
    result = 1
    while result <= number:
        yield result
        result += 1

g = myrange(10)         # First assign the function to build a generator g
print(next(g))          # Next use next() function to run the generator

for i in myrange(10):
    print(i)




# Eg2.
import random
def randomgene(minlength, maxlength):
    '''Return a number of codons between minlength and maxlength'''
    if minlength < 2 or minlength > maxlength:
        raise ValueError('Wrong minlength and/or maxlength')
    # Give the initial start codon
    yield 'ATG'
    stopcodons = ('TGA', 'TAG', 'TAA')
    # Compute codons in gene minus start/stop codons
    codoncount = random.randrange(minlength, maxlength+1) - 2
    while codoncount > 0:
        codon = ''.join([random.choice('ATCG') for i in range(3)])
        if codon not in stopcodons:
           yield codon
           codoncount -= 1
    # Finally give a stop codon
    yield random.choice(stopcodons)

# Finally using it
print(''.join(randomgene(40,50)))
for codon in randomgene(50,100):
    print(codon)




# Eg3.
def generate_mers(template):
    '''Return different possible combination of kmers according to the template'''
    charlist = template.split('|')
    if 0 in [len(x) for x in charlist]:
        raise ValueError('Wrong template: ' + template)
    counter = [0 for x in charlist]
    start = 0
    while start < len(charlist):
        mer = ''
        for (pos, charpos) in enumerate(counter):
            mer += charlist[pos][charpos]
        yield mer
        start = 0
        while start < len(charlist):
            counter[start] += 1
            if counter[start] == len(charlist[start]):
                counter[start] = 0
                start += 1
            else:
                break

for mer in generate_mers('ATCG|T|GC|G'):
    print(mer)
