from __future__ import division

__author__ = 'Kavin'

import sys
import re
import time
import os
import argparse
from Bio.Blast import NCBIXML
from Bio import Entrez
from Bio import SeqIO
# from GENBANKdownload import GenBankDownload

def GenBankDownload(organism_id):
    Entrez.email = 'kabela01@mail.bbk.ac.uk'
    handle = Entrez.efetch(db='nucleotide', id=organism_id, rettype='gb')
    local_file = open(str(organism_id + '.gb'), 'w')
    local_file.write(handle.read())
    handle.close()
    local_file.close()


def GenBankParser(gbFile, start, frame, IRE=200,
                  Upstream=True):
    with open(gbFile, "r") as gbFile_handle:
        gb_record = SeqIO.parse(gbFile_handle, "genbank")
        for record in gb_record:
            for feature in record.features:
                if start in feature:
                    if feature.type == 'CDS':
                        if 'product' in feature.qualifiers:
                            product = feature.qualifiers['product'][0]
                        location = feature.location
                        # # Check if strand predicted by BLAST matches strand in GB file
                        if frame != location.strand:
                            print '!!!!!Strands do not match! The GBrecord strand is', location.strand, 'while the BLAST strand is', frame, '!!!!!!!!'
                            product = str(product + ' DIFFERENT STRANDS')

                        ## Extract the sequence
                        if Upstream:
                            if location.strand == 1:
                                ire_start = location.start.position - IRE
                                ire_end = location.start.position
                                ire_sequence = record.seq[ire_start:ire_end]
                            else:
                                ire_start = location.end.position + IRE
                                ire_end = location.end.position
                                ire_sequence = record.seq[
                                               ire_end:ire_start].reverse_complement()  # Reverse the sequence
                        else:
                            if location.strand == 1:
                                ire_start = location.end.position
                                ire_end = location.end.position + IRE
                                ire_sequence = record.seq[ire_start:ire_end]
                            else:
                                ire_start = location.start.position
                                ire_end = location.start.position - IRE
                                ire_sequence = record.seq[
                                               ire_end:ire_start].reverse_complement()  # Reverse the sequence

        if 'product' in locals():  # Check existence of values before returning
            return (product, location.strand, ire_sequence)
        else:
            return ('NA', '0', 'NA')


def check_range(arg):  # Function to ensure correct range of IRE Length is input at the command prompt
    try:
        value = int(arg)
    except ValueError as err:
        raise argparse.ArgumentTypeError(str(err))
    if value < 20 or value > 300:
        message = "Expected length between 20 and 300 inclusive, received value = {}".format(value)
        raise argparse.ArgumentTypeError(message)
    return value


def main(argv):
    """Blast Parser, GenBank File Downloaded, IRE Sequence Extractor"""
    parser = argparse.ArgumentParser(description='Blast Parser, GenBank File Downloaded, IRE Sequence Extractor',
                                     usage="[optional upstream] [length of sequence] <Blast XML file>")
    parser.add_argument('-u', '--upstream', action='store_true', default=False,
                        help='Defines whether to look upstream; Default looks downstream')
    parser.add_argument('IRE_len', type=check_range,
                        help='Define the length of sequence to pull (i.e.: UTR length between 20 and 300 bases)',
                        default=200, nargs=1)
    parser.add_argument('file', help='BLAST XML file')
    args = parser.parse_args()

    upstream_value = False
    if args.upstream:
        upstream_value = True

    if not args.file:
        parser.error("Please specify a BLAST XML file")

    # Create output file
    fname = re.search('(.*)\.(\w*)', args.file)
    fname2 = str(fname.group(1)) + '_extracted.txt'
    out = open(fname2, "w")

    i = 0
    with open(args.file, 'rU') as blastxml:
        blast_records = NCBIXML.parse(blastxml)
        for blast_record in blast_records:
            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    identity = int((hsp.identities / hsp.align_length) * 100)
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

                            # Download GB file if not previously downloaded
                            if os.path.exists(str(gbID.group(1) + '.gb')):
                                if os.path.getsize(str(gbID.group(1) + '.gb')) > 10:
                                    pass
                                else:
                                    print "File corrupt; Re-downloading GenBank file for", gbID.group(1)
                                    GenBankDownload(gbID.group(1))
                                    print "Download completed"
                                    time.sleep(1)  # Important to prevent DDoS type control from NCBI
                                    i += 1  # Count the number of downloaded files
                            else:
                                print "Downloading GenBank file for", gbID.group(1)
                                GenBankDownload(gbID.group(1))
                                print "Download completed"
                                time.sleep(1)  # Important to prevent DDoS type control from NCBI
                                i += 1  # Count the number of downloaded files

                            # Parse GB file for required information
                            product, gb_strand, ire_seq = GenBankParser(str(gbID.group(1) + '.gb'), hsp.sbjct_start,
                                                                        hsp.frame[1], IRE=args.IRE_len[0],
                                                                        Upstream=upstream_value)
                            print 'GenBank strand:', gb_strand
                            print 'Product:', product
                            print 'IRE Seq:', ire_seq, '\n'

                            # Ensure only existing products and non-blank IRE sequences are passed on for writing to file
                            if product != 'NA' and ('A' or 'C' or 'G' or 'T' or 'U') in ire_seq:
                                out.write('>' + str(gbID.group(1)[:-2]) + str(
                                    re.sub(' ', '_', alignment.hit_def[:35])) + ' Prod:' + str(
                                    product) + ' Str:' + str(hsp.frame[1]) + ' E=' + str(hsp.expect) + ' Iden:' + str(
                                    identity) + '%\n')
                                out.write(str(ire_seq) + '\n\n')

    # Housekeeping and displaying if any files downloaded
    out.close()
    if i > 0:
        print """\n\n************************************************\nNumber of files downloaded: %s \n************************************************""" % i


if __name__ == "__main__":
    main(sys.argv)