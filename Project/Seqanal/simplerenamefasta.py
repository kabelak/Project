__author__ = 'Kavin'

import sys
import re



fname = re.search('(.*)\.(\w*)', sys.argv[1])
fname2 = str(fname.group(1))+'_processed.'+str(fname.group(2))
out = open(fname2, "w")

with open(sys.argv[1], "rU") as fh:
    for line in fh:
        if line.startswith('>'):
            newline = re.search('OS=(.*)\s?\w*?=', line)
            #print newline.group(1)
            out.write('>'+line[4:10]+'|'+re.sub(' ', '_', newline.group(1))+'\n')
        else:
            out.write(line)

out.close()
