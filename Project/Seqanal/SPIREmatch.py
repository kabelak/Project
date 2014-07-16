__author__ = 'Kavin'

import sys
import xlrd
import re
from test import spireextract
# from extractmatch import spireextract
from collections import defaultdict

### Function to extract data from an excel worksheet
def exceldata(excelfile, sheet):
    workbook = xlrd.open_workbook(excelfile)
    worksheet = workbook.sheet_by_index(sheet)
    data = [[worksheet.cell_value(r, c) for c in range(0, 2)] for r in range(worksheet.nrows)]
    return data

#print sheetgrow.ncols
#print sheetgrow.nrows

growthfile = "F:\Google Drive\Birkbeck\Project\RNAseq\Cortes sup mat\mmc2expogrowth.xlsx"
arrestfile = "F:\Google Drive\Birkbeck\Project\RNAseq\Cortes sup mat\mmc6arrest.xlsx"

datagrow = exceldata(growthfile, 5)
dataarrest = exceldata(arrestfile, 4)

fgrow = []
rgrow = []
farrest = []
rarrest = []

for i in range(5, len(datagrow)):
    if datagrow[i][1] == 'F':
        fgrow.append(int(datagrow[i][0]))
    elif datagrow[i][1] == 'R':
        rgrow.append(int(datagrow[i][0]))

for i in range(5, len(dataarrest)):
    if dataarrest[i][1] == 'F':
        farrest.append(int(dataarrest[i][0]))
    elif dataarrest[i][1] == 'R':
        rarrest.append(int(dataarrest[i][0]))
'''
print fgrow
print rgrow
print farrest
print rarrest
'''

spire_entries = spireextract("mtb.txt")

possiblestartsgrow = defaultdict(list)
possiblestartsarrest = defaultdict(list)
spread = 200


for key, value in spire_entries.items():
    matchat = re.search('\((\d*):(\d*)', key)
    matchstart = matchat.group(1)
    matchend = matchat.group(2)
    matchloc = re.search('(\w*)\sof.*', value['Feature']).group(1)
    gene = re.search('term=(\w*)', value['URL']).group(1)
    geneloc = re.search('(\d*)\.\.(\d*)', value['Position'])
    genestart = int(geneloc.group(1))
    geneend = int(geneloc.group(2))

    if matchloc == 'upstream':
        if value['Direction'] == '+':
            for TSS in fgrow:
                if genestart - spread <= TSS <= genestart:
                    possiblestartsgrow[gene].append(TSS)
            for TSS in farrest:
                if genestart - spread <= TSS <= genestart:
                    possiblestartsarrest[gene].append(TSS)

        if value['Direction'] == '-':
            for TSS in fgrow:
                if geneend <= TSS <= geneend + spread:
                    possiblestartsgrow[gene].append(TSS)
            for TSS in farrest:
                if geneend <= TSS <= geneend + spread:
                    possiblestartsarrest[gene].append(TSS)

for kg, vg in sorted(possiblestartsgrow.items()):
    if possiblestartsarrest.has_key(kg):
        print kg, ' has start sites:', vg, ' during growth and ', possiblestartsarrest[kg], ' during arrest'

# print possiblestartsarrest
#print '\n\n'
#print possiblestartsgrow

'''
    if matchloc == 'downstream':
        if value['Direction'] == '+':
            for TSS in fgrow, farrest:
                if genestart - 200 <= TSS <= genestart:
                    #and there are no TSS between the end of the gene and the start of the next IRE match, as well as no Start Codons
                    possiblestartsgrow[gene].append(TSS)
        if value['Direction'] == '-':
            for TSS in fgrow, farrest:
                if geneend <= TSS <= geneend + 200:
                    possiblestartsgrow[gene].append(TSS)





    if value['Direction'] == '-':
        TSSlistgrow = rgrow
        TSSlistarrest = rarrest
    else:
        TSSlistgrow = fgrow
        TSSlistarrest = farrest

    if value['Direction'] == '+':
        for TSS in fgrow:
            if genestart - 200 <= TSS <= genestart:
                possiblestartsgrow[gene].append(TSS)

print possiblestartsgrow
'''

