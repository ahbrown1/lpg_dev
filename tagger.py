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
parser.add_argument('--tag_prefix', type=str, help='batch name prefix', default='`batch_')
parser.add_argument('--backlog', type=str, help='backlog storage dir', default=dflt_backlog )
parser.add_argument('infile', type=str, help='name of the big fileD' )

args = parser.parse_args()



## >>> import csv
## >>> with open('eggs.csv', newline='') as csvfile:
## ...     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
## ...     for row in spamreader:
## ...         print(', '.join(row))
## Spam, Spam, Spam, Spam, Spam, Baked Beans
## Spam, Lovely Spam, Wonderful Spam
#import pdb; pdb.set_trace()


path = os.path.join(args.backlog,"out.csv")
assert( os.path.isdir(args.backlog))
assert(not os.path.exists(path) )

with open(path, mode='w') as id :
    writer = csv.writer(id, delimiter=',')
    with open( args.infile, 'r') as csvfile :
        # get header
        header = csvfile.readline().strip()
        header_list = header.split(',')
        print header_list
        flen = len(header_list)
        assert(TAG not in header_list )

        header_list.append(TAG)
        header = ','.join(header_list) 
        print header
        id.write(header)
    
        reader = csv.reader(csvfile, delimiter=',')
        batch = args.batch_start
        assert( batch >= 0 )
        index = 0
        for  loop_row in reader:
            row  = copy.copy(loop_row)
    
            #print flen
            #print len(row)
            assert(len(row) == flen )
            tag = '%s%05d'%(args.tag_prefix, batch )
    	    row.append(tag)
            index +=1 
            if index > args.batch_size :
                index = 0
                batch += 1
            writer.writerow(row)
    	print(','.join(row))

     



#has_remainder = True
#while  has_remainder :
#
#    id_out_file = None
#    
#    for i in range(1000):
#       path = os.path.join(args.backlog,"id_out.%03d.csv"%i)
#       if not os.path.exists(path) :
#           id_out_file = path
#           break
#    
#    assert( id_out_file is not None)
#    remainder_file = tempfile.mktemp()
#
#
#    with open( args.bigfile, 'r' ) as big_csv :
#    
#        # get header
#        header = big_csv.readline()
#    
#        #print header
#    
#        has_remainder = False
#        with open(id_out_file, mode='w') as id :
#            id.write(header)
#            with open(remainder_file, mode='w') as remaining:
#                remaining.write(header)
#   
#                for (count, record) in enumerate(big_csv) :
#                    if count >= args.max_records :
#                        has_remainder = True
#                        remaining.write(record)
#                    else :
#                        id.write(record)
#    
#        os.chmod(id_out_file, 0o444)   # set to read-only
# 
#        # ID import file is complete.
#        # overwrite remainder to the big file for the next run
#        
#        if has_remainder :
#            os.rename(remainder_file, args.bigfile)   # (note: needs an extra trick for MSW)
#        else:
#            os.remove( remainder_file )   # nothing but a header there 
#            os.remove( args.bigfile )   # nothing usefulr there 
