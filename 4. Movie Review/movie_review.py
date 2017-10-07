import re
import glob
from itertools import zip_longest
import time

### DEL 1 ###
# Lese et dokument i treningssettet fra fil, og representer som angitt i Del 1

def read_one_file(filename):
    file = open(filename,'r', encoding='utf-8')
    review = file.read()
    new_review = re.sub('[^a-åA-Å0-9]'," ",review).lower() #Fjerner bytter ut ikke godkjente tegn med " ", setter alt lower case
    word_set = set(new_review.split()) #Fjerner dublikater ved å bruke set
    try: word_set.remove("br")  #br er et ord som ligger i teksten bra <br /> som gir linjeskift i html kode, fjerner den hvis det eksisterer
    except KeyError: pass
    file.close()
    return word_set


### DEL 2 ###
# Les alle filene fra treningsettet. Analyser representasjonene slik at du finner de 25 mest populre ordene for hhv,
# positive og negetive anmeldelser
def read_all_files():
    negative_file_list = glob.glob("data/alle/train/neg/*.txt") #Liste over filene
    positive_file_list = glob.glob("data/alle/train/pos/*.txt")
    antall_positive = len(positive_file_list) #Bruk viss du vil ha sannsynlighet
    antall_negative = len(negative_file_list)
    positive_words, negative_words = {},{}
    for p_file,n_file in zip_longest(positive_file_list,negative_file_list): #Gå gjennom hver review
        pos_set = read_one_file(p_file) #Hent ordene brukt i set
        neg_set = read_one_file(n_file)
        for w_pos,w_neg in zip_longest(pos_set,neg_set): #Finn frekvens av hvert ord
            count_word(positive_words,w_pos)
            count_word(negative_words,w_neg)
    positive_words,negative_words = list(positive_words.items()),list(negative_words.items())
    positive_words.sort(key=lambda x:x[1], reverse=True),negative_words.sort(key=lambda x:x[1], reverse=True) #Sorter for å finne top 25
    return positive_words[0:25],negative_words[0:25]

def count_word(dictionary,word):
    if word not in dictionary and word is not None:
        dictionary[word] = 1
    elif word is not None:
        dictionary[word] += 1

def main():
    start = time.time()
    pos,neg = read_all_files()
    print(pos)
    print(neg)
    end = time.time()
    print((end-start)/12500)
    # liste = [(9,"hei"),(8,"nei"),(1,"nsj")]
    # liste.sort()
    # print(liste)









main()
