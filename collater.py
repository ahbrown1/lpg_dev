#!/usr/bin/env python

'''
   PDF batch collater
'''

import sys
import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter

def collate(paths, output):

    # Create a reader for each input file
    readers = []
    npages = -1
    for  path in paths:
        reader = PdfFileReader(path)
        path_pages = reader.getNumPages()
        if npages >= 0 :
            if path_pages != npages:
                raise Exception("Page count mismatch: file %s has %d pages; expecting %d"%(path, path_pages, npages ))
        else :
            npages = path_pages
        readers.append(reader)

    pdf_writer = PdfFileWriter()
    for page in range(npages) :
        for reader in readers :
            pdf_writer.addPage(reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

def main() :
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", help="output file name", default="output")
    parser.add_argument("infiles", help="input file names", nargs='+')
    args = parser.parse_args()
    import pdb; pdb.set_trace()
    collate( args.infiles, args.out)

if __name__ == '__main__':
    sys.exit(main())

    paths = ['document1.pdf', 'document2.pdf']
    merge_pdfs(paths, output='merged.pdf')
