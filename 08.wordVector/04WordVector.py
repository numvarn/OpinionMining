import sys
import csv
import operator
import codecs
import math
import copy
from os import listdir
from os import path
from os.path import isfile, join

class CreateWordVector():
    def __init__(self, file_path):
        super(CreateWordVector, self).__init__()
        self.file_path = file_path
        self.symptoms = []
        self.verbs = {}

    def readSymptoms(self):
        rows = csv.reader(open('./dict/symptoms-60.csv'))
        for row in rows:
            self.symptoms.append(row[0])

    def readVerbsDict(self):
        rows = csv.reader(open('./dict/telex-verb-utf8.csv'))
        count = 0
        for row in rows:
            if count > 1:
                self.verbs.update({row[0]:row[1]})
            count += 1

    def createVector(self):
        feq_word = {}
        feq_doc = {}
        found_word = {}
        idf_terms = {}
        document_count = 0

        self.readSymptoms()
        self.readVerbsDict()

        symptomID = 1

        for symp in self.symptoms:
            print('#{} Processing : {}'.format(symptomID ,symp))

            # Read every sub-directory
            onlyDir = [ name for name in listdir(rootDir) if path.isdir(path.join(rootDir, name)) ]
            dir_count = 0
            for dirname in onlyDir:
                print("\t#{}-------{}".format(symptomID, dirname))
                process_dir = rootDir+'/'+dirname+'/filtered-pos'
                if path.exists(process_dir):
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
                        with codecs.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f:
                                words_in_line = line.split('|')
                                for word in words_in_line:
                                    token = word.split('/')
                                    if len(token) >  1:
                                        if token[1] == 'SYMPTOM' and token[0] == symp:
                                            found_symptom = True
                                            print("\t\t-------{} found {}".format(filename, symp))
                                            break

                        # If founded symptem in file
                        # @Step 2
                        if found_symptom:
                            document_count += 1
                            # @Step 2
                            with open(file_path, 'r') as f:
                                for line in f:
                                    words_in_line = line.split('|')
                                    for word in words_in_line:
                                        token = word.split('/')
                                        if token[1] == 'V':
                                            key = token[0]
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

                # dir_count += 1
                # if dir_count > 10:
                #     break

            # Sort dictionary by value
            feq_word = sorted(feq_word.items(), key=operator.itemgetter(1), reverse=True)

            # --------------------------------------------------------------------------
            # Create Word-List
            # write word list of this symptom to CSV file
            # --------------------------------------------------------------------------
            # for calculate TF-IDF
            upone_level = path.dirname(rootDir.rstrip('/'))
            outfile = upone_level+'/01.wordlist/'+str(symptomID)+'-'+symp+'.csv'
            with open(outfile, 'w') as myfile:
                wr = csv.writer(myfile)
                header = ['TH-verbs', 'EN-verbs', 'Word Fequency', 'Doc Fequency', 'IDF']
                wr.writerow((header))

                for term in feq_word:
                    key, value = term[0], term[1]

                    # calculate IDF of each terms
                    # idf = log(N/df)
                    # --- N is number of all documents
                    # --- df is number of documents that found this term
                    idf = math.log10(document_count / feq_doc[key])
                    idf_terms.update({key:idf})

                    line = [key, self.verbs[key], value, feq_doc[key], idf]
                    wr.writerow(line)

            print('----- Word list file has been writed !!')

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
            upone_level = path.dirname(rootDir.rstrip('/'))
            out_vector = upone_level+'/02.vector/'+str(symptomID)+'-'+symp+'.csv'
            with open(out_vector, 'w') as myfile:
                header = copy.deepcopy(terms_list)

                header.insert(0, 'ไอดี')
                header.insert(1, 'ไฟล์')
                header.insert(2, 'ไดเรคทอรี่')
                header.insert(3, symp)

                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerow(header)

                # translate TH to EN
                header[0] = 'ID'
                header[1] = 'File'
                header[2] = 'Directory'
                header[3] = 'SYMPTOM'

                for i in range(4, len(header)):
                    header[i] = self.verbs[header[i]]

                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerow(header)

            # @Step 2 : read all file and scan only term in term_use
            file_count = 0
            onlyDir = [ name for name in listdir(rootDir) if path.isdir(path.join(rootDir, name)) ]
            for dirname in onlyDir:
                process_dir = rootDir+'/'+dirname+'/filtered-pos'
                if path.exists(process_dir):
                    # Read every files in each sub-directory
                    onlyfiles = [f for f in listdir(process_dir) if isfile(join(process_dir, f))]
                    for filename in onlyfiles:
                        file_path = process_dir+'/'+filename

                        # @Step 1
                        found_symptom = False
                        with codecs.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f:
                                words_in_line = line.split('|')
                                for word in words_in_line:
                                    token = word.split('/')
                                    if len(token) >  1:
                                        if token[1] == 'SYMPTOM' and token[0] == symp:
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
                                    words_in_line = line.split('|')
                                    for word in words_in_line:
                                        token = word.split('/')
                                        term = token[0]
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

            print('----- Word Vector file has been writed !!')

            symptomID += 1
            if symptomID > 1:
                break


if __name__ == '__main__':
    if len(sys.argv) != 1:
        rootDir = sys.argv[1]
        wordVector = CreateWordVector(rootDir)
        wordVector.createVector()
