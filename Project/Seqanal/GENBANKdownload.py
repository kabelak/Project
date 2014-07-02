__author__ = 'Kavin'

from Bio import Entrez

# ref.: http://wilke.openwetware.org/Parsing_Genbank_files_with_Biopython.html

organism_id = 'HE804045.1'

# replace with your real email (optional):
Entrez.email = 'whatever@mail.com'
# accession id works, returns genbank format, looks in the 'nucleotide' database:
handle=Entrez.efetch(db='nucleotide',id=organism_id,rettype='gb')
# store locally:
local_file=open(str(organism_id+'.gb'), 'w')
local_file.write(handle.read())
handle.close()
local_file.close()
