__author__ = 'Kavin'


import re
import sys

fname = re.search('(.*)\.(\w*)', sys.argv[1])
fname2 = str(fname.group(1))+'_list.'+str(fname.group(2))
outp = open(fname2, "w")

with open(sys.argv[1], "rU") as f:
    for line in f:
        if line.startswith('>'):
            fields = re.search(">(\w*)\|(.*)/", line)
            outp.write(fields.group(1)+'\t'+fields.group(2)+'\n')

outp.close()