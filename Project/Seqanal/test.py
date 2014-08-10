__author__ = 'Kavin'

import sys


def spireextract(
        spirefile):  # TODO: Feature, Distance, Position and URL are repeated if there are both up/dowstream matches for a SPIRE entry - resolve! (duplicate the previous data, and add the new entry)
    import re  # TODO: if you're gona fix this, might as well fix the data structure so as to get the gene names etc

    _spire_entry = {}
    _spire_entries = {}
    with open(spirefile, 'rU') as _f:
        for _line in _f:
            if _line.startswith('Match'):
                _line = re.sub('\n', '', _line)
                entry = _line
                _line = next(_f)
                while not _line.startswith('None'):
                    while not _line.startswith('\tAlignments'):
                        _line = re.sub('\n|\t', '', _line)
                        characteristic = re.search('(\w*):\s(.*)', _line)
                        _spire_entry[characteristic.group(1)] = characteristic.group(2)
                        _line = next(_f)
                    _line = next(_f)
                    if _line.startswith('None'):
                        break
                    else:
                        _spire_entry2 = _spire_entry.copy()
                        while not _line.startswith('\tAlignments'):
                            _line = re.sub('\n|\t', '', _line)
                            characteristic = re.search('(.*):\s(.*)', _line)
                            _spire_entry2[characteristic.group(1)] = characteristic.group(2)
                            _line = next(_f)
                        entry2 = str(entry + '2')
                        if _spire_entry2['Direction'] == 'forward':
                            _spire_entry2['Direction'] = '+'
                        else:
                            _spire_entry2['Direction'] = '-'
                        _spire_entries[entry2] = _spire_entry2
                if _spire_entry['Direction'] == 'forward':
                    _spire_entry['Direction'] = '+'
                else:
                    _spire_entry['Direction'] = '-'
                _spire_entries[entry] = _spire_entry
                _spire_entry = {}
    return _spire_entries


'''
spire_entries = spireextract(sys.argv[1])

for key, value in spire_entries.items():
    print key, value


'''


def main():
    spire_entries = spireextract(sys.argv[1])


if __name__ == "__main__":
    main()

'''
######## sorting a dict by value

from collections import defaultdict
import re

numbertimes = defaultdict(int)

for key, value in spire_entries.items():
    gene = re.search('term=(\w*)', value['URL']).group(1)
    numbertimes[gene] +=1

for occ in sorted(numbertimes, key=numbertimes.get):
    print numbertimes[occ], occ




                if _spire_entry['Direction'] == 'forward':
                    _spire_entry['Direction'] = '+'
                else:
                    _spire_entry['Direction'] = '-'

'''