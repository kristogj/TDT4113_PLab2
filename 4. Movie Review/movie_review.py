from re import findall
from glob import glob
from itertools import zip_longest
import time
from heapq import nlargest

class Review():

    def __init__(self,n_gram):
        stop_file = open("data/stop_words.txt","r",encoding="utf-8")
        stop_str = stop_file.read().lower()
        stop_file.close()
        self.stopwords = set(findall(r"[\w][\w]*'?[\w][\w]",stop_str))
        self.n_gram = n_gram


    ### DEL 1 ###
    # Lese et dokument i treningssettet fra fil, og representer som angitt i Del 1
    def read_one_file(self,filename):
        file = open(filename,'r', encoding='utf-8')
        review = file.read().lower()
        file.close()
        file_words = findall(r"[\w][\w]*'?´?[\w][\w]",review)
        if self.n_gram >0:
            file_words = file_words + ["_".join(file_words[x:x+self.n_gram]) for x in range(0,len(file_words)-(self.n_gram+1))]
        return set([word for word in file_words if word not in self.stopwords])


    ### DEL 2 ###
    # Les alle filene fra treningsettet. Analyser representasjonene slik at du finner de 25 mest populre ordene for hhv,
    # positive og negetive anmeldelser
    def read_all_files(self):
        #Lag liste av alle filene
        negative_file_list,positive_file_list = glob("data/alle/train/neg/*.txt"),glob("data/alle/train/pos/*.txt")
        total_number_of_documents = len(negative_file_list) + len(positive_file_list)
        #Lag dict som skal telle frekvensen av et ord
        positive_words, negative_words, total_words = {},{},{}
        for p_file,n_file in zip_longest(positive_file_list,negative_file_list): #Gå gjennom hver review
            pos_set,neg_set = self.read_one_file(p_file), self.read_one_file(n_file)
            #To for-looper er raskere enn å kjøre zip_longest her pga den store forskjellen av ord som skjer ofte
            for w_pos in pos_set: count_word_2(positive_words,total_words,w_pos)
            for w_neg in neg_set: count_word_2(negative_words,total_words,w_neg)
        change_counter_2(positive_words,total_words,total_number_of_documents) #Finn info
        change_counter_2(negative_words,total_words,total_number_of_documents)
        positive_words,negative_words = list(positive_words.items()),list(negative_words.items()) #Dict --> list of tuples
        positive_words,negative_words = nlargest(25,positive_words,key=lambda x:x[1]),\
                                        nlargest(25,negative_words,key=lambda x:x[1]) #Finner de 25 mest brukte ordene
        return positive_words,negative_words


### DEL 3 ###
#Skal brukes til å filtrere bort stop-ord i read_one_file
#La inn stopwords i read_one_file

### DEL 4 ###
#Gjør endringer i word counteren, slik at info også lagres i den totale dictionaryen
#Bruker change_counter for å endre verdien i tuppelen til informasjonsverdien
def count_word_2(dictionary,tot_dictionary,word):
    if word not in dictionary:
        dictionary[word] = 1
        tot_dictionary[word] = 1
    else:
        dictionary[word] += 1
        tot_dictionary[word] += 1

### DEL 5 ###
#Fjern ord som ikke brukes mer enn en hvis prosent-andel i alle dokumente (å "prune")
#Med pruning
def change_counter_2(dictionary,tot_dictionary,number_of_documents):
    for word in tot_dictionary:
        try:
            if tot_dictionary[word] / number_of_documents < 0.05:
                dictionary.pop(word)
                continue
            dictionary[word] = round(dictionary[word]/tot_dictionary[word],4)
        except KeyError:
            pass

### DEL 6 ###
#Lag n-grams
#La inn i read_one_file











start = time.time()
review = Review(2)
pos,neg = review.read_all_files()
print(pos)
print(neg)
end = time.time()
print((end-start))






