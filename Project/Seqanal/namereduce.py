__author__ = 'Kavin'

import sys
import re


fname = re.search('(.*)\.(\w*)', sys.argv[1])
fname2 = str(fname.group(1)) + '_processed.' + str(fname.group(2))
out = open(fname2, "w")

with open(sys.argv[1], "rU") as fh:
    for line in fh:
        if line.startswith('>'):
            out.write(re.sub('\s|\(|\)|\[|\]', '_', line[:89]) + '\n')
        else:
            out.write(line[:29] + '\n')

out.close()