#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os import path
from os import makedirs
from os.path import isfile, join
from shutil import copyfile
import sys
import csv

def readSymptoms():
    symptoms = []
    rows = csv.reader(open("./dict/symptoms-60.csv", "rb"))
    for row in rows:
        symptoms.append(row[0].decode('utf-8'))
    return symptoms

def filterDocument(filepath, destination_dir, filename, symptoms):

    src = filepath+"/"+filename
    dst = destination_dir+"/"+filename

    founded = 0

    with open(filepath+"/"+filename, 'r') as f:
        for line in f:
            newword = []
            if len(line.rstrip('\n')) > 0:
                newline = ''
                string = line.decode('utf-8')
                words = string.split("|")

                for word in words:
                    if word in symptoms:
                        copyfile(src, dst)
                        founded = 1
                        break

            if founded == 1:
                break
    f.close()

def main():
    symptoms = readSymptoms()

    if len(sys.argv) != 1:
        filedir = sys.argv[1]

        upone_level = path.dirname(filedir.rstrip('/'))
        destination_dir = upone_level+"/filtered"

        # Create directory for store result file
        if not path.exists(destination_dir):
            makedirs(destination_dir)

        # List all file from target directory
        onlyfiles = [f for f in listdir(filedir) if isfile(join(filedir, f))]

        for filename in onlyfiles:
            if filename != '.DS_Store':
                print "Processing file : ", filename
                filterDocument(filedir, destination_dir, filename, symptoms)
    else:
        print "Please, Enter File Directory"

if __name__ == '__main__':
    main()
