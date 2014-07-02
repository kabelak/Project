from __future__ import division
__author__ = 'Kavin'

import sys
import re
from Bio.Blast import NCBIXML


fname = re.search('(.*)\.(\w*)', sys.argv[1])
fname2 = str(fname.group(1))+'_processed.'+str(fname.group(2))
#out = open(fname2, "w")

with open(sys.argv[1], 'rU') as fh:
    blast_records = NCBIXML.parse(fh)
    for blast_record in blast_records:
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                #if hsp.expect < 0.04:
                print '****Alignment****'
                #print('sequence:', alignment.title)
                #print('length:', alignment.length)
                gbID = re.search('gi\|.*\|.*\|(.*)\|', alignment.hit_id)
                print 'Hit ID:', gbID.group(1)
                print 'Hit def:', alignment.hit_def
                print 'hit start:', hsp.sbjct_start
                print 'hit end:', hsp.sbjct_end
                print 'query start:', hsp.query_start
                print 'query end:', hsp.query_end
                print 'query strand:', hsp.frame[0]
                print 'hit strand:', hsp.frame[1]
                print 'e value:', float(hsp.expect)
                print 'identities:', hsp.identities
                print 'align length:', hsp.align_length
                print 'Identity:', int((hsp.identities/hsp.align_length)*100), '%'
                print hsp.query[:50] + '...'
                print hsp.match[:50] + '...'
                print hsp.sbjct[:50] + '...'












'''
   blast_record = next(blast_records)
'''
