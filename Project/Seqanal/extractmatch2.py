__author__ = 'Kavin'

import re
import sys



matches1 = {} # make this a dict {}
matches = {}

# f.readline() until f.readline().startswith('Match')

with open(sys.argv[1], 'rU') as f:
  for line in f:
    if line.startswith('Match'):
        line = re.sub('\n', '', line)
        entry = line
        line = next(f)
        while not line.startswith('None'):
            line = re.sub('\n|\t', '', line)
            characteristic = re.search('(.*):\s(.*)', line)
            # Re match before : match after
            # matches1[group1] = group 2
            #matches1.append(line) ## delete this
            matches1[characteristic.group(1)] = characteristic.group(2)
            line = next(f)
        matches[entry] = matches1
        matches1= {}

#with open(sys.argv[2], 'rU') as f2:
# open excel file - requires either csv.read or excel package <- latter may be best for future use
# read in TSS and start codon for each gene
# compare the IRE found for any gene with position of IRE wrt to TSS and start codon



for key, value in matches.items():
    position = re.search('\((\d*):(\d*)', key)
    gene = re.search('term=(\w*)', value['URL'])
    print value['Sequence'], 'starts at ', position.group(1), ' and ends at ', position.group(2)
    print 'This is part of gene ', gene.group(1), 'which is part of feature ', value['Feature']

    #print key, value['Direction']



# case: what about matches where there are sequences upstream and downstream? -- duplicate entry up to certain point, then replace dict values
# rule 1: matches between TSS and start codon - read from other file
# rule 2: remove ones which do not fold nicely
