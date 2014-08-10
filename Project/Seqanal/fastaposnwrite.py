__author__ = 'Kavin'

import sys
import re
from Bio import SeqIO

fname = re.search('(.*)\.(\w*)', sys.argv[1])
fname2 = str(fname.group(1)) + '_processed.' + str(fname.group(2))

with open(fname2, "w") as f:
    for seq_record in SeqIO.parse(sys.argv[1], "fasta"):
        string = ">" + str(seq_record.description[4:12]) + str(seq_record.description[43:81])
        f.write(re.sub('\s|\|', '_', string) + "\n")
        f.write(str(seq_record.seq) + "\n\n")
