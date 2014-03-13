__author__ = 'Kavin'

import re
import sys

input_file = open(sys.argv[1], 'r')

##sequences = []
count = 0
for line in input_file:
    searchseq = re.search( r'Sequence: (.*)?\s$', line, re.M)
    if searchseq:
        count += 1
        #print line
        print '>',count,'\n',searchseq.group(1),'\n',

##print sequences

## input_file.readlines()
## input_file.read()
