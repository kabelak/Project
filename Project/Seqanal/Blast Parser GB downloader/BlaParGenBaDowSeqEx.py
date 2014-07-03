from __future__ import division
__author__ = 'Kavin'

import sys
import re
import time
import os
from Bio.Blast import NCBIXML
from Bio import Entrez
from Bio import SeqIO


forward_IRE = {}
reverse_IRE = {}


def GenBankDownload(organism_id):
    #from Bio import Entrez
    print "Downloading GenBank file for", organism_id
    Entrez.email = 'kabela01@mail.bbk.ac.uk'
    handle = Entrez.efetch(db='nucleotide',id=organism_id,rettype='gb')
    local_file = open(str(organism_id+'.gb'), 'w')
    local_file.write(handle.read())
    handle.close()
    local_file.close()
    print "Download completed"
    time.sleep(2) #important to prevent DDoS type control from NCBI

def GenBankParser(gbFile, start, frame, IRE=200):
    #from Bio import SeqIO
    if 'product' in locals():
        print product
    gb_record = SeqIO.parse(open(gbFile, "r"), "genbank")
    for record in gb_record:
        for feature in record.features:
            if start in feature:
                if feature.type == 'CDS':
                    if 'product' in feature.qualifiers:
                        #print 'Product:', feature.qualifiers['product'][0]
                        product = feature.qualifiers['product'][0]
                        print product
                        #print("%s %s" % (feature.type, feature.qualifiers.get('product')))
                    location = feature.location
                    # TODO how to make sure it is checking in the right strand? At the moment, the 'start in feature' seems to find... but how?
                    if frame != location.strand:
                        print '!!!!!Strands do not match! The GBrecord strand is', location.strand, 'while the BLAST strand is', frame, '!!!!!!!!'
                    if location.strand == 1:
                        ire_start = location.start.position-IRE
                        ire_end = location.start.position
                        #print ire_start
                        #print ire_end
                        #print 'Upstream Region:', record.seq[ire_start:ire_end]
                        ire_sequence = record.seq[ire_start:ire_end]
                        #forward_IRE[feature.qualifiers['product'][0]] = record.seq[ire_start:ire_end]
                        #coding_start = location.start.position
                        #coding_end = location.end.position
                    else:
                        ire_start = location.end.position+IRE
                        ire_end = location.end.position
                        #print ire_start
                        #print ire_end
                        #print 'Reverse Strand; Upstream Region:', record.seq[ire_end:ire_start]
                        ire_sequence = record.seq[ire_end:ire_start]
                        #reverse_IRE[feature.qualifiers['product'][0]] = record.seq[ire_end:ire_start]
                        #coding_start = location.end.position
                        #coding_end = location.start.position
                    #print location.strand, coding_start, coding_end
                    #print record.seq[coding_start:coding_end]
    if 'product' in locals():
        return (product, location.strand, ire_sequence)
    else:
        return ('NA', '0', 'NA')

fname = re.search('(.*)\.(\w*)', sys.argv[1])
fname2 = str(fname.group(1))+'_processed.txt'
out = open(fname2, "w")

with open(sys.argv[1], 'rU') as fh:
    blast_records = NCBIXML.parse(fh)
    for blast_record in blast_records:
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                identity = int((hsp.identities/hsp.align_length)*100)
                if identity > 0:
                    if hsp.expect < 0.01:
                        print '****Alignment****'
                        gbID = re.search('gi\|.*\|.*\|(.*)\|', alignment.hit_id)
                        print 'Hit ID:', gbID.group(1)
                        print 'Hit def:', alignment.hit_def
                        #print 'Hit start:', hsp.sbjct_start
                        #print 'Hit end:', hsp.sbjct_end
                        #print 'Query start:', hsp.query_start
                        #print 'Query end:', hsp.query_end
                        #print 'Query strand:', hsp.frame[0]
                        print 'Hit strand:', hsp.frame[1]
                        print 'E-value:', float(hsp.expect)
                        #print 'Identities:', hsp.identities
                        print 'Alignment length:', hsp.align_length
                        print 'Identity:', identity, '%'
                        #print hsp.query[:50] + '...'
                        #print hsp.match[:50] + '...'
                        #print hsp.sbjct[:50] + '...'

                        if not os.path.exists(str(gbID.group(1)+'.gb')):
                            GenBankDownload(gbID.group(1))
                        product, gb_strand, ire_seq = GenBankParser(str(gbID.group(1)+'.gb'), hsp.sbjct_start, hsp.frame[1])
                        print 'GenBank strand:', gb_strand
                        print 'Product:', product, '\n'
                        out.write('>'+str(re.sub(' ', '_', alignment.hit_def[:35]))+' Prod:'+str(product)+' Str:'+str(hsp.frame[1])+' E='+str(hsp.expect)+' Iden:'+str(identity)+'%\n')
                        out.write(str(ire_seq)+'\n\n')




                    '''
                    if gb_strand == hsp.frame[1]:
                         product
                    print ire_seq
                    print '\n\n'


fname = re.search('(.*)\.(\w*)', sys.argv[1])
fname2 = str(fname.group(1))+'_processed.txt'
out = open(fname2, "w")

out.write('Plus strand matches\n')
for key, value in reverse_IRE.items():
    out.write(str(key)+':'+str(value)+'\n')


TODO

# Make



'''