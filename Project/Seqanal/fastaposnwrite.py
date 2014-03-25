__author__ = 'Kavin'

import sys

from Bio import SeqIO

with open("outfile.txt","w") as f:
        for seq_record in SeqIO.parse(sys.argv[1], "fasta"):
                f.write(">" + str(seq_record.description[:89]) + "\n")
                f.write(str(seq_record.seq[-65:-5]) + "\n\n") # position -5 to -65
