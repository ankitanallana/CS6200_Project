from __future__ import division
from bs4 import BeautifulSoup
import os

case_folding = True
punctuation_handing = True


def remove_full_stop(w):
    w = w.replace(". "," ")
    w = w.replace(", "," ")
    w = w.replace(",\n","\n")
    w = w.replace(".\n","\n")
    return w


def to_lower_case(w):
    return w.lower()


def remove_special_characters(word):
    word = word.replace("(", "")
    word = word.replace(")", "")
    word = word.replace("'", "")
    word = word.replace('"', "")
    word = word.replace('.', "")
    word = word.replace(':', "")
    word = word.replace(";", "")
    word = word.replace("/", "")
    word = word.replace("$", "")
    word = word.replace("%", "")
    word = word.replace(",", "")
    word = word.replace("[","")
    word = word.replace("]","")
    word = word.replace("&","")
    word = word.replace("~","")
    word = word.replace("*","")
    word = word.replace("!","")
    word = word.replace("+","")
    word = word.replace("-","")
    word = word.replace("|","")
    word = word.replace("{","")
    word = word.replace("}","")
    word = word.replace("%","")
    return word


def tokenization(w):
    if case_folding:
        w = to_lower_case(w)
    if punctuation_handing:
        w = remove_special_characters(w)
    w = remove_full_stop(w)
    w = ''.join([i for i in w if not i.isdigit()])
    return w

def make_corpus(path_to_data_dir,path_to_new_dir):
    for x in range(os.listdir(path_to_data_dir).__len__()):
        with open(path_to_data_dir + "/"+ os.listdir(path_to_data_dir)[x], 'r') as f:
            soup = BeautifulSoup(f.read(), 'html')
            a = ' '.join(tokenization(soup.text).split())

            completeName = os.path.join(path_to_new_dir, os.listdir(path_to_data_dir)[x])
            file1 = open( completeName, "w")
            file1.write(a)
            file1.close()


def main(path_to_data_dir,path_to_new_dir):
    os.mkdir(path_to_new_dir)
    make_corpus(path_to_data_dir,path_to_new_dir)
    return path_to_new_dir + "/"

