import csv

def main():
    dict_path = '/Users/phisan/Desktop/dictionary-60/symptoms.csv'
    dict_check_path = '/Users/phisan/Desktop/dictionary-60/symptoms-check.csv'

    dict_list = []
    new_list = []

    with open(dict_path, 'r') as fd:
        for line in fd:
            dict_list.append(line.split())

    index = 1
    with open(dict_check_path, 'r') as fdc:
        for line in fdc:
            if line.split() not in dict_list:
                new_list.append(line.split())
                dict_list.append(line.split())
                print index, " : ", line
                index += 1
    fd.close()
    fdc.close()

    if len(new_list) > 0:
        with open(dict_path, 'a') as fd:
            for symp in new_list:
                newline = ",".join(symp)+"\n"
                fd.write(newline)
        fd.close()
    else:
        print "Have no new systom"


if __name__ == '__main__':
    main()
