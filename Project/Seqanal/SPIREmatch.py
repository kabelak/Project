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

for i in range(5, len(datagrow)):  # replace 20 with len(datagrow)
    if datagrow[i][1] == 'F':
        fgrow.append(int(datagrow[i][0]))
    elif datagrow[i][1] == 'R':
        rgrow.append(int(datagrow[i][0]))

for i in range(5, len(dataarrest)):  # replace 20 with len(dataarrest)
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

possiblestarts = defaultdict(list)

for key, value in spire_entries.items():
    matchat = re.search('\((\d*):(\d*)', key)
    matchstart = matchat.group(1)
    matchend = matchat.group(2)
    gene = re.search('term=(\w*)', value['URL']).group(1)
    geneloc = re.search('(\d*)\.\.(\d*)', value['Position'])
    genestart = int(geneloc.group(1))
    geneend = int(geneloc.group(2))

    if value['Direction'] == '+':
        for TSS in fgrow:
            if genestart - 200 <= TSS <= genestart:
                possiblestarts[gene].append(TSS)

print possiblestarts["Rv1073"]