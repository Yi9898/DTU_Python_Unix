#!/usr/bin/env python3
# Project: Pairwise Alignment for DNA and protein sequences
# Authors: Yi and Chen
import sys, re

### Functions ###
def DNA_similarity_matrix(seq1, seq2):
    '''Return the similarity matrix of DNA sequences by adding match score or mismatch penalty'''
    # Intialize parameters
    simMatrix = list()
    match_score = 1
    mismatch_penalty = -1

    # Initialize the similarity matrix with zero
    for i in range(len(seq1)):
        simMatrix.extend([[0]*(len(seq2))])

    # Similarity matrix filling
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if seq1[i] == seq2[j]:
                simMatrix[i][j] = match_score
            else:
                simMatrix[i][j] = mismatch_penalty
    return simMatrix


def AA_similarity_matrix(seq1, seq2):
    '''Return the similarity matrix of protein sequences by adding match score or mismatch penalty'''
    # Intialize parameters
    simMatrix = list()
    sub_matrix = load_PAM('PAM250.txt')

    # Initialize the similarity matrix with zero
    for i in range(len(seq1)):
        simMatrix.extend([[0]*(len(seq2))])

    # Similarity matrix filling according to PAM250
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            try:
                simMatrix[i][j] = int(sub_matrix[seq1[i]][seq2[j]])
            except ValueError as error:
                sys.stderr.write("Can't find substitution score in PAM250, reason: " + str(error) + "\n")
                sys.exit(1)
    return simMatrix


def load_PAM(matrix_filename):
    '''Return a transformed dict for the raw PAM250.txt'''
    # Read file
    try:
        infile = open(matrix_filename, 'r')
    except IOError as error:
        sys.stderr.write("Can't read file, reason: " + str(error) + "\n")
        sys.exit(1)

    # Extract main parts
    matrix = infile.read()
    lines = matrix.strip().split('\n')
    header = lines[0]
    columns = header.split()
    matrix = dict()

    # Build the dict
    for row in lines[1:]:
      items = row.split()
      matrix[items[0]] = dict()
      for i in range(1, len(items)):
          matrix[items[0]][columns[i-1]] = items[i]
    infile.close()
    return matrix


def needleman_wunsch(seq1, seq2):
    '''Return the filled main matrix using Needleman algorithm'''

    # 1. Intialization
    mainMatrix = list()
    gap_penalty = -2
    # Distinguish the sequences between DNA and protein
    if seq1[0] == 'M' and seq2[0] == 'M':
        simMatrix = AA_similarity_matrix(seq1, seq2)
    elif seq1[0] != 'M' and seq2[0] != 'M':
        simMatrix = DNA_similarity_matrix(seq1, seq2)
    else:
        raise ValueError('The categories of two sequences are not the same.')
        sys.exit(1)

    # Initialize the main matrix
    for i in range(len(seq1)+1):
        mainMatrix.extend([[0]*(len(seq2)+1)])


    # 2. Matrix filling
    for i in range(len(seq1)+1):
        mainMatrix[i][0] = i * gap_penalty
    for j in range(len(seq2)+1):
        mainMatrix[0][j] = j * gap_penalty

    # Fill in the remaining rows and colums
    for i in range(1, len(seq1)+1):
        for j in range(1, len(seq2)+1):
            mainMatrix[i][j] = max(mainMatrix[i-1][j-1] + simMatrix[i-1][j-1],
                                   mainMatrix[i-1][j] + gap_penalty,
                                   mainMatrix[i][j-1] + gap_penalty)


    # 3. Traceback
    # Parameter initialization
    align1 = ''
    align2 = ''
    i = len(seq1)
    j = len(seq2)

    while i > 0 or j > 0:
        # Go to the diagonal position
        if i > 0 and j > 0 and (mainMatrix[i][j] == mainMatrix[i-1][j-1]  + simMatrix[i-1][j-1]):
            align1 += seq1[i-1]
            align2 += seq2[j-1]
            i -= 1
            j -= 1

        # Go the upper position
        elif i > 0 and (mainMatrix[i][j] == mainMatrix[i-1][j] + gap_penalty):
            align1 += seq1[i-1]
            align2 += '-'
            i -= 1

        # Go to the left position
        else:  #j > 0 and (mainMatrix[i][j] == mainMatrix[i][j-1] + gap_penalty)
            align1 += '-'
            align2 += seq2[j-1]
            j -= 1

    return align1[::-1], align2[::-1]


def extract_seq(fsa_file):
    '''Return the sequence dictionary of two sequences in the fasta file'''
    try:
        infile = open(filename, 'r')
        # Initialize
        seq_dic = dict()
        seq_num = 0
        # Collect data into seq_dic
        for line in infile:
            if line.startswith('>'):
                seq_num += 1
                # Extract the name of each sequence
                name = line.split()[0]
                if name not in seq_dic.keys():
                    seq_dic[name] = ''
                else:
                    sys.stderr.write("You got same DNA sequences to be aligned in <filename>\n")
                    print('The sequences 100% match with one another.')
                    sys.exit(1)
                continue
            else:
                seq_dic[name] += line.strip()
        # Error handling of multiple sequences in the file
        if seq_num != 2:
            raise VauleError("Your <filename> should only contain two sequences to be aligned\n")
            sys.exit(1)

    except IOError as error:
        sys.stderr.write("Can't read file, reason: " + str(error) + "\n")
        sys.exit(1)
    infile.close()
    return seq_dic


def align(fsa_file):
    '''Return the two aligned sequences and their corresponding identifiers stored in string variables'''
    seq_dict = extract_seq(fsa_file)
    sequences = list()
    identifiers = list()
    for key, value in seq_dict.items():
        identifiers.append(key)
        sequences.append(value)
    aligned1, aligned2 = needleman_wunsch(sequences[0], sequences[1])
    return aligned1, aligned2, identifiers


def write_result(aligned_seq1, aligned_seq2, name_list):
    '''Return the final output file showing the aligned sequences'''
    # Reformat and store the two aligned sequences
    if len(aligned_seq1) == len(aligned_seq2):
        (tmp, rest1, rest2, i) = ('', '', '', 0)
        while len(aligned1) >= i+60:
            tmp += aligned1[i:i+60]
            tmp += aligned2[i:i+60]
            i += 60
        # store the rest of two aligned sequences
        rest1 += aligned1[i:]
        rest2 += aligned2[i:]
    else:
        raise ValueError('Wrong methods used in global alignment.')
        sys.exit(1)

    # Write output file
    try:
        outfile = open('aligned.fsa', 'w')
        for i in range(0, len(tmp), 60):
            # write the line with title name of each sequence
            if (i/60)%2 == 0:
                outfile.write(name_list[0] + ': ' + tmp[i:i+60] + '\n')
            elif (i/60)%2 == 1:
                outfile.write(name_list[1] + ': ' + tmp[i:i+60] + '\n')
        outfile.write(name_list[0] + ': ' + rest1 + '\n')
        outfile.write(name_list[0] + ': ' + rest2 + '\n')
        outfile.close()
    except IOError as error:
        sys.stderr.write("Can't write file, reason: " + str(error) + "\n")
        sys.exit(1)






### Main Code ###

# Get input file name
if len(sys.argv) == 1:   # no commandline arguments
    filename = input('Please enter a fasta filename containing two sequences to be aligned: ')
elif len(sys.argv) == 2: # something is there
    filename = sys.argv[1]
else:
    sys.stderr.write('Usage: Pairwise_align.py <filename>\n')
    sys.exit(1)

# Alignment
aligned1, aligned2, identifiers = align(filename)

# Get output file
write_result(aligned1, aligned2, identifiers)

# Job done
print('Job done. Please check the result in <aligned.fsa>')
