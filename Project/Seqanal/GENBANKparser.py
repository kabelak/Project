__author__ = 'Kavin'

from Bio import SeqIO
gb_file = "CP003119.1.gb"
gb_record = SeqIO.parse(open(gb_file, "r"), "genbank")
mysnp = 2421243
for record in gb_record:
    for feature in record.features:
        #print feature
        if mysnp in feature:
            if feature.type == 'CDS':
                if 'product' in feature.qualifiers:
                    print feature.qualifiers['product'][0]
                    #print("%s %s" % (feature.type, feature.qualifiers.get('product')))
                location = feature.location
                if location.strand == 1:
                    coding_start = location.start.position
                    coding_end = location.end.position
                    print record.seq[coding_start:coding_end]
                else:
                    coding_start = location.end.position
                    coding_end = location.start.position
                    print record.seq[coding_end:coding_start]
                    print 'Please note upstream sequence starts after the end of the sequence in this case'
                print location.strand, coding_start, coding_end




            '''
            for key, value in feature.qualifiers.items():
                if key == 'product':
                    print value

            #print feature.type()
            #print(feature.qualifiers.get('product'))
            #print "Name %s, %i features" % (record.name, len(record.features))
            #print repr(record.seq)
print feature.qualifiers['product'][0].lower()
#need strand info to extract sequence

'''

'''
def GenBankParser(gbFile,start):
    #from Bio import SeqIO
    gb_record = SeqIO.parse(open(gbFile, "r"), "genbank")
    for record in gb_record:
        for feature in record.features:
            if start in feature:
                print("%s %s" % (feature.type, feature.qualifiers.get('product')))

'''
