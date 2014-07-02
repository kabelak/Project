__author__ = 'Kavin'

from Bio import SeqIO
gb_file = "CP000481.1.gb"
gb_record = SeqIO.parse(open(gb_file,"r"), "genbank")
for record in gb_record:
    print "Name %s, %i features" % (record.name, len(record.features))
    print repr(record.seq)