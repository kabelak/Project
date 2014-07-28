__author__ = 'Kavin'

import sys
import xlrd
import re
from extractmatch import spireextract
from collections import defaultdict
from Bio import SeqIO

# ## Function to extract data from an excel worksheet
def exceldata(excelfile, sheet):
    workbook = xlrd.open_workbook(excelfile)
    worksheet = workbook.sheet_by_index(sheet)
    data = [[worksheet.cell_value(r, c) for c in range(0, 2)] for r in range(worksheet.nrows)]
    return data


# ## Function to extract TSS data from a specific type of excel worksheet
def extractTSS(excellist):
    forward = [];
    reverse = []
    for i in range(5, len(excellist)):
        if excellist[i][1] == 'F':
            forward.append(int(excellist[i][0]))
        elif datagrow[i][1] == 'R':
            reverse.append(int(excellist[i][0]))

    return forward, reverse


# ## Function to parse GenBank file for gene information
def GENBANKparse(gbfile):
    import indexed

    _genes = indexed.IndexedOrderedDict()
    _gene = {}
    for record in SeqIO.parse(open(gbfile, "r+"), "genbank"):
        for feature in record.features:
            if feature.type == "CDS":
                if "locus_tag" in feature.qualifiers:
                    genename = feature.qualifiers["locus_tag"][0]
                    _gene['Start'] = feature.location.start.position
                    _gene['End'] = feature.location.end.position
                    _gene['Strand'] = feature.location.strand
                    if "product" in feature.qualifiers:
                        _gene['Product'] = feature.qualifiers["product"]
                    _genes[str(genename)] = _gene
                    _gene = {}

    return _genes

### Initialise TSS data into an array
growthfile = "F:\Google Drive\Birkbeck\Project\RNAseq\Cortes sup mat\mmc2expogrowth.xlsx"
arrestfile = "F:\Google Drive\Birkbeck\Project\RNAseq\Cortes sup mat\mmc6arrest.xlsx"
datagrow = exceldata(growthfile, 5)
dataarrest = exceldata(arrestfile, 4)
fgrow, rgrow = extractTSS(datagrow)
farrest, rarrest = extractTSS(dataarrest)

### Initialise SPIRE and GenBank data into dictionaries
# TODO: Analyse which SPIRE output and which GenBank file to use!!!!!
spire_entries = spireextract("mtb.txt")
codingregions = GENBANKparse("M.tb H37Rv BCT 2013-Jun-13.gb")

### Initialise dictionaries and variables for use below
possiblestartsgrow = defaultdict(list)
possiblestartsarrest = defaultdict(list)
downpossiblestartsgrow = defaultdict(list)
downpossiblestartsarrest = defaultdict(list)
spread = 200
ilength = 5
for key, value in spire_entries.items():
    ### Extract information from a SPIRE match
    matchat = re.search('\((\d*):(\d*)', key)
    matchstart = int(matchat.group(1))
    matchend = int(matchat.group(2))
    matchloc = re.search('(\w*)\sof.*', value['Feature']).group(1)
    spire_entries[key]['Match Location'] = str(matchloc)
    gene = re.search('term=(\w*)', value['URL']).group(1)
    spire_entries[key]['Gene'] = str(gene)
    del spire_entries[key]['URL']

    ### Extract gene start/end information from GB file
    codingstart = codingregions[gene]['Start']
    codingend = codingregions[gene]['End']
    position = codingregions.keys().index(gene)

    ### Look at SPIRE matches and figure out if there is a TSS within 'spread' nucleotides of the coding start position
    if matchloc == 'upstream':
        if value['Direction'] == '+':
            for TSS in fgrow:
                if codingregions.values()[position - 1]['End'] <= TSS <= matchstart - ilength <= codingstart:
                    possiblestartsgrow[gene].append(TSS)
            for TSS in farrest:
                if codingregions.values()[position - 1]['End'] <= TSS <= matchstart - ilength <= codingstart:
                    possiblestartsarrest[gene].append(TSS)
        if value['Direction'] == '-':
            for TSS in rgrow:
                if codingend <= matchstart and matchend + ilength <= TSS <= codingregions.values()[position + 1][
                    'Start']:
                    possiblestartsgrow[gene].append(TSS)
            for TSS in rarrest:
                if codingend <= matchstart and matchend + ilength <= TSS <= codingregions.values()[position + 1][
                    'Start']:
                    possiblestartsarrest[gene].append(TSS)

    # ## For downstream IREs, look if there are TSSs between the IRE and the end of the coding sequence; If there aren't return, the closest possible TSS upstream
    if matchloc == 'downstream':
        #print 'downstream'
        if value['Direction'] == '+':
            for TSS in fgrow:
                if codingend <= TSS <= matchstart:
                    TSS = 'unlikely'
                    downpossiblestartsgrow[gene].append(TSS)
                if codingregions.values()[position - 1]['End'] <= TSS <= codingstart:
                    downpossiblestartsgrow[gene].append(TSS)
            for TSS in farrest:
                if codingend <= TSS <= matchstart:
                    TSS = 'unlikely'
                    downpossiblestartsarrest[gene].append(TSS)
                if codingregions.values()[position - 1]['End'] <= TSS <= codingstart:
                    downpossiblestartsarrest[gene].append(TSS)
        if value['Direction'] == '-':
            for TSS in rgrow:
                if matchstart - ilength <= TSS <= codingstart:
                    TSS = 'unlikely'
                    downpossiblestartsgrow[gene].append(TSS)
                if codingend <= TSS <= codingregions.values()[position + 1]['Start']:
                    downpossiblestartsgrow[gene].append(TSS)
            for TSS in rarrest:
                if matchend <= TSS <= codingstart:
                    TSS = 'unlikely'
                    downpossiblestartsarrest[gene].append(TSS)
                if codingend <= TSS <= codingregions.values()[position + 1]['Start']:
                    downpossiblestartsarrest[gene].append(TSS)

### Iterate through SPIRE matches to add the possible TSSs, and delete the SPIRE match if no TSSs found
for key, value in spire_entries.items():
    if possiblestartsgrow.has_key(value['Gene']):
        spire_entries[key]['Growth TSSs'] = possiblestartsgrow[value['Gene']]
    if possiblestartsarrest.has_key(value['Gene']):
        spire_entries[key]['Arrest TSSs'] = possiblestartsarrest[value['Gene']]
    if downpossiblestartsgrow.has_key(value['Gene']):
        if 'unlikely' in downpossiblestartsgrow[value['Gene']]:
            del downpossiblestartsgrow[value['Gene']]
        else:
            spire_entries[key]['down Growth TSSs'] = downpossiblestartsgrow[value['Gene']]
    if downpossiblestartsarrest.has_key(value['Gene']):
        if 'unlikely' in downpossiblestartsarrest[value['Gene']]:
            del downpossiblestartsarrest[value['Gene']]
        else:
            spire_entries[key]['down Arrest TSSs'] = downpossiblestartsarrest[value['Gene']]

    if not possiblestartsgrow.has_key(value['Gene']) and not possiblestartsarrest.has_key(value['Gene']) \
            and not downpossiblestartsgrow.has_key(value['Gene']) and not downpossiblestartsarrest.has_key(
            value['Gene']):
        del spire_entries[key]


# for key, value in sorted(spire_entries.items(), key=lambda x: x[1]):
### Print out values
print 'Number of successful matches: %i\n#################################\n\n' % len(spire_entries)
for key, value in spire_entries.items():
    a = spire_entries[key]
    print '\n%s on the %s strand giving IRE sequence %s which folds to %s with loop %s and is %s (%s, %s).' % \
          (key, a['Direction'], a['Sequence'], a['Folds to'], a['region'], a['Feature'], a['Gene'], a['Position'])
    if 'Growth TSSs' in a:
        print 'Possible exponential growth TSS(s):', a['Growth TSSs']
    if 'Arrest TSSs' in a:
        print 'Possible starvation TSS(s):', a['Arrest TSSs']
    if 'down Growth TSSs' in a:
        print 'IRE has no TSS between itself and end of CDS; Possible exponential growth TSS(s):', a['down Growth TSSs']
    if 'down Arrest TSSs' in a:
        print 'IRE has no TSS between itself and end of CDS; Possible starvation TSS(s):', a['down Arrest TSSs']
