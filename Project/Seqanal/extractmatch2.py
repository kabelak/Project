__author__ = 'Kavin'

import re
import sys
import xlrd


## Import data from Spire output file

matches1 = {}
matches = {}
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


## Import data from Excel workbook/sheet
workbook = xlrd.open_workbook("F:\Google Drive\Birkbeck\Project\RNAseq\Cortes sup mat\mmc3TSSvsStartCodon.xlsx")
sheet = workbook.sheet_by_index(0)
data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

TSS = {}
row = {}
for i in range(2, 15): #sheet.nrows
    # print i
    Gene = data[i][0]
    # print Gene
    row['StartCodon'] = data[i][4]
    if data[i][6] == '':
        # if empty as well, go to next iteration
        row['TSS'] = data[i][9]
    else:
        row['TSS'] = data[i][6]
    TSS[Gene] = row
    row = {}

#print TSS

for UTR, area in TSS.items():
    for key, value in matches.items():
        position = re.search('\((\d*):(\d*)', key)
        gene = re.search('term=(\w*)', value['URL'])
        if UTR == gene.group(1):
            print 'Eureka!'
            print UTR, gene.group(1)
            print value['Sequence'], 'starts at ', position.group(1), ' and ends at ', position.group(2)
            print "Untrans Region starts at", area['TSS'], 'and ends at', area['StartCodon']







    #print key, value['Direction']

'''
for key, value in TSS.items():
    if key == 'Rv0005':
        print 'well done!', key, value

for key, value in matches.items():
    position = re.search('\((\d*):(\d*)', key)
    gene = re.search('term=(\w*)', value['URL'])
    print value['Sequence'], 'starts at ', position.group(1), ' and ends at ', position.group(2)
    print 'This is part of gene ', gene.group(1), 'which is part of feature ', value['Feature']

#with open(sys.argv[2], 'rU') as f2:
# open excel file - requires either csv.read or excel package <- latter may be best for future use
# read in TSS and start codon for each gene
# case: what about matches where there are sequences upstream and downstream? -- duplicate entry up to certain point, then replace dict values
# rule 1: matches between TSS and start codon - read from other file
# rule 2: remove ones which do not fold nicely
'''