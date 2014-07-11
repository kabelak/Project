__author__ = 'Kavin'

from Bio import SeqIO
from Bio import SeqFeature
import xlrd
import sys
import re

workbook = xlrd.open_workbook("F:\Google Drive\Birkbeck\Project\RNAseq\Cortes sup mat\mmc3TSSvsStartCodon.xlsx")
# workbook = xlrd.open_workbook(sys.argv[2])
sheet = workbook.sheet_by_index(0)
data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

# Create dicts to store TSS data
TSS = {}
row = {}
# For each entry (row), store the startcodon and strand information
for i in range(2, sheet.nrows - 1):
    if data[i][5] < -0.7:  # Ensures BASS score is within significant range
        Gene = data[i][0]
        row['Direction'] = str(data[i][3])
        row['StartCodon'] = int(data[i][4])
        TSS[str(Gene)] = row
        row = {}
    else:
        i += 1

outfile_init = re.search('(.*)\.(\w*)', sys.argv[1])
outfile = str(outfile_init.group(1)) + '_modified.' + str(outfile_init.group(2))

final_features = []
# TODO look in the TSS files and include, for each gene, the closest TSS which isn't part of another gene

for record in SeqIO.parse(open(sys.argv[1], "r+"), "genbank"):
    for feature in record.features:
        if feature.type == "gene" or feature.type == "CDS":
            if TSS.has_key(feature.qualifiers["locus_tag"][0]):
                newstart = TSS[feature.qualifiers["locus_tag"][0]]['StartCodon']
                if feature.location.strand == 1:
                    feature.location = SeqFeature.FeatureLocation(SeqFeature.ExactPosition(newstart - 1),
                                                                  SeqFeature.ExactPosition(
                                                                      feature.location.end.position),
                                                                  feature.location.strand)
                else:
                    feature.location = SeqFeature.FeatureLocation(
                        SeqFeature.ExactPosition(feature.location.start.position),
                        SeqFeature.ExactPosition(newstart), feature.location.strand)
        final_features.append(feature)  # Append final features
    record.features = final_features
    with open(outfile, "w") as new_gb:
        SeqIO.write(record, new_gb, "genbank")

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