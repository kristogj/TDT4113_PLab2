from re import findall
from glob import glob
from itertools import zip_longest
from time import time
from heapq import nlargest
from math import log

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
            file_words += ["_".join(file_words[x:x+self.n_gram]) for x in range(0,len(file_words)-(self.n_gram+1))]
        return set([word for word in file_words if word not in self.stopwords])


    ### DEL 2 ###
    def read_all_traning_files(self):
        #Lag liste av alle filene
        negative_file_list,positive_file_list = glob("data/alle/train/neg/*.txt"),glob("data/alle/train/pos/*.txt")
        total_number_of_documents = len(negative_file_list) + len(positive_file_list)
        #Lag dict som skal telle frekvensen av et ord
        positive_words, negative_words, total_words = {},{},{}
        print("Reading traingingfiles...")
        for p_file,n_file in zip_longest(positive_file_list,negative_file_list): #Gå gjennom hver review
            pos_set,neg_set = self.read_one_file(p_file), self.read_one_file(n_file)
            #To for-looper er raskere enn å kjøre zip_longest her pga den store forskjellen av ord som skjer ofte
            for w_pos in pos_set: count_word(positive_words,total_words,w_pos)
            for w_neg in neg_set: count_word(negative_words,total_words,w_neg)
        # change_counter_2(positive_words,total_words,total_number_of_documents) #Finn informasjonsverdi
        # change_counter_2(negative_words,total_words,total_number_of_documents)
        prune(positive_words, total_words, len(positive_file_list))  # Finn popularitetverdi
        prune(negative_words, total_words, len(negative_file_list))
        # positive_words,negative_words = list(positive_words.items()),list(negative_words.items()) #Dict --> list of tuples
        # positive_words,negative_words = nlargest(25,positive_words,key=lambda x:x[1]),\
        #                                 nlargest(25,negative_words,key=lambda x:x[1]) #Finner de 25 mest brukte ordene
        self.pos_vocabular = positive_words
        self.neg_vocabular = negative_words

    ### Del 7 ###
    def klassifikasjonssystem(self,path):
        file_list = glob(path)
        my_pos_files,my_neg_files = [],[]
        print("Reading testfiles...")
        for file in file_list:
            _set = self.read_one_file(file)
            pos_score = 0
            neg_score = 0
            for word in _set: pos_score += get_score(self.pos_vocabular,word)
            for word in _set: neg_score += get_score(self.neg_vocabular,word)
            if pos_score > neg_score: my_pos_files.append(file)
            else: my_neg_files.append(file)
        if "pos" in path: return len(my_pos_files)/len(file_list)
        return len(my_neg_files)/len(file_list)

def get_score(vokabuler,word):
    score = 0
    try:
        score += log(vokabuler[word])
    except KeyError:
        score += log(0.005)
    return score

### DEL 3 ###
#Filterer bort stopwords i read_one_file

### DEL 4 ###
def count_word(dictionary,tot_dictionary,word):
    if word not in dictionary:
        dictionary[word] = 1
        tot_dictionary[word] = 1
    else:
        dictionary[word] += 1
        tot_dictionary[word] += 1

### DEL 5 ###
def prune(dictionary,tot_dictionary,number_of_documents):
    for word in tot_dictionary:
        try:
            if tot_dictionary[word] / number_of_documents < 0.02:
                dictionary.pop(word)
                continue
            dictionary[word] = dictionary[word]/tot_dictionary[word]
        except KeyError:
            pass

### DEL 6 ###
#n-grams lages i read_one_file



start = time()
#Lag objekt, bestem lengde n-gram
review = Review(2)
#Training
review.read_all_traning_files()
#Klassifiser
pos = review.klassifikasjonssystem("data/alle/test/pos/*.txt")
neg = review.klassifikasjonssystem("data/alle/test/neg/*.txt")
print("Resultat positive testfiler: " +  str(pos) + "%")
print("Resultat negative testfiler: " + str(neg) + "%")
end = time()
print((end-start))






