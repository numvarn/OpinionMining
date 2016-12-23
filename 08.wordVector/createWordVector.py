#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os import path
from os import makedirs
from os.path import isfile, join
import sys
import csv
import operator
import math
import copy

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

def createVector(rootDir, symptom, symptomID, verbs):
    feq_word = {}
    feq_doc = {}
    found_word = {}
    idf_terms = {}
    document_count = 0

    # Read every sub-directory
    onlyDir = [ name for name in listdir(rootDir) if path.isdir(path.join(rootDir, name)) ]
    for dirname in onlyDir:
        if dirname != '00-word-vector-symps' \
                and dirname != '01.wordlist' \
                and dirname != '02.vector':
            process_dir = rootDir+'/'+dirname+'/pos-stopword'

            # Read every files in each sub-directory
            onlyfiles = [f for f in listdir(process_dir) if isfile(join(process_dir, f))]
            for filename in onlyfiles:
                file_path = process_dir+'/'+filename

                # -------------------------------------------------------------#
                # Read file in 2 step
                # Step 1 : Read file for scan Symptom keyword
                #          if found symptom keyword in file go to step 2
                # Step 2 : Read file for scan and stroe verbs keyword into
                #          word-list or bag-of-words
                # -------------------------------------------------------------#

                # @Step 1
                found_symptom = False
                with open(file_path, 'r') as f:
                    for line in f:
                        words_in_line = line.decode('utf-8').split('|')
                        for word in words_in_line:
                            token = word.split('/')
                            if token[1] == 'SYMPTOM' and token[0] == symptom:
                                found_symptom = True
                                break
                # If founded symptem in file
                # @Step 2
                if found_symptom:
                    document_count += 1
                    # @Step 2
                    with open(file_path, 'r') as f:
                        for line in f:
                            words_in_line = line.decode('utf-8').split('|')
                            for word in words_in_line:
                                token = word.split('/')
                                if token[1] == 'V':
                                    key = token[0].encode('utf-8')
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

    # --------------------------------------------------------------------------
    # Create Word-List
    # write word list of this symptom to CSV file
    # --------------------------------------------------------------------------
    # for calculate TF-IDF
    outfile = rootDir+'/01.wordlist/'+str(symptomID)+'-'+symptom.encode('utf-8')+'.csv'
    with open(outfile, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        header = ['TH-verbs', 'EN-verbs', 'Word Fequency', 'Doc Fequency', 'DF']
        wr.writerow(header)

        for term in feq_word:
            key, value = term[0], term[1]

            # calculate IDF of each terms
            # idf = log(N/df)
            # --- N is number of all documents
            # --- df is number of documents that found this term
            idf = math.log10(document_count / feq_doc[key])
            idf_terms.update({key:idf})

            line = [key, verbs[key], value, feq_doc[key], idf]
            wr.writerow(line)
    print '----- Word list file has been writed !!'

    # --------------------------------------------------------------------------
    # Create Word-Vector
    # --------------------------------------------------------------------------
    # @Step 1 : filter only term that have idf > 0
    terms_list = []
    for term in feq_word:
        key, value = term[0], term[1]
        term_idf = idf_terms[key]
        if term_idf != 0:
            terms_list.append(key)

    # Write vector to CSV file
    # write only header
    out_vector = rootDir+'/02.vector/raw-vector/'+str(symptomID)+'-'+symptom.encode('utf-8')+'.csv'
    with open(out_vector, 'wb') as myfile:
        header = copy.deepcopy(terms_list)

        header.insert(0, 'ไอดี')
        header.insert(1, 'ไฟล์')
        header.insert(2, 'ไดเรคทอรี่')
        header.insert(3, symptom.encode('utf-8'))

        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(header)

        # translate TH to EN
        header[0] = 'ID'
        header[1] = 'File'
        header[2] = 'Directory'
        header[3] = 'SYMPTOM'

        for i in range(4, len(header)):
            header[i] = verbs[header[i]]

        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(header)

    # @Step 2 : read all file and scan only term in term_use
    file_count = 0
    onlyDir = [ name for name in listdir(rootDir) if path.isdir(path.join(rootDir, name)) ]
    for dirname in onlyDir:
        if dirname != '00-word-vector-symps' and dirname != '01.wordlist' and dirname != '02.vector':
            process_dir = rootDir+'/'+dirname+'/pos-stopword'

            # Read every files in each sub-directory
            onlyfiles = [f for f in listdir(process_dir) if isfile(join(process_dir, f))]
            for filename in onlyfiles:
                file_path = process_dir+'/'+filename

                # @Step 1
                found_symptom = False
                with open(file_path, 'r') as f:
                    for line in f:
                        words_in_line = line.decode('utf-8').split('|')
                        for word in words_in_line:
                            token = word.split('/')
                            if token[1] == 'SYMPTOM' and token[0] == symptom:
                                found_symptom = True
                                break
                # If founded symptem in file
                # @Step 2
                if found_symptom:
                    # @Step 2
                    # initialize vector to get fequency of each term
                    file_count += 1
                    term_feq = [0] * len(terms_list)
                    with open(file_path, 'r') as f:
                        for line in f:
                            words_in_line = line.decode('utf-8').split('|')
                            for word in words_in_line:
                                token = word.split('/')
                                term = token[0].encode('utf-8')
                                if term in terms_list:
                                    term_index = terms_list.index(term)
                                    term_feq[term_index] += 1

                    # write data to CSV when finished reading each file
                    term_feq.insert(0, file_count)
                    term_feq.insert(1, filename)
                    term_feq.insert(2, dirname)
                    term_feq.insert(3, 1)

                    with open(out_vector, 'a') as myfile:
                        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                        wr.writerow(term_feq)
    print '----- Word Vector file has been writed !!'
def main():
    if len(sys.argv) != 1:
        symptoms = readSymptoms()
        verbs = readVerbsDict()

        rootDir = sys.argv[1]

        symptomID = 0

        # for test
        # symptomID = 16
        # print '\n#%s Processing Sysmptom : %s' %(symptomID ,symptoms[symptomID])
        # createVector(rootDir, symptoms[symptomID], symptomID, verbs)


        for symp in symptoms:
            print '#%s Processing Sysmptom : %s' %(symptomID ,symp)

            # call function
            createVector(rootDir, symp, symptomID, verbs)
            symptomID += 1

            if symptomID > 100:
                break
    else:
        print 'Please, Enter File Directory'

if __name__ == '__main__':
    main()
