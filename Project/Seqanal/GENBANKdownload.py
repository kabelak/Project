__author__ = 'Kavin'

from Bio import Entrez

# ref.: http://wilke.openwetware.org/Parsing_Genbank_files_with_Biopython.html

# replace with your real email (optional):
Entrez.email = 'whatever@mail.com'
# accession id works, returns genbank format, looks in the 'nucleotide' database:
handle=Entrez.efetch(db='nucleotide',id='CP002059.1',rettype='gb')
# store locally:
local_file=open('CP002059.1.gb', 'w')
local_file.write(handle.read())
handle.close()
local_file.close()
