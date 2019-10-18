#!/usr/bin/env python
'''
   Take as inputs :
   - the big file :  a cat of all processed CVS files in preferred priority order
     Ex: A cvscat <Out of State Owners>.csv <In State Owners>.csv  > county.csv
   - the  maxximum range to be taggedm
   - the name of the (to be created) ID input file

   Results:
    - the ID input file with tag ranges added 
'''
import csv
import argparse
import tempfile
import os
import  sys, stat
import copy

TAG='Tags'

dflt_backlog = os.getenv('LPG_BACKLOG', './backlog/')
parser = argparse.ArgumentParser(description='Preprocess ID input.')

parser.add_argument('--batch_size', type=int, help='Max records per tagged batch', default=250)
parser.add_argument('--batch_start', type=int, help='starting tag index', default=0)
parser.add_argument('--tag_prefix', type=str, help='batch name prefix', default='batch_')
parser.add_argument('--backlog', type=str, help='backlog storage dir', default=dflt_backlog )
parser.add_argument('--outfile', type=str, help='output file', default='tagged.csv' )
parser.add_argument('infile', type=str, help='name of the big fileD' )

args = parser.parse_args()



path = os.path.join(args.backlog, args.outfile)
assert( os.path.isdir(args.backlog))
assert(not os.path.exists(path) )

with open(path, mode='w') as id :
    writer = csv.writer(id, delimiter=',')
    with open( args.infile, 'r') as csvfile :
        # get header
        header = csvfile.readline().strip()
        header_list = header.split(',')
        #print header_list
        flen = len(header_list)
        assert(TAG not in header_list )

        header_list.append(TAG)
        header = ','.join(header_list) 
        #print header
        id.write("%s\n"%header)
    
        reader = csv.reader(csvfile, delimiter=',')
        batch = args.batch_start
        assert( batch >= 0 )
        index = 0
        for  loop_row in reader:
            row  = copy.copy(loop_row)
    
            assert(len(row) == flen )
            tag = '%s%03d'%(args.tag_prefix, batch )
    	    row.append(tag)
            writer.writerow(row)

            index +=1 
            if index > args.batch_size :
                index = 0
                batch += 1
print "Done."

     

