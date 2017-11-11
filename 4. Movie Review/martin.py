import re
import os
import copy
import math

class Reader:

    def __init__(self):
        positive_words = []
        negative_words = []
        positive_path = os.listdir('data/subset/train/pos/')
        negative_path = os.listdir('data/subset/train/neg/')
        self.stop_words = set(open('data/stop_words.txt', encoding='utf-8').read().split())

        for path in positive_path:
            positive_words += self.file_to_list('data/alle/train/pos/' + path)

        for path in negative_path:
            negative_words += self.file_to_list('data/alle/train/neg/' + path)

        self.pos_words_occ = self.get_all_occurences(positive_words)
        self.neg_words_occ = self.get_all_occurences(negative_words)

        all_words = positive_words + negative_words
        print(all_words)
        self.prune(0.0001, all_words)

        self.positive_words = self.informative_words(True)
        self.negative_words = self.informative_words(False)
        #print(self.get_most_popular_words(self.positive_words))
        #print(self.get_most_popular_words(self.negative_words))
        #print(self.positive_words)



    # Del 1

    # Gjøre om en fil med tekst til en liste med ord uten spesialsymboler og duplikater
    def file_to_list(self, filename):
        text = ""
        file = open(filename, encoding ='utf-8')
        for line in file:
            text += re.sub("[.,#+()-:?!&<´>/;'^*]", "", line.lower().rstrip('\n').replace('"', '').replace("!","").replace("br ",""))

        file.close()
        words = self.n_gram(text.split())
        return list(set([word for word in words if word not in self.stop_words]))


    # Ta inn en liste med ord, og returnerer en dict med antall tilfeller av et ord
    def get_all_occurences(self, word_list):
        my_dict = {}
        for word in word_list:
            if word not in my_dict:
                my_dict[word] = 1
            else:
                my_dict[word] += 1
        return my_dict

    # Tar inn en dict, og returnerer nøklene med de 25 høyeste verdiene
    def get_most_popular_words(self, dict):
        my_dict = copy.deepcopy(dict)
        popular_words = []
        for i in range(25):
            max_key = max(my_dict, key=my_dict.get)
            my_dict[max_key] = 0
            popular_words.append(max_key)
        return popular_words

    # TRUE er positivt ord, FALSE er negativt ord
    def get_word_value(self, word, type):
        if type:
            if word in self.neg_words_occ:
                return self.pos_words_occ[word]/(self.pos_words_occ[word] + self.neg_words_occ[word])
            return 1
        else:
            if word in self.pos_words_occ:
                return self.neg_words_occ[word]/(self.neg_words_occ[word] + self.pos_words_occ[word])
            return 1

    def prune(self, percentage, words):
        total_occ = self.get_all_occurences(words)
        print(total_occ)
        for word in total_occ:
            try:
                if total_occ[word]/len(words) <= percentage:
                    self.pos_words_occ.pop(word)
            except KeyError:
                pass

            try:
                if total_occ[word]/len(words) <= percentage:
                    self.neg_words_occ.pop(word)
            except KeyError:
                pass

    def information_values(self, type):
        values = {}
        if type:
            my_dict = copy.deepcopy(self.pos_words_occ)

        else:
            my_dict = copy.deepcopy(self.neg_words_occ)

        for word in my_dict:
            values[word] = self.get_word_value(word, type)

        res = []
        for i in range(25):
            max_key = max(values, key=values.get)
            res.append(max_key)
            values[max_key] = 0
        return res

    def n_gram(self, list):
        n_list = []
        for i in range(len(list)-2):
            word1 = list[i]+"_"+list[i+1]
            word2 = list[i]+"_"+list[i+1]+"_"+list[i+2]
            n_list.append(word1)
            n_list.append(word2)

        return list+n_list

    def informative_words(self, type):
        values = {}
        if type:
            dict = self.pos_words_occ
        else:
            dict = self.neg_words_occ

        for word in dict:
            values[word] = self.get_word_value(word, type)

        return values



class Classification():

    def __init__(self):
        self.reader = Reader()


    def get_type(self, filename, e):
        file = self.reader.file_to_list(filename)
        pos_sum = 0
        neg_sum = 0

        for word in file:
            if word in self.reader.positive_words:# and word not in self.reader.negative_words:
                value = self.reader.positive_words[word]
                pos_sum += math.log(value)

            if word not in self.reader.positive_words:
                pos_sum += math.log(e)

            if word in self.reader.negative_words:
                #print(word)
                value = self.reader.negative_words[word]
                #print(value)
                neg_sum += math.log(value)

            if word not in self.reader.negative_words:
                neg_sum += math.log(e)

        return pos_sum > neg_sum


def main():

    runner = Classification()

    pos_path = os.listdir("data/subset/test/pos")
    neg_path = os.listdir("data/subset/test/neg")
    pos_files = 0
    neg_files = 0

    for file in pos_path:
        if runner.get_type("data/subset/test/pos/" + file, 0.02):
            pos_files +=1

    for file in neg_path:
        if runner.get_type("data/subset/test/neg/" + file, 0.02) == False:
            neg_files += 1



    #print(runner.get_type("data/subset/test/pos/0_10.txt",0.02))
    right_positive = pos_files/len(pos_path)
    right_negative = pos_files/len(neg_path)

    print("Riktig positive filer er " + str(right_positive))
    print("Riktig negative filer er " + str(right_negative))



main()
