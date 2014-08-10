__author__ = 'Kavin'

import sys


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