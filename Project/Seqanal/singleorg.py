__author__ = 'Kavin'

import sys
import re

fh = open(sys.argv[1], 'rU')
lines = fh.readlines()
size = len(lines)
orgs = {}

print size

outp =open("outputfile.txt", "w")
for i in range(0, size):
    if lines[i].startswith('>'):
        entry = re.search('OS=(\w*\s\w*\.?)\s', lines[i])
        org = entry.group(1)
        print org
        if not orgs.has_key(org):
            print org+' inside'
            orgs[org] = '1'
            outp.write(lines[i])
            i = i+1
            while not lines[i].startswith('>'):
                outp.write(lines[i])
                i = i+1
                if i >= size:
                    break
            outp.write('\n')
            i = i-1


        else:
            while not lines[i].startswith('>'):
                i = i+1
                if i >= size:
                    break
            i = i-1



for (key, value) in orgs.items():
    print key
    print value



'''



for line in fh:
    if line.startswith('>'):
        entry = re.search('OS=(.*)\sGN', line)
        org = entry.group(1)



'''
'''








for (firstline, sequence) in re.findall('(>.*)\n(.*)>', fh.read(), re.DOTALL):
    print firstline
    print 'blablabla'
    print sequence
'''

