#!/usr/bin/env python

import argparse
import csv
import copy
import re

re_long_apn = re.compile('^(\d+)\-\d+\-(\d+)$')
re_short_apn = re.compile('^(\d+)\-(\d+)$')
DFLT_APN_NAME = 'APN'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='remove extraneous numbers from MD APN')
    parser.add_argument('--outfile', help='output file; stdout if not given', default='/dev/stdout')
    parser.add_argument('--infile', help='input file; stdin if not given', default='/dev/stdin')
    parser.add_argument('--apn-name', dest='apn_name', help='APN field name', default=DFLT_APN_NAME)
    args = parser.parse_args()


    with open(args.outfile, mode='w') as  out_csv :
        writer = csv.writer(out_csv, delimiter=',')
        
        with open( args.infile, 'r') as in_csv :
            # get header
            header = in_csv.readline().strip()
            out_csv.write("%s\n"%header)
   
            # create header lookup dict
            lookup = {}
            header_list = header.split(',')
            assert(args.apn_name in header_list)

            for pos, name in enumerate(header_list) :
                lookup[name] = pos

            # now get the actual data
            reader = csv.reader(in_csv, delimiter=',')
            for  lineno, loop_row in enumerate(reader):
                row = copy.copy(loop_row)
                apn = row[lookup[args.apn_name]]
                long_apn = re_long_apn.match(apn)
                if long_apn:
                    # remove intermediate digits between 2 dashes
                    # (doesn't play well with most lookups)
                    apn = "%02d-%s"%(int(long_apn.group(1)), long_apn.group(2))

                short_apn = re_short_apn.match(apn)
                if short_apn:
                    # make fiels before leading dash 2 digits
                    apn = "%02d-%s"%(int(short_apn.group(1)), short_apn.group(2))
                else :
                    raise Exception('Bad APN format on line %d'%(lineno +1,))
                row[lookup[args.apn_name]] = apn
                writer.writerow(row)
   

        
