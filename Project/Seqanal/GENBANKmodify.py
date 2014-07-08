__author__ = 'Kavin'

from Bio import SeqIO

gb_file = "mtbtomod.gb"
gb_record = SeqIO.parse(open(gb_file, "r+"), "genbank")
mysnp = 2421243
rvnumber = 'Rv0005'
newstart = 5357

final_features = []

for record in gb_record:
    for feature in record.features:
        # print feature
        if feature.type == "gene":
            #print feature.type
            if feature.qualifiers["locus_tag"][0] == rvnumber:
                #print feature
                print "no"
                if feature.location.strand == 1:
                    print "no"
                    #feature._loc = _loc("5357..7267", 1000, 1)
                    #feature.qualifiers["amend_position"] = "%s:%s" % (newstart, feature.location.end+1)
                    feature._set_location_operator(5357)
                    #print feature.location.start
                else:
                    feature.location.end.position = newstart
        final_features.append(feature)
    record.features = final_features
    with open("testest.gb", "w") as for_rast:
        SeqIO.write(record, for_rast, "genbank")

'''
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


x = 0
final_features = []
for f in record.features:
    if f.type == "CDS":
        f.qualifiers["locus_tag"] = "%s_%s" % (record.id, x+1)
        x += 1
    final_features.append(f)

record.features = final_features
with open("/Users/k/Desktop/prueba/contig_for_rast.gbk","w") as for_rast:
    SeqIO.write(record, for_rast, "genbank")

'''