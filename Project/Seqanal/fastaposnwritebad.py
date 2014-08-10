__author__ = 'Kavin'

import sys
import re

from Bio import SeqIO

with open("outfile.txt", "w") as f:
    for seq_record in SeqIO.parse(sys.argv[1], "fasta"):
        org = re.search('\[(.*)\]', str(seq_record.description))
        # print org.group(1)
        f.write(">" + str(seq_record.description[:13]) + org.group(1) + "\n")
        SeqIO.write(seq_record.seq, f, "fasta")  # geneIndex -5 to -65
