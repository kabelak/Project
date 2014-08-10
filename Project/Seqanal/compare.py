__author__ = 'Kavin'

import sys
from collections import defaultdict

SP = open("SP.txt", 'r').readlines()
SP2 = open("SP2.txt", 'r').readlines()

dict = defaultdict(list)

for line in SP:
    for line2 in SP2:
        if line == line2:
            dict[line].append(line2)

for key in dict:
    print key
