__author__ = 'Kavin'

import os

output = open("merge.txt", "w")

filenames = os.listdir('.')
for f in filenames:
    if f != "merge.txt" and f != "mergetextfiles.py":
        with open(f, 'r') as content_file:
            content = content_file.read()
            output.write(content + '\n')

output.close()