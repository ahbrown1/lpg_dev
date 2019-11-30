#!/usr/bin/env python

import argparse
import csv
import copy
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="parse column(s) from CSV file")
    parser.add_argument(
        "--outfile", help="output file; stdout if not given", default="/dev/stdout"
    )
    parser.add_argument("--infile", help="input file", default="/dev/stdin")
    parser.add_argument(
        "--no-header",
        action="store_true",
        default=False,
        dest="no_header",
        help="skip headers in output",
    )
    parser.add_argument(
        "cnames", type=str, nargs="+", help="name(s) of header columns to parse"
    )
    args = parser.parse_args()

    with open(args.outfile, mode="w") as out_csv:
        csv_writer = csv.writer(out_csv, delimiter=",")

        with open(args.infile, "r") as in_csv:
            # get header
            csv_reader = csv.reader(in_csv, delimiter=",")
            for header_list in csv_reader :
                break
            #header = csv_reader.next
            #header = in_csv.readline().strip()
            #print(header)
            #sys.exit(0) 

            # create input header lookup dict
            lookup = {}
            #header_list = header.split(',')
            #print(header_list)
            #sys.exit(0) 

            for pos, name in enumerate(header_list):
                lookup[name] = pos
            print(lookup)
            #print(lookup['"p_state"'])
            # print the output header line
            if not args.no_header:
                csv_writer.writerow(args.cnames)

            # now get the actual data
            #csv_reader = csv.reader(in_csv, delimiter=",")
            for lineno, in_row in enumerate(csv_reader):
                out_row = []
                for name in args.cnames:
                    out_row.append(in_row[lookup[name]])
                csv_writer.writerow(out_row)
