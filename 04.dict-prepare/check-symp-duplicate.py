import csv

def main():
    dict_path = '/Users/phisan/Desktop/dictionary-60/symptoms.csv'
    dict_new_path = '/Users/phisan/Desktop/dictionary-60/symptoms-60.csv'

    dict_list = []

    with open(dict_path, 'r') as fd:
        for line in fd:
            symps = line.split()
            if symps not in dict_list:
                dict_list.append(symps)
            else:
                newline = "".join(symps)+"\n"
                print newline

    with open(dict_new_path, 'a') as fd:
        for symp in dict_list:
            newline = ",".join(symp)+"\n"
            fd.write(newline)
    fd.close()

    print len(dict_list)


if __name__ == '__main__':
    main()
