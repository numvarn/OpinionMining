#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os import path
from os import makedirs
from os.path import isfile, join
import sys
import csv

def readSymptoms():
    symptoms = []
    rows = csv.reader(open("./dict/symptoms-60.csv", "rb"))
    for row in rows:
        symptoms.append(row[0].decode('utf-8'))
    return symptoms

def createVector(rootDir, dirname, dest_path, symptom, symptomID):
    # List all file from target directory
    print "Processing Directory : ", dirname
    process_dir = rootDir+"/"+dirname+"/pos-stopword"
    onlyfiles = [f for f in listdir(process_dir) if isfile(join(process_dir, f))]
    for filename in onlyfiles:
        print filename

def main():
    if len(sys.argv) != 1:
        symptoms = readSymptoms()

        rootDir = sys.argv[1]

        symptomID = 1
        destination_dir = rootDir+"/00-word-vector-symps"
        # Create directory for store result file
        if not path.exists(destination_dir):
            makedirs(destination_dir)

        # List all file from target directory
        onlyDir = [ name for name in listdir(rootDir) if path.isdir(path.join(rootDir, name)) ]
        for symp in symptoms:
            print "Processing Sysmptom : ", symp, "\n"

            dest_path = destination_dir+"/"+str(symptomID)+"-"+symp+".csv"

            for dirname in onlyDir:
                if dirname != '00-word-vector-symps' and dirname == 'health.haijai.com':
                    createVector(rootDir, dirname, dest_path, symp, symptomID)
            symptomID += 1

            if symptomID > 2:
                break
    else:
        print "Please, Enter File Directory"


if __name__ == '__main__':
    main()
