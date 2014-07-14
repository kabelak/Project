__author__ = 'Kavin'

from Bio import Entrez
import sys

# ref.: http://wilke.openwetware.org/Parsing_Genbank_files_with_Biopython.html

# organism_id = 'HE804045.1'

def GenBankDownload(organism_id):
    Entrez.email = 'kabela01@mail.bbk.ac.uk'
    handle = Entrez.efetch(db='nucleotide', id=organism_id, rettype='gb')
    local_file = open(str(organism_id + '.gb'), 'w')
    local_file.write(handle.read())
    handle.close()
    local_file.close()


if __name__ == "__main__":
    GenBankDownload(sys.argv[1])