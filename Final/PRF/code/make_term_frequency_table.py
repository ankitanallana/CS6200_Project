from __future__ import division
import sys,math, heapq, os,time


def open_file(file):
    f = open(file, "r")    ## Open the file with read only permit
    temp = f.readlines()    ## The variable "temp" is a list containing all lines
    f.close()     ## close the file after reading the lines.
    return temp


def find_ngrams(input_list, n):
    if n == 1:
        return input_list
    return zip(*[input_list[i:] for i in range(n)])


def main(list,file_path):
    """

    :param list: list with top k documents names
    :param file_path: path to stemmed corpus
    :return: temp2: list with most cooccured terms
    """

    print len(list)
    temp = []
    ngram =1
    for x in range(len(list)):
            with open(str(file_path) + str(list[x]), 'r') as f:
                for line in f:
                    list1 = []
                    list2 = []
                    for word in line.split():
                        temp.append(word)
                    a = find_ngrams(temp, ngram)
                    for y in range(len(a)):
                        if list1.__contains__(a[y]):
                            list2[list1.index(a[y])] += 1
                        else:
                            list1.append(a[y])
                            list2.append(1)

    outF = open("term_frequency_table_" +str(ngram) +"_ngram.txt", "w")
    a = heapq._nlargest(len(list2), zip(list2, list1))
    b = heapq._nsmallest(len(list2), zip(list2, list1))
    for l in a:
        outF.write(str(l))
        outF.write("\n")
    outF.close()
    temp2 = []
    for x in range(0,len(b)):
        temp2.append(b.pop()[1])
    return temp2
