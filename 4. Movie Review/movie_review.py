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
        file_words = findall(r"[\w][\w]*'?[\w][\w]",review)
        if self.n_gram >0:
            file_words += ["_".join(file_words[x:x+self.n_gram]) for x in range(0,len(file_words)-(self.n_gram+1))]
        return set([word for word in file_words if word not in self.stopwords])


    ### DEL 2 ###
    def read_all_traning_files(self,positive_file_list,negative_file_list):
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
        prune(positive_words, total_words, len(positive_file_list))  # Finn popularitetverdi, kansje mer riktig
        prune(negative_words, total_words, len(negative_file_list))  #å sende in total_number_of_documents
        self.pos_vocabular = positive_words
        self.neg_vocabular = negative_words

    def get_top_25(self):
        pos_words, neg_words = dict(self.pos_vocabular), dict(self.neg_vocabular)
        pos_words, neg_words = list(pos_words.items()),list(neg_words.items())
        pos_words, neg_words = nlargest(25,pos_words,key=lambda x:x[1]),nlargest(25,neg_words,key=lambda x:x[1])
        return pos_words,neg_words

    ### Del 7 ###
    def klassifikasjonssystem(self,file_list):
        my_pos_files,my_neg_files = [],[]
        print("Reading testfiles...")
        for file in file_list:
            _set = self.read_one_file(file)
            pos_score,neg_score = 0,0
            for word in _set:
                pos_score += get_score(self.pos_vocabular,word)
                neg_score += get_score(self.neg_vocabular,word)
            if pos_score > neg_score: my_pos_files.append(file)
            else: my_neg_files.append(file)
        if "pos" in file_list[0]: return len(my_pos_files)/len(file_list)
        return len(my_neg_files)/len(file_list)

def get_score(vokabuler,word):
    try:
        return log(vokabuler[word])
    except KeyError:
        return log(0.01)


### DEL 3 ###
#Filterer bort stopwords i read_one_file

### DEL 4 ###
def count_word(dictionary,tot_dictionary,word):
    if word not in dictionary:
        dictionary[word], tot_dictionary[word] = 1,1
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
negative_training_list = glob("data/alle/train/neg/*.txt")
positive_traning_list = glob("data/alle/train/pos/*.txt")
neg_test_list = glob("data/alle/test/neg/*.txt")
pos_test_list = glob("data/alle/test/pos/*.txt")
#Lag objekt, bestem lengde n-gram
review = Review(2)
#Training
review.read_all_traning_files(positive_traning_list,negative_training_list)
top_25_pos,top_25_neg = review.get_top_25()
print(top_25_pos)
print(top_25_neg)
#Klassifiser
pos = review.klassifikasjonssystem(pos_test_list)
neg = review.klassifikasjonssystem(neg_test_list)
print("Resultat positive testfiler: " +  str(round(pos*100,2)) + "%")
print("Resultat negative testfiler: " + str(round(neg*100,2)) + "%")
print("Total: " + str(round(((pos+neg)/2)*100,2)) + "%")
end = time()
print(str((end-start)) + " sek")






