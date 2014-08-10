__author__ = 'Kavin'

import sys
import numpy
from Bio import SeqIO
import collections
import indexed
from test import spireextract
import re


def GENBANKparse(gbfile):
    import indexed

    _genes = indexed.IndexedOrderedDict()
    _gene = {}
    for record in SeqIO.parse(open(gbfile, "r+"), "genbank"):
        for feature in record.features:
            if feature.type == "CDS":
                if "locus_tag" in feature.qualifiers:
                    genename = feature.qualifiers["locus_tag"][0]
                    _gene['Start'] = feature.location.start.position
                    _gene['End'] = feature.location.end.position
                    _gene['Strand'] = feature.location.strand
                    _genes[str(genename)] = _gene
                    _gene = {}

    return _genes


genes = GENBANKparse("M.tb H37Rv BCT 2013-Jun-13.gb")

print 'Number of successful matches: %i ' % len(genes)

print genes['Rv1752']
position = genes.keys().index('Rv1752')
print position

print genes.values()[position + 1]
