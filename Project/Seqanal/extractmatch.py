__author__ = 'Kavin'

import sys

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
        matches1= []
    break
  last_pos = fp.tell()
  line = fp.readline()
