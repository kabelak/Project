__author__ = 'Kavin'

import re
import sys

f = open(sys.argv[1], 'rU')

matches1 = []
matches = ()

# f.readline() until f.readline().startswith('Match')

for line in f:
    if line.startswith('Match'):
        line = re.sub('\n', '', line)
        matches1.append(line)
        line = next(f)
        while not line.startswith('None'):
            line = re.sub('\n|\t', '', line)
            matches1.append(line)
            line = next(f)
        matches = matches + (matches1,)
        matches1= []

print matches

matches1 = []
matches = ()

fp = open(sys.argv[1], 'rU')
last_pos = fp.tell()
line = fp.readline()
while line != '':
    if line.startswith('Match'):
        matches1.append(line)
        line = next(f)
        while not line.startswith('Match'):
            matches1.append(line)
            line = next(f)
        matches = matches + (matches1,)
        matches1 = []
    break
last_pos = fp.tell()
line = fp.readline()  # rule 1: matches between TSS and start codon - read from other file
# rule 2: remove ones which do not fold nicely
