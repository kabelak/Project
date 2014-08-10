__author__ = 'Kavin'

import sys
import re

genes = ['Rv0001', 'Rv0002c']


def iterategene(genename, upstream=True):
    id = int(re.search('(\d{4})', genename).group(1))
    if upstream:
        id = str(id - 1)
    else:
        id = str(id + 1)
    if 'c' in genename:
        newname = str('Rv' + id.zfill(4) + 'c')
    else:
        newname = str('Rv' + id.zfill(4))

    return newname


for gene in genes:
    print gene
    print iterategene(gene)
