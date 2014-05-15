__author__ = 'Kavin'

import re
import sys

f = open(sys.argv[1], 'rU')

matches1 = [] # make this a dict {}
matches = {}

# f.readline() until f.readline().startswith('Match')

for line in f:
    if line.startswith('Match'):
        line = re.sub('\n', '', line)
        entry = line
        line = next(f)
        while not line.startswith('None'):
            line = re.sub('\n|\t', '', line)
            # Re match before : match after
            # matches1[group1] = group 2
            matches1.append(line) ## delete this
            line = next(f)
        matches[entry] = matches1
        matches1= []

print matches

# case: what about matches where there are sequences upstream and downstream? -- duplicate entry up to certain point, then replace dict values
# rule 1: matches between TSS and start codon - read from other file
# rule 2: remove ones which do not fold nicely
