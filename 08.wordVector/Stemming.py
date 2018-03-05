import csv
import numpy as np

class Stemming():
    def __init__(self, input_file):
        # super(Stemming, self).__init__()
        self.input_file = input_file

    def stem(self):
        rows = csv.reader(open(self.input_file))
        line_count = 0
        term_lt = []

        for row in rows:
            if line_count > 0:
                term_lt.append([row[2], row[1]])
            line_count += 1

        term_arr = np.array(term_lt)
        term_new = []
        stem = {}
        for term in term_arr:
            # index = -1
            if term[0] not in term_new:
                term_new.append(term[0])
                stem.update({term[0]:{term[1]}})
            else:
                stem[term[0]].add(term[1])
        return stem

if __name__ == '__main__':
    in_file = "/Users/phisan/ResearchCode/OpinionMining/08.wordVector/dict/WordListVerbs-selected.csv"
    stem = Stemming(in_file)
    stemed = stem.stem()

    number = 1
    for key in stemed.keys():
        print("{} : {} : {}".format(number, key, stemed[key]))
        number += 1
