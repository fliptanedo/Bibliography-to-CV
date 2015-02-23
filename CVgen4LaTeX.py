#! /usr/bin/env python
# CVgen4LaTeX.py version 1.0
# Flip Tanedo, 18 August 2013
# based on CVgenerator
# requires: bib4LaTeX.py 
#
# What it does: takes InSpires output and returns a snippit for 
# a LaTeX CV file.
#
# To run:
#   make sure this file has permission to be run 
#       chmod 777 CVgenerator.py
#   run script
#       ./CVgen4LaTeX.py input.txt output.txt exception.txt
#
#   input.txt: .bib file from Inspire (search using bibtex output)
#   output.txt: file to be overwritten with html snippet
#   exception.txt: list of bibliography IDs to ignore (optional)
#
# -------------------------------------------------------------------------- #

import sys                          # module for accessing arguments
# from bib4LaTeX import bib4LaTeX     # class that holds each bibitem


print "\n"
print "CVgen4LaTeX.py version 1.0"
print "by Flip Tanedo, October 2013"
print "---------------------------"
print "Takes in Inspire output and returns LaTeX snippit."
print "Input: `LaTeX (US)' file, output text file, input list of exceptions"
print "\n"

# infile = open('inspireout.bib','r')

infile  = open(sys.argv[1],'r')	# Open input bib file for reading
outfile = open(sys.argv[2],'w')	# Open output text file for writing

exlist  = [] # list of bib IDs that should be ignored


# Deal with exceptions
if len(sys.argv) > 3:
    exfile  = open(sys.argv[3],'r')	# Open input exception file for reading
    for line in exfile:
        if line.split() == []:
            continue
        else:
            exlist.append(line.strip())
    exfile.close()

currentId = 'firstElement'  # generic ID that is not in the exception list

print 'Not including citations with IDs:'
print exlist
print '\n'

authorBool = False # flag after each \bibitem call (to store the author list)

# Process
for line in infile:
    # print line
    if line.split() == []: # if line is white space
        continue
    if line[:7] == '%\cite{':
        if currentId != 'firstElement':
            if not (currentId in exlist):
             outfile.write('\n\\vspace{-2mm}\n \n' )
             print line
        currentId = line.split('{')[1].split('}')[0]
        # print currentId
    if currentId in exlist:
        continue 
    if authorBool == True: # this is the list of authors
        authorList = line  # store for printing after the title
        line = ''          # empty out this contribution
        authorBool = False 
    if line[:9] == '\\bibitem{':
        authorBool = True # next line is the author list
        continue
    if line[:5] == '  %``':
        # print line[3:]
        # outfile.write(line[3:])
        line = line[3:]
        #
        # This is where we put in some kludges
        if line[2:13] == 'SUSY_FLAVOR': 
            line = '``\\texttt{SUSY\_FLAVOR}' + line[13:]
        if line[2:60] == 'Complete One-Loop MSSM Predictions for B --> lepton lepton':
            line = '``Complete one-loop predictions for $B_s \\rightarrow \\ell^+\\ell\'^-$ in the MSSM\'\', \n'
        #
        #
        line = line + authorList # author list after the title
    if line[:9] == '  [arXiv:':
        line = '\\texttt{' + line[3:len(line)-3] + '} \n'
    if line[:8] == '  arXiv:':
        line = '\\texttt{' +  line[2:len(line)-2] + '} \n'
    outfile.write(line)
        



print '\n'


infile.close()
outfile.close()