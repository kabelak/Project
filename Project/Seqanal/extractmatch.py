__author__ = 'Kavin'

import re
import sys

f = open(sys.argv[1], 'rU')

matches = []

# f.readline() until f.readline().startswith('Match')

for line in f:
    if line.startswith('Match'):
        matches.append(line)

print matches


file = open('FilePath/OUTPUT.01')
lines = file.read()
file.close()
with open("output.txt","w") as f:
    for match in re.finditer(r"(?m)^\s*-+\s+\S+\s+(-?[\d.]+E[+-]\d+)", lines):
        f.write(match.group(1)+"\n")
