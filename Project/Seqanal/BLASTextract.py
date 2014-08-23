__author__ = 'Kavin'

import sys
import re


def main(argv):
    genera = {}
    fname = re.search('(.*)\.(\w*)', argv)
    fname2 = str(fname.group(1)) + '_list.' + str(fname.group(2))
    outp = open(fname2, "w")
    with open(argv, r"U") as f:
        for line in f:
            genus = re.search("\|(?:\s||\t)(\w*)\s", line)
            if not genera.has_key(genus.group(1)):
                genera[genus.group(1)] = 1
            else:
                genera[genus.group(1)] += 1

    for key, value in genera.items():
        outp.write(str(key) + ', ')


if __name__ == "__main__":
    main(sys.argv[1])
