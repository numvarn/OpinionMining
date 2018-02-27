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
    verbs_th = []
    verbs_eng = []
    rows = csv.reader(open('./dict/telex-verb-utf8.csv', 'rb'))
    count = 0
    for row in rows:
        if count > 1:
            verbs_th.append(row[0])
            verbs_eng.append(row[1])
        count += 1
    return verbs_th, verbs_eng

def main():
    src_dir = "/Volumes/Sirikanlaya/rawData/haamor.com/filtered-pos"

    symptoms = readSymptoms()
    verbs_th, verbs_eng = readVerbsDict()

    total_documents = 0
    verbs_feq = [0] * len(verbs_th)
    document_feq = [0] * len(verbs_th)
    term_idf = [0] * len(verbs_th)

    files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]
    file_count = 0
    for filename in files:
        total_documents += 1
        file_path = src_dir+"/"+filename
        with open(file_path, 'r') as f:
            founded_verbs = []
            for line in f:
                words_in_line = line.decode('utf-8').split('|')
                for word in words_in_line:
                    token = word.split('/')
                    if token[1] == 'V' and token[0].encode('utf-8') in verbs_th:
                        verbs_index = verbs_th.index(token[0].encode('utf-8'))
                        verbs_feq[verbs_index] += 1
                        if verbs_index not in founded_verbs:
                            founded_verbs.append(verbs_index)

        for i in founded_verbs:
            document_feq[i] += 1

        print("#{} : {}".format(file_count, filename))
        file_count += 1

        # if file_count > 20:
        #     break

    # Calculate IDF value
    for i in range(0, len(verbs_th)):
        if document_feq[i] > 0:
            term_idf[i] = math.log10(total_documents / document_feq[i])
        else:
            term_idf[i] = 0

    # Write wordlist to CSV file
    outfile = '/Users/phisanshukkhi/Desktop/research_result/WordListVerbs.csv'
    header = ['ID', 'TH-verbs', 'EN-verbs', 'Word Fequency', 'Doc Fequency', 'IDF']
    with open(outfile, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(header)

        for i in range(0, len(verbs_th)):
            line = [i+1, \
                    verbs_th[i], \
                    verbs_eng[i], \
                    verbs_feq[i], \
                    document_feq[i], \
                    term_idf[i]]

            wr.writerow(line)


if __name__ == '__main__':
    main()
