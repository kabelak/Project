__author__ = 'Kavin'

from Bio import SeqIO
gb_file = "CP000481.1.gb"
gb_record = SeqIO.parse(open(gb_file, "r"), "genbank")
mysnp = 203538
for record in gb_record:
    for feature in record.features:
        #print feature
        if mysnp in feature:
            print("%s %s" % (feature.type, feature.qualifiers.get('product')))
            #print "Name %s, %i features" % (record.name, len(record.features))
            #print repr(record.seq)




'''
def GenBankParser(gbFile,start):
    #from Bio import SeqIO
    gb_record = SeqIO.parse(open(gbFile, "r"), "genbank")
    for record in gb_record:
        for feature in record.features:
            if start in feature:
                print("%s %s" % (feature.type, feature.qualifiers.get('product')))

'''
