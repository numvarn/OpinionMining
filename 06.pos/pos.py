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

def readStopWords():
    stopwords = []
    rows = csv.reader(open("./dict/stopwords.csv", "rb"))
    for row in rows:
        stopwords.append(row[0].decode('utf-8'))
    return stopwords

def readLexitron():
    lex = []
    pos = []
    rows = csv.reader(open("./dict/lectitron-telex-utf8.csv", "rb"))
    for row in rows:
        lex.append(row[1].decode('utf-8'))
        pos.append(row[4].decode('utf-8'))
    return lex, pos

def pastOfSpeech(filepath, destination_dir, filename, stopwords, lexitron, pos, symptoms):
    # f = open(filepath+"/"+filename, 'r')
    ft = open(destination_dir+"/"+filename, 'a')

    with open(filepath+"/"+filename, 'r') as f:
        for line in f:
            newword = []
            if len(line.rstrip('\n')) > 0:
                newline = ''
                string = line.decode('utf-8')
                words = string.split("|")
                index = 0
                for word in words:
                    if word in symptoms:
                        words[index] = words[index] + "/SYMPTOM"
                    elif word in stopwords or word == "":
                        words[index] = words[index] + "/END"
                    elif word in lexitron:
                        lex_index = lexitron.index(word)
                        pos_tag = pos[lex_index]
                        words[index] = words[index] + "/" + pos_tag
                    elif not word.isspace():
                        words[index] = words[index] + "/NA"
                    else:
                        pass
                    index += 1

                if len(words) > 0:
                    newword = filter(lambda wd: not wd.isspace(), words)
                    newline = "|".join(newword)+"\n"
                    newline = newline.encode('utf-8')
                    ft.write(newline)

    f.close()
    ft.close()

def main():
    stopwords = readStopWords()
    symptoms = readSymptoms()
    lexitron, pos = readLexitron()

    if len(sys.argv) != 1:
        filedir = sys.argv[1]

        upone_level = path.dirname(filedir.rstrip('/'))
        uptwo_level = path.dirname(upone_level.rstrip('/'))
        destination_dir = uptwo_level+"/pos"

        # Create directory for store result file
        if not path.exists(destination_dir):
            makedirs(destination_dir)

        # List all file from target directory
        onlyfiles = [f for f in listdir(filedir) if isfile(join(filedir, f))]

        for filename in onlyfiles:
            if filename != '.DS_Store':
                print "Processing file : ", filename
                pastOfSpeech(filedir, destination_dir, filename, stopwords, lexitron, pos, symptoms)
    else:
        print "Please, Enter File Directory"

if __name__ == '__main__':
    main()
