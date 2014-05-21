__author__ = 'Kavin'

import sys

from Bio import SeqIO

with open("outRNAfastafile.txt","w") as f:
        for seq_record in SeqIO.parse(sys.argv[1], "fasta"):
                f.write(">" + str(seq_record.description[4:12]) + seq_record.description[43:81] + "\n")
                f.write(str(seq_record.seq) + "\n\n")
