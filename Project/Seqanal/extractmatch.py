__author__ = 'Kavin'

# #######################################################################################################
# Script to match entries within a Spire output and TSS/Startcodon entries within an Excel Spreadsheet #
# Usage:                                                                                               #
# python extractmatch.py [Spire Output File] [Excel Sheet]                                          #
# Output:                                                                                              #
#   Will display Rv number of match, RNA sequence of Spire match and start/end positions               #
########################################################################################################

import xlrd
import sys
import re
from Bio import SeqIO

#### Import data from Spire output file
# Create dicts to score Spire output data


# For each entry within Spire output (ie, each match), create a temp dict 'matches1' with all the charateristics, then
# create a glocal dict key for the entry with the characteristics as a value (ie, dict of dicts)

def spireextract(
        spirefile):  # TODO: Feature, Distance, Position and URL are repeated if there are both up/dowstream matches for a SPIRE entry - resolve! (duplicate the previous data, and add the new entry)
    import re  # TODO: if you're gona fix this, might as well fix the data structure so as to get the gene names etc

    _spire_entry = {}
    _spire_entries = {}
    with open(spirefile, 'rU') as _f:
        for _line in _f:
            if _line.startswith('Match'):
                _line = re.sub('\n', '', _line)
                entry = _line
                _line = next(_f)
                while not _line.startswith('None'):
                    while not _line.startswith('\tAlignments'):
                        _line = re.sub('\n|\t', '', _line)
                        characteristic = re.search('(\w*):\s(.*)', _line)
                        _spire_entry[characteristic.group(1)] = characteristic.group(2)
                        _line = next(_f)
                    _line = next(_f)
                    if _line.startswith('None'):
                        break
                    else:
                        _spire_entry2 = _spire_entry.copy()
                        while not _line.startswith('\tAlignments'):
                            _line = re.sub('\n|\t', '', _line)
                            characteristic = re.search('(.*):\s(.*)', _line)
                            _spire_entry2[characteristic.group(1)] = characteristic.group(2)
                            _line = next(_f)
                        entry2 = str(entry + '2')
                        if _spire_entry2['Direction'] == 'forward':
                            _spire_entry2['Direction'] = '+'
                        else:
                            _spire_entry2['Direction'] = '-'
                        _spire_entries[entry2] = _spire_entry2
                if _spire_entry['Direction'] == 'forward':
                    _spire_entry['Direction'] = '+'
                else:
                    _spire_entry['Direction'] = '-'
                _spire_entries[entry] = _spire_entry
                _spire_entry = {}
    return _spire_entries


spire_entries = spireextract(sys.argv[1])

'''
for key, value in spire_entries.items():
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

matches = {}

for UTR, area in TSS.items():
    for key, value in spire_entries.items():
        position = re.search('\((\d*):(\d*)', key)
        gene = re.search('term=(\w*)', value['URL'])
        if UTR == gene.group(1):
            if value['Direction'] != area['Direction']:
                print 'There is a problem in the strand direction matches...', value['Direction'], ' and ', area[
                    'Direction']
            else:
                if value[
                    'Direction'] == '+':  # TODO: forward does not mean the match is upstream - NEED TO FIX! Look at Feature: upstream/downstream
                    if int(area['TSS']) <= int(position.group(1)) and int(area['StartCodon']) >= int(position.group(2)):
                        matches[UTR] = {'UTRStart': int(area['TSS']), 'UTRStop': int(area['StartCodon']),
                                        'IREStart': int(position.group(1)), 'IREStop': int(position.group(2)),
                                        'Direction': value['Direction'], 'Spireseq': str(value['Sequence'])}
                if value['Direction'] == '-':
                    if int(area['TSS']) >= int(position.group(2)) and int(area['StartCodon']) <= int(position.group(1)):
                        matches[UTR] = {'UTRStart': int(area['StartCodon']), 'UTRStop': int(area['TSS']),
                                        'IREStart': int(position.group(2)), 'IREStop': int(position.group(1)),
                                        'Direction': value['Direction'], 'Spireseq': str(value['Sequence'])}

### Extract the sequences from the GenBank file
gb_file = SeqIO.parse(open("mtbtomod.gb", "r"), "genbank")
for record in gb_file:
    for key, value in matches.items():
        if value['Direction'] == '+':
            value['Sequence'] = record.seq[value['IREStart'] - 10:value['IREStop'] + 10]
            # print key, value['Sequence']
        if value['Direction'] == '-':
            ire_sequence = record.seq[value['IREStop'] - 10:value['IREStart'] + 10]
            value[
                'Sequence'] = ire_sequence.reverse_complement()  # Extracts the reverse complement (ie, 3'->5' read, opposite strand)
            # print 'minus', key, value['Sequence']

fname = re.search('(.*)\.(\w*)', sys.argv[1])
fname2 = str(fname.group(1)) + '_seqExtract52.' + str(fname.group(2))
with open(fname2, "w") as out:
    for key, value in matches.items():
        out.write('>' + str(key) + '\n' + str(value['Sequence']) + '\n\n')

# out.write('>' + str(key) + value['Direction'] + '\n' + str(value['Sequence']) + '\n     ' + value['Spireseq'] + '\n\n')

'''
# read in TSS and start codon for each gene
# case: what about matches where there are sequences upstream and downstream? -- duplicate entry up to certain point, then replace dict values
# rule 1: matches between TSS and start codon - read from other file
# rule 2: remove ones which do not fold nicely
'''