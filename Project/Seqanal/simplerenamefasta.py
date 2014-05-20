__author__ = 'Kavin'

import sys
import re


out = open("newout.fasta", "w")

with open(sys.argv[1], "rU") as fh:
    for line in fh:
        if line.startswith('>'):
            newline = re.search('OS=(.*)\s?\w*?=', line)
            #print newline.group(1)
            out.write('>'+line[4:10]+'|'+newline.group(1)+'\n')
        else:
            out.write(line)



