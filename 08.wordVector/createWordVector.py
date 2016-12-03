#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os import path
from os import makedirs
from os.path import isfile, join
import sys

def main():
    if len(sys.argv) != 1:
        filedir = sys.argv[1]

        upone_level = path.dirname(filedir.rstrip('/'))
        destination_dir = upone_level+"/word-vectors"

        # Create directory for store result file
        if not path.exists(destination_dir):
            makedirs(destination_dir)

        # List all file from target directory
        onlyfiles = [f for f in listdir(filedir) if isfile(join(filedir, f))]

        for filename in onlyfiles:
            if filename != '.DS_Store':
                print "Processing file : ", filename
    else:
        print "Please, Enter File Directory"


if __name__ == '__main__':
    main()
