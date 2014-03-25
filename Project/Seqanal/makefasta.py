__author__ = 'Kavin'

import re
import sys

input_file = open(sys.argv[1], 'rU')

##sequences = []
file = input_file.read()
spacesfile = re.sub(r'>', '\n>', file)

print spacesfile