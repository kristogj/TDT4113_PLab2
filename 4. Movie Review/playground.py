from re import findall
from nltk import ngrams

# file = open("data/stop_words.txt","r",encoding="utf-8")
# str = file.read().lower()
# file.close()
# l = set(findall(r"[\w][\w]*'?[\w][\w]",str))

# print(l)


#Uten pruning
def change_counter(dictionary,tot_dictionary): #Oppdateres i del 5
    for word in tot_dictionary:
        try:
            dictionary[word] = round(dictionary[word]/tot_dictionary[word],4)
        except KeyError:
            pass


def count_word(dictionary,word): #Oppdateres i del 4
    if word not in dictionary and word is not None:
        dictionary[word] = 1
    elif word is not None:
        dictionary[word] += 1


liste = ["hie","nen","nnd"]
print(ngrams(liste,2))
