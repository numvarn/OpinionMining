#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path, listdir, makedirs
from os.path import isfile, join
import sys
import csv
import math

def readSymptoms():
    symptoms = []
    rows = csv.reader(open('./dict/symptoms-60.csv', 'rb'))
    for row in rows:
        symptoms.append(row[0].decode('utf-8'))
    return symptoms

def readVerbsDict():
    verbs = {}
    rows = csv.reader(open('./dict/telex-verb-utf8.csv', 'rb'))
    count = 0
    for row in rows:
        if count > 1:
            verbs.update({row[0]:row[1]})
        count += 1
    return verbs

def main():
    src_dir = "/Volumes/Sirikanlaya/rawData/haamor.com/filtered-pos"

    symptoms = readSymptoms()
    verbs = readVerbsDict()

    total_documents = 0
    symptoms_feq = [0] * len(symptoms)
    document_feq = [0] * len(symptoms)
    term_idf = [0] * len(symptoms)

    files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]
    file_count = 0
    for filename in files:
        total_documents += 1
        file_path = src_dir+"/"+filename
        with open(file_path, 'r') as f:
            founded_symptom = []
            for line in f:
                words_in_line = line.decode('utf-8').split('|')
                for word in words_in_line:
                    token = word.split('/')
                    if token[1] == 'SYMPTOM':
                        symp_index = symptoms.index(token[0])
                        symptoms_feq[symp_index] += 1
                        if symp_index not in founded_symptom:
                            founded_symptom.append(symp_index)

        for i in founded_symptom:
            document_feq[i] += 1

        print("#{} : {}".format(file_count, filename))
        file_count += 1
        
        # if file_count > 20:
        #     break

    # Calculate IDF value
    for i in range(0, len(symptoms)):
        if document_feq[i] > 0:
            term_idf[i] = math.log10(total_documents / document_feq[i])
        else:
            term_idf[i] = 0

    # Write wordlist to CSV file
    outfile = '/Users/phisanshukkhi/Desktop/research_result/WordListSymptoms.csv'
    header = ['ID', 'Symptom', 'Word Fequency', 'Doc Fequency', 'IDF']
    with open(outfile, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(header)

        for i in range(0, len(symptoms)):
            line = [i+1, \
                    symptoms[i].encode('utf-8'), \
                    symptoms_feq[i], \
                    document_feq[i], \
                    term_idf[i]]

            wr.writerow(line)

if __name__ == '__main__':
    main()
