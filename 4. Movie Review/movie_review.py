from re import sub
from glob import glob
from itertools import zip_longest
import time
from heapq import nlargest

### DEL 1 ###
# Lese et dokument i treningssettet fra fil, og representer som angitt i Del 1
def read_one_file(filename,stopwords):
    file = open(filename,'r', encoding='utf-8')
    review = file.read()
    new_review = sub('[^a-åA-Å0-9]'," ",review).lower() #Fjerner bytter ut ikke godkjente tegn med " ", setter alt lower case
    word_set = set(new_review.split()) #Fjerner dublikater ved å bruke set
    file.close()
    return set([word for word in word_set if word not in stopwords])


### DEL 2 ###
# Les alle filene fra treningsettet. Analyser representasjonene slik at du finner de 25 mest populre ordene for hhv,
# positive og negetive anmeldelser
def read_all_files():
    stopwords = get_stop_words()
    negative_file_list = glob("data/alle/train/neg/*.txt") #Liste over filene
    positive_file_list = glob("data/alle/train/pos/*.txt")
    total_number_of_documents = len(negative_file_list) + len(positive_file_list)
    positive_words, negative_words, total_words = {},{},{}
    for p_file,n_file in zip_longest(positive_file_list,negative_file_list): #Gå gjennom hver review
        pos_set = read_one_file(p_file,stopwords) #Hent ordene som er brukt i filen
        neg_set = read_one_file(n_file,stopwords)
        for w_pos,w_neg in zip_longest(pos_set,neg_set): #Finn frekvens av hvert ord
            count_word_2(positive_words,total_words,w_pos)
            count_word_2(negative_words,total_words,w_neg)

    change_counter_2(positive_words,total_words,total_number_of_documents)
    change_counter_2(negative_words,total_words,total_number_of_documents)
    positive_words,negative_words = list(positive_words.items()),list(negative_words.items())
    positive_words,negative_words = nlargest(25,positive_words,key=lambda x:x[1]),\
                                    nlargest(25,negative_words,key=lambda x:x[1]) #Finner de 25 mest brukte ordene
    return positive_words,negative_words #Returnerer egentlig bare en liste med stopp-ord

def count_word(dictionary,word): #Oppdateres i del 4
    if word not in dictionary and word is not None:
        dictionary[word] = 1
    elif word is not None:
        dictionary[word] += 1

### DEL 3 ###
#Skal brukes til å filtrere bort stop-ord i read_one_file
def get_stop_words():
    file = open("data/stop_words.txt")
    words = file.read().split()
    file.close()
    return set(words)

### DEL 4 ###
#Gjør endringer i word counteren, slik at info også lagres i den totale dictionaryen
#Bruker change_counter for å endre verdien i tuppelen til informasjonsverdien
def count_word_2(dictionary,tot_dictionary,word):
    if word not in dictionary and word is not None:
        dictionary[word] = 1
        tot_dictionary[word] = 1
    elif word is not None:
        dictionary[word] += 1
        tot_dictionary[word] += 1

def change_counter(dictionary,tot_dictionary): #Oppdateres i del 5
    for word in tot_dictionary:
        try:
            dictionary[word] = dictionary[word]/tot_dictionary[word]
        except KeyError:
            pass


### DEL 5 ###
#Fjern ord som ikke brukes mer enn en hvis prosent-andel i alle dokumente (å "prune")
def change_counter_2(dictionary,tot_dictionary,number_of_documents):
    for word in tot_dictionary:
        try:
            if tot_dictionary[word] / number_of_documents < 0.05:
                dictionary.pop(word)
                continue
            dictionary[word] = dictionary[word]/tot_dictionary[word]
        except KeyError:
            pass

### DEL 6 ###

def main():
    start = time.time()
    pos,neg = read_all_files()
    print(pos)
    print(neg)
    end = time.time()
    print((end-start))










main()
