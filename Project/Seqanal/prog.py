__author__ = 'Kavin'

import argparse
import sys
import re


def main(argv):
    parser = argparse.ArgumentParser(description='Process some integers.',
                                     usage="Usage: %prog [options] <Blast XML file>")
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    # help='an integer for the accumulator')
    #parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                    const=sum, default=max,
    #                    help='sum the integers (default: find the max)')
    parser.add_argument('-u', '--upstream', action='store_true', default=False)
    parser.add_argument('IRE_len', type=int,
                        help='Define the length of sequence to pull (i.e.: UTR length between 20 and 300 bases)',
                        default=200, choices=range(19, 301, 1), nargs=1)
    parser.add_argument('file')

    args = parser.parse_args()
    print len(argv)
    print args.IRE_len[0]

    upstream_value = False
    if args.upstream:
        upstream_value = True

    if upstream_value:
        print '  true\n'
    else:
        print '  false\n'

    fname = re.search('(.*)\.(\w*)', args.file)
    fname2 = str(fname.group(1)) + '_extracted.txt'
    out = open(fname2, "w")
    print args.file
    with open(args.file, 'r') as fh:
        for lines in fh:
            out.write(str(lines) + '\n')

            #print args.accumulate(args.integers)


"""
In this case, the const=sum means that args.accumulate while resolve to sum or, if not called via --sum from the command line, resolve to max. Therefore, max/sum(args.integers) will occur
"""

if __name__ == "__main__":
    main(sys.argv)