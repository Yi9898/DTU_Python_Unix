#!/bin/python3
import sys, re


#Classic file reading

#If no commandline arguments
if len(sys.argv) == 1:
    Fasta_file=input("Please enter sequences file: ")
    Motifs_file=input("Please enter motifs file: ")
    Deviation=int(input("Which deviation should I accept? "))
    
#If there is something there                   
elif len(sys.argv) == 4:	                                                   
    Fasta_file = sys.argv[1]
    Motifs_file = sys.argv[2]
    Deviation = float(sys.argv[3])
else:
    sys.stderr.write("program.py <fasta file> <motifs file> <deviation>")                      
    sys.exit(1)
    

    

#All the functions used in the programm are defined 
    
def motifs_creator(infile):
    """Read through motifs file and save the base pair and penalty in a list of lists"""
    
    #Initialize variables
    (motifs_value,lengths,gaps) = ([],[],[])
    values = list()
    motif_len = 0
    
    #Open motifs file and parse through it
    motifs_infile = open(infile,"r")
    for line in motifs_infile:
        #If line is a comment just skip it    
        if line[0] == "#":
            motif_len += 0
        
        else:
            try:
                #Check the input
                if len(line.split())!= 2:
                    raise IOError ("Please check motifs file")
                    
                #Save the motifs and their score in a list of lists
                elif line[0] not in ("#*"):
                    motif_len += 1                                                     
                    base = line.split()[0]
                    try:
                        score = float(line.split()[1])
                    except ValueError: 
                        print("Penalty is not defined correclty in motifs file. Please check your input \n")
                        sys.exit(1)
                    values += [[base,score]]
                    
                #A gap is found in the motif, search for the ammount of unimportant bases
                elif line[0] == "*":
                    motifs_value.append(values)
		            #if the gap is an interval
                    if re.search(r'(\-)', line.split()[1]) is not None:
                        positions = re.search(r'^(\d+)\-(\d+)$',line.split()[1])
                        try: 
                            gap = [int(positions.group(1)),int(positions.group(2))]
                        except ValueError: 
                            print("Unimportant interval should be written as: integer - integer. Please check input file\n")
                            sys.exit(1) 
                    #if it is a number
                    else:
                        positions = re.search(r'^(\d+)$',line.split()[1])
                        try: 
                            gap = [int(positions.group(1)),int(positions.group(1))]
                        except ValueError: 
                            print("Unimportant number should be an integer. Please check input file\n")
                            sys.exit(1) 
                   
                    #Append length of motif in a list and the unimportant bases in another list 
                    lengths.append(motif_len)
                    gaps.append(gap)
                    
                    #Prepare for the next motif by restarting variables 
                    values = list()
                    motif_len = 0  
                    
            except IOError as error:
                print(error)
                sys.exit(1)
                
    #Save the last motif found
    motifs_value.append(values)
    lengths.append(motif_len)

    #Close motifs file and return the variables
    motifs_infile.close() 

    return(motifs_value,lengths,gaps)




def match_finder(sequence,length,motifs,deviation):
    """Search for matches in sequence and save them in a list"""
    
    #Initialize variable
    match = list()
    
    #Search through the sequence for a motif
    for pos in range(len(sequence)-length):
        dev = 0
        for motif_pos in range(0,length):
            #Check if the value of motif in a partiqular position can only be a nucleotide and add the deviation if it doesn't match with the position in sequence
            if len(motifs[motif_pos][0]) == 1:
                if sequence[pos+motif_pos] != motifs[motif_pos][0]:
                    dev += int(motifs[motif_pos][1])
            #If more than one possible nucleotide, add the deviation and later substract it if there is a match found between sequence and the possible nucleotides
            else:
                dev += int(motifs[motif_pos][1])
                for base in range(len(motifs[motif_pos][0])):
                    if sequence[pos+motif_pos] == motifs[motif_pos][0][base]:
                        dev -= int(motifs[motif_pos][1])
                            
        #Compare the deviation with the input value, if smaller append the match on a list          
        if dev <= deviation:
            match += [[pos,pos+length,dev]]

    return(match)




def deviation_func(res, motif1, motif2, deviation, len1, len2):
    """Calculate the total deviation and the gaps between the first two parts of the motif"""                
    
    #Initialize variables and parse through every combination of matches
    results = list()
    for row1 in range(len(res[motif1])):
        for row2 in range(len(res[motif2])):
            end1 = res[motif1][row1][1]
            start2 = res[motif2][row2][0]
                            
            #If the second motif starts after the first, calculate the difference
            if start2 > end1: 
                diff = start2 - end1
                #If the difference is in the correct gap interval, calculate the total deviation
                if diff >= gap[0][0] and diff <= gap[0][1]:
                    finaldev = int(res[motif1][row1][2]) + int(res[motif2][row2][2])
                    #If the deviation is smaller than input value, save the results in a list
                    if finaldev <= Deviation:  
                        results += [[end1-len1,start2+len2,finaldev,[diff]]]
                        
    return(results)




def total_deviation(prev_res, res, motif, deviation, len2):
    """Calculate the total deviation when more than 2 parts in motifs file"""                
    
    #Initialize variable and parse through every combination of previous result and following part in matches 
    total_results = list()
    for row1 in range(len(prev_res)):
        for row2 in range(len(res[motif])):
            differences = list()
            end1 = prev_res[row1][1]
            start2 = res[motif][row2][0]

            #If the second motif starts after the first, calculate the difference
            if start2 > end1: 
                diff = start2 - end1
                #If the difference is in the correct gap interval, calculate the total deviation
                if diff >= gap[(motif-1)][0] and diff <= gap[(motif-1)][1]:
                    finaldev = int(prev_res[row1][2]) + int(res[motif][row2][2])
                    #If the deviation is smaller than input value, append the amount of unimportant bases between the parts and save the results 
                    if finaldev <= Deviation:
                        differences += prev_res[row1][3]
                        differences += [diff]
                        total_results += [[prev_res[row1][0],start2+len2,finaldev,differences]]
                      
    return(total_results)



def position_finder(res_list,row,col):
    """Calculate the position of a match in order to print it in the results"""
    if col == 0:
        start = res_list[row][col]
        end = res_list[row][col]+ size[col]
    if col == 1:
        end = res_list[row][col]
        start = res_list[row][col]- size[col]

    sequence = str(seq[start:end])
    
    return(start,end,sequence)



#On to the main algorithm

#Extract the nessecery information from motifs creator function
motif_score = motifs_creator(Motifs_file)[0] 
size = motifs_creator(Motifs_file)[1]
gap = motifs_creator(Motifs_file)[2] 


#Initialize variables and start parsing through the sequences
(seq, header) = ('', '')
matches = list()
# Open the sequence file and an outfile to write the results
infile = open(Fasta_file, 'r')
outfile = open('found_motifs.txt', 'w')
# Find header line
for line in infile:
    if line != '' and line[0] == '>':
        header = line
        #Check if there is a sequence saved and search for matches in every part of motifs  
        if seq != "":
            for part in range(len(motif_score)):
                matches += [match_finder(seq, size[part], motif_score[part], Deviation)]
                
            #Check the amount of parts included in the motif
            #If there is just one part
            if len(motif_score) == 1:
                #If there are no matches found, state it in the output file
                if len(matches[0]) == 0:
                    outfile.write("No results found \n")
                #If there are, calculate the start and end position and write them in the output file
                else:
                    for i in range(len(matches[0])):
                        match = position_finder(matches[0],i,0)
                        outfile.write("Pos: "+str(match[0])+"-"+str(match[1])+",  Sequence: "+ match[2] +"\t")
                        outfile.write("Deviation = " + str(matches[0][i][2])+"\n")                  
            
            #If motifs include 2 parts        
            elif len(motif_score) == 2:
                #Calculate the total deviation between matches for both parts
                result = deviation_func(matches,0,1,Deviation,size[0],size[1])
    
                #Find start and end of every part and deviation and write them in output file
                for i in range(len(result)):
                    for part in range(len(motif_score)):
                        match = position_finder(result, i, part)
                        outfile.write(str(part+1)+". Pos: "+str(match[0])+"-"+str(match[1])+"  Sequence: "+ match[2] +"\t")
                    outfile.write("Deviation = " + str(result[i][2])+"\n")
                
                #If no matches found, state in in the output file
                if result == []:
                    outfile.write("No results found \n")
            
            #If motifs include more than 2 parts
            elif len(motif_score) > 2:
                #Search for matches between the first two parts
                result = deviation_func(matches,0,1, Deviation,size[0],size[1])
                
                if result != [[]]:
                    #Calculate the deviation between the results from previous parts and the next part  
                    for part in range(2, len(motif_score)):
                        new_result = total_deviation(result, matches, part, Deviation, size[part])
                        result = new_result
                
                #Find start and end of first part and write them in output file       
                for i in range(len(new_result)):
                    s = position_finder(new_result, i, 0)
                    outfile.write("1. Pos: "+str(s[0])+"-"+str(s[1])+"  Sequence: "+ s[2] +",\t")
                    
                    #Calculate the start and end position of the other parts and write them in the output file 
                    end = s[1]
                    for part in range(len(new_result[i][3])):
                        new_start = end + new_result[i][3][part]
                        new_end = new_start + size[part+1]
                        sequence = str(seq[new_start:new_end])
                        outfile.write(str(part+2)+". Pos: "+str(new_start)+"-"+str(new_end)+"  Sequence: "+ sequence +",\t")
                        end = new_end
                    
                    #Write down the total deviation 
                    outfile.write("Deviation = " + str(new_result[i][2])+"\n")
                
                #If no results found state that 
                if new_result == []:
                    outfile.write("No results found \n")
            
        #Write the header of the following sequence and restart variables      
        outfile.write(header)        
        seq = ''
        matches = list()
        
    #If the line doesn't include a header save the sequence    
    elif line[0] != '>':
        seq += line[:-1]


#repeat everything for the last sequence
if seq != "":
    for part in range(len(motif_score)):
        matches += [match_finder(seq, size[part], motif_score[part], Deviation)]
        
    #Check the amount of parts included in the motif
    if len(motif_score) == 1:
        if len(matches[0]) == 0:
            outfile.write("No results found \n")
            for i in range(len(matches[0])):
                match = position_finder(matches[0],i,0)
                outfile.write("Pos: "+str(match[0])+"-"+str(match[1])+",  Sequence: "+ match[2] +"\t")
                outfile.write("Deviation = " + str(matches[0][i][2])+"\n")                  
    
    #If motifs include 2 parts        
    elif len(motif_score) == 2:
        result = deviation_func(matches,0,1,Deviation,size[0],size[1])

        for i in range(len(result)):
            for part in range(len(motif_score)):
                match = position_finder(result, i, part)
                outfile.write(str(part+1)+". Pos: "+str(match[0])+"-"+str(match[1])+"  Sequence: "+ match[2] +"\t")
            outfile.write("Deviation = " + str(result[i][2])+"\n")
        
        if result == []:
            outfile.write("No results found \n")
    
    #If motifs include more than 2 parts
    elif len(motif_score) > 2:
        result = deviation_func(matches,0,1, Deviation,size[0],size[1])
        
        if result != [[]]:
            for part in range(2, len(motif_score)):
                new_result = total_deviation(result, matches, part, Deviation, size[part])
                result = new_result
             
        for i in range(len(new_result)):
            s = position_finder(new_result, i, 0)
            outfile.write("1. Pos: "+str(s[0])+"-"+str(s[1])+"  Sequence: "+ s[2] +",\t")
            
            end = s[1]
            for part in range(len(new_result[i][3])):
                new_start = end + new_result[i][3][part]
                new_end = new_start + size[part+1]
                sequence = str(seq[new_start:new_end])
                outfile.write(str(part+2)+". Pos: "+str(new_start)+"-"+str(new_end)+"  Sequence: "+ sequence +",\t")
                end = new_end
            
            outfile.write("Deviation = " + str(new_result[i][2])+"\n")
        
        if new_result == []:
            outfile.write("No results found \n")
    

#Close files
outfile.close()
infile.close()

            
print("Your results are ready in file:", outfile.name)
