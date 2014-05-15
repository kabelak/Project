__author__ = 'Kavin'

import re
import sys

f = open(sys.argv[1], 'rU')

matches1 = []
matches = ()

# f.readline() until f.readline().startswith('Match')

for line in f:
    if line.startswith('Match'):
        matches1.append(line)
        line = next(f)
        while not line.startswith('Match'):
            matches1.append(line)
            line = next(f)
        matches = matches + (matches1,)
        matches1= []

print matches



