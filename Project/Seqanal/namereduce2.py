__author__ = 'Kavin'

import sys
import re


fname = re.search('(.*)\.(\w*)', sys.argv[1])
fname2 = str(fname.group(1)) + '_reduced.' + str(fname.group(2))
out = open(fname2, "w")

with open(sys.argv[1], "rU") as fh:
    for line in fh:
        if line.startswith('>'):
            name = re.search('\|(\w*_\w*)', line)

            out.write(re.sub('_', ' ', name.group(1)) + ', ')

out.close()