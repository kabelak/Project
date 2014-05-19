__author__ = 'Kavin'


import re
import sys

with open(sys.argv[1], "rU") as f:
    for line in f:
        if line.startswith('>'):
            print "\n"
            org = re.search("gi\|(\d*)\|.*?\[(.*)\]", line)
            #print org.group(1), org.group(2), org.group(3)
            #if org.group(3):
            #print ">",org.group(2),"_",org.group(3),org.group(1)
            print ">"+re.sub('\s', '_', org.group(2))+"||"+org.group(1)
            #else:
            #    print ">", org.group(2), org.group(1)
        else:
            line = re.sub('\n', '', line)
            print line


