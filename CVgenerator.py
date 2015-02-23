#! /usr/bin/env python
# CVgenerator.py version 1.0
# Flip Tanedo, 31 August 2013
# based loosely on my Tools2Param.py script
# requires: bibdata.py 
#
# To run:
#   make sure this file has permission to be run 
#       chmod 777 CVgenerator.py
#   run script
#       ./CVgenerator.py input.bib output.txt exception.txt
#
#   input.bib: .bib file from Inspire (search using bibtex output)
#   output.txt: file to be overwritten with html snippet
#   exception.txt: list of bibliography IDs to ignore (optional)
#
# -------------------------------------------------------------------------- #

import sys                          # module for accessing arguments
from bibdata import bibentry        # class that holds each bibitem


print "\n"
print "CVgenerator.py version 1.0"
print "by Flip Tanedo, August 2013"
print "---------------------------"
print "Takes in Inspire output and returns html snippit."
print "Input: .bib file, output text file, input list of exceptions"
print "\n"

# infile = open('inspireout.bib','r')

infile  = open(sys.argv[1],'r')	# Open input bib file for reading
outfile = open(sys.argv[2],'w')	# Open output text file for writing

exlist  = [] # list of bib IDs that should be ignored
biblist = [] # list of bibliographic entries


# Deal with exceptions
if len(sys.argv) > 3:
    exfile  = open(sys.argv[3],'r')	# Open input exception file for reading
    for line in exfile:
        if line.split() == []:
            continue
        else:
            exlist.append(line.strip())
    exfile.close()


for line in infile:
    # outfile.write(line)
    if line.split() == []: #if line is white space
        continue
    if (len(biblist) == 0) & (line[0] != '@'):
        continue # skip because first entry hasn't been defined yet
    if line[0] == '@':
        biblist.append(bibentry(line))
    else: # this must be bibliographical data (need to deal with non-data)
        biblist[len(biblist)-1].add_line(line)  # process new potential data

outfile.write('<ul>\n\n')

for bibitem in biblist:
    bibitem.process()
    if not (bibitem.id in exlist):
        # outfile.write(bibitem.htmlout() + '\n\n')
        outfile.write(bibitem.htmlout2() + '\n\n')
    else:
        print 'Skipping ' + bibitem.id

outfile.write('</ul>\n')

print '\n'


infile.close()
outfile.close()