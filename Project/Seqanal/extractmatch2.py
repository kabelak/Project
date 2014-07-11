__author__ = 'Kavin'

# #######################################################################################################
# Script to match entries within a Spire output and TSS/Startcodon entries within an Excel Spreadsheet #
# Usage:                                                                                               #
#   python extractmatch2.py [Spire Output File] [Excel Sheet]                                          #
# Output:                                                                                              #
#   Will display Rv number of match, RNA sequence of Spire match and start/end positions               #
########################################################################################################

import re
import sys
import xlrd
from Bio import SeqIO

#### Import data from Spire output file
# Create dicts to score Spire output data
spire_entry = {}
spire_entries = {}

# For each entry within Spire output (ie, each match), create a temp dict 'matches1' with all the charateristics, then
# create a glocal dict key for the entry with the characteristics as a value (ie, dict of dicts)
with open(sys.argv[1], 'rU') as f:
    for line in f:
        if line.startswith('Match'):
            line = re.sub('\n', '', line)
            entry = line
            line = next(f)
            while not line.startswith('None'):
                line = re.sub('\n|\t', '', line)
                characteristic = re.search('(.*):\s(.*)', line)
                spire_entry[characteristic.group(1)] = characteristic.group(2)
                line = next(f)
            if spire_entry['Direction'] == 'forward':
                spire_entry['Direction'] = '+'
            else:
                spire_entry['Direction'] = '-'
            spire_entries[entry] = spire_entry
            spire_entry = {}
'''
for key, value in matches.items():
    if value['Folds to'] == '     .(((((.....)))))':
        print key, '\n'
        print value['URL'], '\n'
'''
#### Import data from Excel workbook/sheet
workbook = xlrd.open_workbook("F:\Google Drive\Birkbeck\Project\RNAseq\Cortes sup mat\mmc3TSSvsStartCodon.xlsx")
# workbook = xlrd.open_workbook(sys.argv[2])
sheet = workbook.sheet_by_index(0)
data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

# Create dicts to store TSS data
TSS = {}
row = {}

# For each entry (row), store the startcodon and TSS as key/values within the value of a global dict
# with gene name as key
for i in range(2, sheet.nrows - 1):
    # print i
    while data[i][6] == '' and data[i][9] == '':
        i += 1
    Gene = data[i][0]
    row['Direction'] = str(data[i][3])
    # print Gene
    if data[i][5] < -0.7:
        row['StartCodon'] = int(data[i][4])
    else:
        row['StartCodon'] = int(data[i][2])
    if data[i][6] == '':
        # If empty, go to next iteration, ie internal TSS
        row['TSS'] = int(data[i][9])
    else:
        row['TSS'] = int(data[i][6])
    TSS[Gene] = row
    row = {}

'''
for key, value in TSS.items():
    print key, '\n'
    print value, '\n'

'''
#### Find intersection
# For each gene within the Excel sheet, iterate through entries within Spire output to find a match
# with SeqIO.parse(open("mtbtomod.gb", "r"), "genbank") as gbfile:

for UTR, area in TSS.items():
    for key, value in spire_entries.items():
        position = re.search('\((\d*):(\d*)', key)
        gene = re.search('term=(\w*)', value['URL'])
        if UTR == gene.group(1):
            if value['Direction'] != area['Direction']:
                print 'There is a problem in the strand direction matches...', value['Direction'], ' and ', area[
                    'Direction']
            else:
                if value['Direction'] == '+':
                    if area['TSS'] <= position.group(1) and int(area['StartCodon']) >= int(position.group(2)):
                        print UTR, gene.group(1)
                        print value['Sequence'], ' is contained within the UTR on the ', value['Direction']
                if value['Direction'] == '-':
                    if int(area['TSS']) >= int(position.group(2)) and int(area['StartCodon']) <= int(position.group(1)):
                        print UTR, gene.group(1)
                        print value['Sequence'], ' is contained within the UTR on the ', value['Direction']


'''
                #print 'Eureka! Rv number matches found!'
                print UTR, gene.group(1)
                print value['Sequence'], 'starts at ', position.group(1), ' and ends at ', position.group(2), ' on strand ', area['Direction']
                print "Untrans Region starts at", area['TSS'], 'and ends at', area['StartCodon'], ' on strand ', area['Direction']

            #print key, value['Direction']



for key, value in matches.items():
    position = re.search('\((\d*):(\d*)', key)
    gene = re.search('term=(\w*)', value['URL'])
    print value['Sequence'], 'starts at ', position.group(1), ' and ends at ', position.group(2)
    print 'This is part of gene ', gene.group(1), 'which is part of feature ', value['Feature']

#sheet.nrows

#with open(sys.argv[2], 'rU') as f2:
# open excel file - requires either csv.read or excel package <- latter may be best for future use
# read in TSS and start codon for each gene
# case: what about matches where there are sequences upstream and downstream? -- duplicate entry up to certain point, then replace dict values
# rule 1: matches between TSS and start codon - read from other file
# rule 2: remove ones which do not fold nicely
'''