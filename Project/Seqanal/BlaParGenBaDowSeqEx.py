from __future__ import division
__author__ = 'Kavin'

import sys
import re
import time
from Bio.Blast import NCBIXML
from Bio import Entrez
from Bio import SeqIO


def GenBankDownload(organism_id):
    #from Bio import Entrez
    Entrez.email = 'kabela01@mail.bbk.ac.uk'
    handle = Entrez.efetch(db='nucleotide',id=organism_id,rettype='gb')
    local_file = open(str(organism_id+'.gb'), 'w')
    local_file.write(handle.read())
    handle.close()
    local_file.close()
    time.sleep(2) #important to prevent DDoS type control from NCBI

def GenBankParser(gbFile,start):
    #from Bio import SeqIO
    gb_record = SeqIO.parse(open(gbFile, "r"), "genbank")
    for record in gb_record:
        for feature in record.features:
            if start in feature:
                print(feature.qualifiers.get('product'))

with open(sys.argv[1], 'rU') as fh:
    blast_records = NCBIXML.parse(fh)
    for blast_record in blast_records:
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if int((hsp.identities/hsp.align_length)*100) > 81:
                    #if hsp.expect < 0.04:
                    print '****Alignment****'
                    #print('sequence:', alignment.title)
                    #print('length:', alignment.length)
                    gbID = re.search('gi\|.*\|.*\|(.*)\|', alignment.hit_id)
                    print 'Hit ID:', gbID.group(1)
                    print 'Hit def:', alignment.hit_def
                    print 'hit start:', hsp.sbjct_start
                    '''
                    print 'hit end:', hsp.sbjct_end
                    print 'query start:', hsp.query_start
                    print 'query end:', hsp.query_end
                    print 'query strand:', hsp.frame[0]
                    '''
                    print 'hit strand:', hsp.frame[1]
                    print 'e value:', float(hsp.expect)
                    '''
                    print 'identities:', hsp.identities
                    print 'align length:', hsp.align_length
                    '''
                    print 'Identity:', int((hsp.identities/hsp.align_length)*100), '%'
                    print hsp.query[:50] + '...'
                    print hsp.match[:50] + '...'
                    print hsp.sbjct[:50] + '...'
                    #GenBankDownload(gbID.group(1))
                    GenBankParser(str(gbID.group(1)+'.gb'), hsp.sbjct_start)










fname = re.search('(.*)\.(\w*)', sys.argv[1])
fname2 = str(fname.group(1))+'_processed.'+str(fname.group(2))
#out = open(fname2, "w")