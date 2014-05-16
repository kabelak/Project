__author__ = 'Kavin'

import xlrd

workbook = xlrd.open_workbook("F:\Google Drive\Birkbeck\Project\RNAseq\Cortes sup mat\mmc3TSSvsStartCodon.xlsx")
sheet = workbook.sheet_by_index(0)

print sheet.nrows

data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

TSS = {}
row = {}

for i in range(2, 15): #sheet.nrows
    print i
    Gene = data[i][0]
    print Gene
    row['StartCodon'] = data[i][4]
    if data[i][6] == '':
        row['TSS'] = data[i][9]
    else:
        row['TSS'] = data[i][6]

    TSS[Gene] = row
    row = {}

#print TSS

for key, value in TSS.items():
    if key == 'Rv0005':
        print 'well done!', key, value








'''
    if data[i][6] == '':
        print i, 'there is no data in TSS'
    else:
        print i, data[i][0], data[i][4], data[i][6]
'''