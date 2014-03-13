__author__ = 'Kavin'

import re
import sys

input_file = open(sys.argv[1], 'rU')

##sequences = []
count = 0
line = input_file.read()
searchseq = re.findall(r'Loop region: (\w*).*Sequence: (\w*)', line, re.DOTALL)


for elements in searchseq:
    print elements

##print sequences

## input_file.readlines()
## input_file.read()
