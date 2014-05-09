__author__ = 'Kavin'


import os
import re

filenames = os.listdir('.')
for f in filenames:
        with open(f, 'r') as content_file:
            content = content_file.read()
            print content
            print '\n'







#from os import listdir
#from os.path import isfile, join
#onlyfiles = [ f for f in listdir('.') if isfile(join(mypath,f)) ]

#files = [f for f in os.listdir('.') if os.path.isfile(f)]