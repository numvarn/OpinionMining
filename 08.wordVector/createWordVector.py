#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os import path
from os import makedirs
from os.path import isfile, join
import sys
import csv
import operator

def readSymptoms():
    symptoms = []
    rows = csv.reader(open("./dict/symptoms-60.csv", "rb"))
    for row in rows:
        symptoms.append(row[0].decode('utf-8'))
    return symptoms

def readVerbsDict():
    verbs = {}
    rows = csv.reader(open("./dict/telex-verb-utf8.csv", "rb"))
    count = 0
    for row in rows:
        if count > 1:
            verbs.update({row[0]:row[1]})
        count += 1
    return verbs

def createVector(rootDir, dest_path, symptom, symptomID, verbs):
    feq_word = {}
    feq_doc = {}
    found_word = {}

    # Read every sub-directory
    onlyDir = [ name for name in listdir(rootDir) if path.isdir(path.join(rootDir, name)) ]
    for dirname in onlyDir:
        if dirname != "00-word-vector-symps" and dirname != '01.wordlist':
            process_dir = rootDir+"/"+dirname+"/pos-stopword"

            # Read every files in each sub-directory
            onlyfiles = [f for f in listdir(process_dir) if isfile(join(process_dir, f))]
            for filename in onlyfiles:
                # print "%s processing file : %s" %(symptom, filename)
                file_path = process_dir+"/"+filename
                with open(file_path, "r") as f:
                    for line in f:
                        words_in_line = line.decode('utf-8').split("|")
                        for word in words_in_line:
                            token = word.split("/")
                            if token[1] == "V":
                                key = token[0].encode("utf-8")
                                if key in feq_word:
                                    feq_word[key] = feq_word[key] + 1
                                    found_word.update({key:1})
                                else:
                                    feq_word.update({key:1})
                                    found_word.update({key:1})

                # conclude document fequency
                # when finish reading each documents
                for key in found_word.keys():
                    if key in feq_doc:
                        feq_doc[key] = feq_doc[key] + 1
                    else:
                        feq_doc.update({key:1})

                found_word.clear()

    # Sort dictionary by value
    feq_word = sorted(feq_word.items(), key=operator.itemgetter(1), reverse=True)

    # Write word list of this symptom to CSV file
    # for calculate TF-IDF
    outfile = rootDir+"/01.wordlist/"+str(symptomID)+"-"+symptom.encode("utf-8")+".csv"
    with open(outfile, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        header = ['TH-verbs', 'EN-verbs', 'Word Fequency', 'Doc Fequency']
        wr.writerow(header)

        for fword in feq_word:
            key, value = fword[0], fword[1]
            line = [key, verbs[key], value, feq_doc[key]]
            wr.writerow(line)
    print "Word list file has been writed !!\n"


def main():
    if len(sys.argv) != 1:
        symptoms = readSymptoms()
        verbs = readVerbsDict()

        rootDir = sys.argv[1]

        symptomID = 1
        destination_dir = rootDir+"/00-word-vector-symps"
        # Create directory for store result file
        if not path.exists(destination_dir):
            makedirs(destination_dir)

        # List all file from target directory
        onlyDir = [ name for name in listdir(rootDir) if path.isdir(path.join(rootDir, name)) ]
        for symp in symptoms:
            print "#%s Processing Sysmptom : %s" %(symptomID ,symp)
            dest_path = destination_dir+"/"+str(symptomID)+"-"+symp+".csv"

            # call function
            createVector(rootDir, dest_path, symp, symptomID, verbs)
            symptomID += 1

            if symptomID > 3:
                break
    else:
        print "Please, Enter File Directory"

if __name__ == '__main__':
    main()
