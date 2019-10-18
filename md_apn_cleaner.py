#!/usr/bin/env python

import argparse
import csv
import copy
import re

re_long_apn = re.compile('^(\d+)\-\d+\-(\d+)$')
re_short_apn = re.compile('^(\d+)\-(\d+)$')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='remove extraneous numbers from MD APN')
    parser.add_argument('--outfile', help='output file; stdout if not given', default='Y')
    parser.add_argument('infile', help='input file',)
    #parser.add_argument('files', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')
    args = parser.parse_args()

    # If you would call fileinput.input() without files it would try to process all arguments.
    # We pass '-' as only file when argparse got no files which will cause fileinput to read from stdin
    #for line in fileinput.input(files=args.files if len(args.files) > 0 else ('-', )):
    #for line in fileinput.input(files=args.files):
    #    print(line)


    with open(args.outfile, mode='w') as  out_csv :
        writer = csv.writer(out_csv, delimiter=',')
        
        with open( args.infile, 'r') as in_csv :
            # get header
            header = in_csv.readline()
   
            # create header lookup dict
            lookup = {}
            header_list = header.split(',')
            for pos, name in enumerate(header_list) :
                lookup[name] = pos

            # now get the actual data
            reader = csv.reader(in_csv, delimiter=',')
            for  lineno, loop_row in enumerate(reader):
                row = copy.copy(loop_row)
                apn = row[lookup['APN']]
                long_apn = re_long_apn.match(apn)
                if long_apn:
                    apn = "%02d-%s"%(int(long_apn.group(1)), long_apn.group(2))

                short_apn = re_short_apn.match(apn)
                if short_apn:
                    apn = "%02d-%s"%(int(short_apn.group(1)), short_apn.group(2))
                else :
                    print 'Bad APN format on line %d'%(lineno +1,)
                print apn
   

        
