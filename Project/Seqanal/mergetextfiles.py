__author__ = 'Kavin'


import os
import re

output = open("merge.txt", "w")

filenames = os.listdir('.')
for f in filenames:
    if f != "merge.txt" and f != "mergetextfiles.py":
        with open(f, 'r') as content_file:
            content = content_file.read()
            output.write(content + '\n')



output.close()




#from os import listdir
#from os.path import isfile, join
#onlyfiles = [ f for f in listdir('.') if isfile(join(mypath,f)) ]

#files = [f for f in os.listdir('.') if os.path.isfile(f)]