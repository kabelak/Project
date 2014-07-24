__author__ = 'Kavin'

import sys
import xlrd
import re
from SPIREmatch import GENBANKparse
from extractmatch import spireextract
from collections import defaultdict
from Bio import SeqIO


def iterategene(genename, decrement=True):
    id = int(re.search('(\d{4})', genename).group(1))
    if decrement:
        id = str(id - 1)
    else:
        id = str(id + 1)
    if 'c' in genename:
        newname = str('Rv' + id.zfill(4) + 'c')  # what about A, B etc????
    else:
        newname = str('Rv' + id.zfill(4))

    return newname

### Function to extract data from an excel worksheet
def exceldata(excelfile, sheet):
    workbook = xlrd.open_workbook(excelfile)
    worksheet = workbook.sheet_by_index(sheet)
    data = [[worksheet.cell_value(r, c) for c in range(0, 2)] for r in range(worksheet.nrows)]
    return data

def extractTSS(excellist):
    forward = [];
    reverse = []
    for i in range(5, len(excellist)):
        if excellist[i][1] == 'F':
            forward.append(int(excellist[i][0]))
        elif datagrow[i][1] == 'R':
            reverse.append(int(excellist[i][0]))

    return forward, reverse

growthfile = "F:\Google Drive\Birkbeck\Project\RNAseq\Cortes sup mat\mmc2expogrowth.xlsx"
arrestfile = "F:\Google Drive\Birkbeck\Project\RNAseq\Cortes sup mat\mmc6arrest.xlsx"
datagrow = exceldata(growthfile, 5)
dataarrest = exceldata(arrestfile, 4)
fgrow, rgrow = extractTSS(datagrow)
farrest, rarrest = extractTSS(dataarrest)

spire_entries = spireextract("mtb.txt")
codingregions = GENBANKparse("M.tb H37Rv BCT 2013-Jun-13.gb")

possiblestartsgrow = defaultdict(list)
possiblestartsarrest = defaultdict(list)
spread = 200
for key, value in spire_entries.items():
    # # Extract information from a SPIRE match
    matchat = re.search('\((\d*):(\d*)', key)
    matchstart = matchat.group(1)
    matchend = matchat.group(2)
    matchloc = re.search('(\w*)\sof.*', value['Feature']).group(1)
    spire_entries[key]['Match Location'] = str(matchloc)
    gene = re.search('term=(\w*)', value['URL']).group(1)
    spire_entries[key]['Gene'] = str(gene)

    # # Extract gene start/end information from GB file
    codingstart = codingregions[gene]['Start']
    codingend = codingregions[gene]['End']

    # # Look at SPIRE matches and figure out if there is a TSS within 'spread' nucleotides of the codingstart
    # TODO: a better way would be to look at the end of coding (stop codon) of the previous gene, instead of using 'spread'
    checkgene = gene
    if matchloc == 'upstream':
        if value['Direction'] == '+':  # Just do -1 to codingregions
            if not codingregions.has_key(iterategene(checkgene)):
                while not codingregions.has_key(iterategene(checkgene)):
                    checkgene = iterategene(checkgene)

            for TSS in fgrow:
                if codingregions[iterategene(checkgene)]['End'] <= TSS <= codingstart:
                    possiblestartsgrow[gene].append(TSS)
            #print gene, checkgene

            for TSS in farrest:
                if codingregions[iterategene(checkgene)]['End'] <= TSS <= codingstart:
                    possiblestartsarrest[gene].append(TSS)
"""
        if value[
            'Direction'] == '-':  # Need to figure out how to work with the 'c' in Rv number; for upstream, need to look at a larger c number, +1
            for TSS in fgrow:
                if codingend <= TSS <= codingend + spread:
                    possiblestartsgrow[gene].append(TSS)
            for TSS in farrest:
                if codingend <= TSS <= codingend + spread:
                    possiblestartsarrest[gene].append(TSS)

    # if matchloc == 'downstream':
    #    print 'downstream'
    #    if value['Direction'] == '+':
    #        for TSS in fgrow:

        # TODO: look between coding sequence stop position and stop position of IRE (+10 bases?) and find out if there are any TSS between them. If there are, then mark as unlikely to be part of the same transcript as the gene, and thus it is a dubious match.
"""

for key, value in spire_entries.items():
    if possiblestartsgrow.has_key(value['Gene']):
        spire_entries[key]['Growth TSSs'] = possiblestartsgrow[value['Gene']]
    elif possiblestartsarrest.has_key(value['Gene']):
        spire_entries[key]['Arrest TSSs'] = possiblestartsarrest[value['Gene']]
    else:
        del spire_entries[key]
    if spire_entries.has_key(key):
        print spire_entries[key]['Gene']

'''
    if matchloc == 'downstream':
        if value['Direction'] == '+':
            for TSS in fgrow, farrest:
                if codingstart - 200 <= TSS <= codingstart:
                    #and there are no TSS between the end of the gene and the start of the next IRE match, as well as no Start Codons
                    possiblestartsgrow[gene].append(TSS)
        if value['Direction'] == '-':
            for TSS in fgrow, farrest:
                if codingend <= TSS <= codingend + 200:
                    possiblestartsgrow[gene].append(TSS)





    if value['Direction'] == '-':
        TSSlistgrow = rgrow
        TSSlistarrest = rarrest
    else:
        TSSlistgrow = fgrow
        TSSlistarrest = farrest

    if value['Direction'] == '+':
        for TSS in fgrow:
            if codingstart - 200 <= TSS <= codingstart:
                possiblestartsgrow[gene].append(TSS)

print possiblestartsgrow
'''

