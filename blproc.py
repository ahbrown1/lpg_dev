#!/usr/bin/env python
'''
   Take as inputs :
   - the big file :  a cat of all processed CVS files in preferred priority order
     Ex: A cvscat <Out of State Owners>.csv <In State Owners>.csv  > county.csv
   - the maximum size of the desired ID input file
   - the name of the (to be created) ID input file

   Results:
    - the ID input file consisting of at most, the size limit
    - the 'big file' now contains only records that are not in the ID input file
      it is deleted if there are no remaining records
'''
import csv
import argparse
import tempfile
import os

dflt_backlog = os.getenv('LPG_BACKLOG', './backlog/')
parser = argparse.ArgumentParser(description='Preprocess ID inpu .')

parser.add_argument('--max_records', type=int, help='Max records for ID import', default=250)
parser.add_argument('--backlog', type=str, help='backlog storage dir', default=dflt_backlog )
parser.add_argument('bigfile', type=str, help='name of the big fileD' )

args = parser.parse_args()


assert( os.path.isdir(args.backlog))

has_remainder = True
while  has_remainder :

    id_out_file = None
    
    for i in range(1000):
       path = os.path.join(args.backlog,"id_out.%03d.csv"%i)
       if not os.path.exists(path) :
           id_out_file = path
           break
    
    assert( id_out_file is not None)
    remainder_file = tempfile.mktemp()


    with open( args.bigfile, 'r' ) as big_csv :
        big_csv_reader = csv.reader(big_csv)
    
        # get header
        header = big_csv_reader.next()
    
        print header
    
        has_remainder = False
        with open(id_out_file, mode='w') as id :
            id_writer = csv.writer(id)
            id_writer.writerow(header)
            with open(remainder_file, mode='w') as remaining:
                remainder_writer = csv.writer(remaining)
                remainder_writer.writerow(header)
    
                for (count, record) in enumerate(big_csv_reader) :
                    if count >= args.max_records :
                        has_remainder = True
                        remainder_writer.writerow(record) 
                    else :
                        id_writer.writerow(record) 
     
        # ID import file is complete.
        # overwrite remainder to the big file for the next run
        if has_remainder :
            os.rename(remainder_file, args.bigfile)   # (needs an extra trick for MSW)
        else:
            os.remove( remainder_file )   # nothing but a header there 
            os.remove( args.bigfile )   # nothing but a hearder there 
