__author__ = 'Kavin'

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print args.accumulate(args.integers)

"""
In this case, the const=sum means that args.accumulate while resolve to sum or, if not called via --sum from the command line, resolve to max. Therefore, max/sum(args.integers) will occur
"""