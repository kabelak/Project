from __future__ import division
__author__ = 'Kavin'

import sys
import re
import time
import os
from Bio.Blast import NCBIXML
from Bio import Entrez
from Bio import SeqIO


#forward_IRE = {}
#reverse_IRE = {}


def GenBankDownload(organism_id):
    print "Downloading GenBank file for", organism_id
    Entrez.email = 'kabela01@mail.bbk.ac.uk'
    handle = Entrez.efetch(db='nucleotide',id=organism_id,rettype='gb')
    local_file = open(str(organism_id+'.gb'), 'w')
    local_file.write(handle.read())
    handle.close()
    local_file.close()
    print "Download completed"
    time.sleep(2)   # Important to prevent DDoS type control from NCBI

def GenBankParser(gbFile, start, frame, IRE=200):
    gb_record = SeqIO.parse(open(gbFile, "r"), "genbank")
    for record in gb_record:
        for feature in record.features:
            if start in feature:
                if feature.type == 'CDS':
                    if 'product' in feature.qualifiers:
                        product = feature.qualifiers['product'][0]
                    location = feature.location
                    # TODO how to make sure it is checking in the right strand? At the moment, the 'start in feature' seems to find... but how?
                    if frame != location.strand:
                        print '!!!!!Strands do not match! The GBrecord strand is', location.strand, 'while the BLAST strand is', frame, '!!!!!!!!'
                        product = str(product + 'DIFFERENT STRANDS')
                    if location.strand == 1:
                        ire_start = location.start.position-IRE
                        ire_end = location.start.position
                        ire_sequence = record.seq[ire_start:ire_end]
                    else:
                        ire_start = location.end.position+IRE
                        ire_end = location.end.position
                        #print 'Reverse Strand; Upstream Region:', record.seq[ire_end:ire_start]
                        ire_sequence = record.seq[ire_end:ire_start]
                        ire_sequence = ire_sequence[::-1]   # Reverse the sequence
    if 'product' in locals():   # Check existence of values before returning
        return (product, location.strand, ire_sequence)
    else:
        return ('NA', '0', 'NA')



fname = re.search('(.*)\.(\w*)', sys.argv[1])
fname2 = str(fname.group(1))+'_processed2.txt'
out = open(fname2, "w")

with open(sys.argv[1], 'rU') as fh:
    blast_records = NCBIXML.parse(fh)
    for blast_record in blast_records:
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                identity = int((hsp.identities/hsp.align_length)*100)
                if identity > 80:
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

                        if not os.path.exists(str(gbID.group(1)+'.gb')):    # Check if GB file has previously been downloaded
                            GenBankDownload(gbID.group(1))

                        product, gb_strand, ire_seq = GenBankParser(str(gbID.group(1)+'.gb'), hsp.sbjct_start, hsp.frame[1])
                        print 'GenBank strand:', gb_strand
                        print 'Product:', product, '\n'
                        if product != 'NA':
                            out.write('>' + str(re.sub(' ', '_', alignment.hit_def[:35])) + ' Prod:' + str(
                                product) + ' Str:' + str(hsp.frame[1]) + ' E=' + str(hsp.expect) + ' Iden:' + str(
                                identity) + '%\n')
                            out.write(str(ire_seq) + '\n\n')

'''
if gb_strand == hsp.frame[1]:
     product
print ire_seq
print '\n\n'

out.write('Plus strand matches\n')
for key, value in reverse_IRE.items():
    out.write(str(key)+':'+str(value)+'\n')
'''
