from random import randint
import crypto_utils
#from bisect import bisect_left
from itertools import product
#************ CIPHER SUPERKLASSE ************

class Cipher():

    #Klassevariabel - Lovlige tegn
    tegn = " !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

    def encode(self,klar_text,key):
        str = ""
        for letter in klar_text:
            old_index = Cipher.tegn.index(letter)
            new_index = (old_index + key) % 95
            str += Cipher.tegn[new_index]
        return str

    def decode(self,cipher_text,key):
        return Cipher.encode(self,cipher_text,95 - key)


    def verify_1key(self,text,key):
        encode = self.encode(text,key)
        decode = self.decode(encode,key)
        return text == decode

    def verify_2keys(self,text,key_e,key_d):
        encode = self.encode(text,key_e)
        decode = self.decode(encode,key_d)
        return text == decode

    def generate_keys(self,key=None):
        if key == None:
            return randint(0,94)
        return key

    def possible_keys(self,lengde):
        return [x for x in range(0,95)]



# ************ CIPHER SUB-KLASSE ************


class Caesar(Cipher):

    #Metodene definert i superklassen
    def encode(self,klar_text,key):
        return Cipher.encode(self,klar_text,key)

    def decode(self,cipher_text,key):
        return Cipher.decode(self,cipher_text,key)

class Multiplicative(Cipher):


    def encode(self,klar_text,key):
        str = ""
        for letter in klar_text:
            old_index = Cipher.tegn.index(letter)
            new_index = (old_index * key) % 95
            str += Cipher.tegn[new_index]
        return str

    def decode(self,cipher_text,key):
        new_key = crypto_utils.modular_inverse(key,95)
        return self.encode(cipher_text,new_key)

    #Lager egen metode fordi vi krever remainder lik 1 for at modular_inversen skal bli riktig
    def generate_keys(self,key=None):
        if key == None:
            key = randint(0,94)
        check = check_prev_remainder(key,95)
        while check != 1:
            key = randint(0,94)
            check = check_prev_remainder(key,95)
        return key



class Affine(Cipher):
    #En kombinasjon av Caesar og Multiplikativ

    #Klassevariabler - felles for alle instanser
    mul = Multiplicative()
    cae = Caesar()

    def encode(self,klar_text,key):
        encode_multi = Affine.mul.encode(klar_text,key[0])
        return Affine.cae.encode(encode_multi,key[1])


    def decode(self,cipher_text,key):
        decode_caesar = Affine.cae.decode(cipher_text,key[1])
        return Affine.mul.decode(decode_caesar,key[0])

    def generate_keys(self,key1=None,key2=None):
        if key1 == None and key2 == None:
            key1 = Affine.mul.generate_keys()
            key2 = randint(0,94)
        return (key1,key2)

    def possible_keys(self,lengde):
        return [(x,y) for x in range(0,95) for y in range(0,95)]


class Unbreakable(Cipher):

    def encode(self,klar_text,key):
        # (letter_index + key_letter_index) % 95
        counter = 0
        str = ""
        for letter in klar_text:
            letter_index = Cipher.tegn.index(letter)
            key_letter_index = Cipher.tegn.index(key[counter % len(key)])
            new_index = (letter_index + key_letter_index) % 95
            str += Cipher.tegn[new_index]
            counter+=1
        return str

    def decode(self,cipher_text,key):
        return self.encode(cipher_text,key)


    def generate_keys(self,sender_key):
        receiver_key = inverted_key(sender_key)
        return sender_key,receiver_key

    #IKKE SEND INN FOR HØY LENGDE
    def possible_keys(self,lengde):
        return ["".join(a) for a in product(Cipher.tegn,repeat=lengde)]



#STATIC HJELPEFUNKSJON
def inverted_key(old):
    new = ""
    for letter in old:
        new += Cipher.tegn[(95 - Cipher.tegn.index(letter)) % 95]
    return new

class RSA(Cipher):


    def encode(self,klar_text,key):
        blocks = crypto_utils.blocks_from_text(klar_text,2)
        new_blocks = []
        for block in blocks:
            new_blocks.append(encode_integer(block,key))
        return new_blocks

    def decode(self,cipher_text_blocks,key):
        new_blocks = []
        for block in cipher_text_blocks:
            new_blocks.append(decode_integer(block,key))
        return crypto_utils.text_from_blocks(new_blocks,2)


    def generate_keys(self):
        p,q = 0,0
        check_keys = -1

        while p==q or check_keys != 1:
            p = crypto_utils.generate_random_prime(8)
            q = crypto_utils.generate_random_prime(8)
            phi = (p - 1) * (q - 1)
            encode_key = randint(3, phi - 1)
            check_keys = check_prev_remainder(encode_key,phi)
        n = p * q
        decode_key = crypto_utils.modular_inverse(encode_key, phi)

        #(n,e) brukes av sender, (n,d) brukes av mottaker
        #(n,e) offentlig, (n,d) er hemmelig og beholdes av mottaker
        return (n,encode_key),(n,decode_key)

#STATIC HJELPEMETODER
def encode_integer(integer,key):
    n,encode_key = key
    return pow(integer,encode_key,n)

def decode_integer(encode_integer,key):
    n,decode_key = key
    return pow(encode_integer,decode_key,n) % n

def check_prev_remainder(_a, _b):
    previous_remainder, remainder = _a, _b
    current_x, previous_x, current_y, previous_y = 0, 1, 1, 0
    while remainder > 0:
        previous_remainder, (quotient, remainder) = remainder, divmod(previous_remainder, remainder)
        current_x, previous_x = previous_x - quotient * current_x, current_x
        current_y, previous_y = previous_y - quotient * current_y, current_y
    return previous_remainder

#************ Person SUPERKLASSE ************

class Person():

    def __init__(self,key,cipher):
        self.__key = key
        self.cipher = cipher

    def set_key(self,key):
        self.__key = key

    def get_key(self):
        return self.__key



#************ Person SUB-KLASSER ************

class Sender(Person):

    def __init__(self,key,cipher):
        Person.__init__(self,key,cipher)

    #Generer cipher tekst
    def operate_cipher(self,klar_text):
        return self.cipher.encode(klar_text,self.get_key())


class Receiver(Person):

    def __init__(self,key,cipher):
        Person.__init__(self,key,cipher)

    #Generer klar tekst
    def operate_cipher(self,cipher_text):
        return self.cipher.decode(cipher_text,self.get_key())


class Hacker(Receiver):

    def __init__(self,dictionary):
        file = open(dictionary,"r")
        read = file.read()
        self.words = set(read.split("\n"))
        file.close()

    #Siden jeg bruker set vil søketiden være O(1)
    def bi_search(self,word):
        #(word <= self.words[-1]) and (self.words[bisect_left(self.words,word)] == word) (Binærsøk)
        return word in self.words

    #Caesar OK
    #Multiplicative OK
    #Affine OK
    #Unbreakable OK //må sende inn lengde på key for å kunne lage alle mulige kombinasjoner av lengden
    #IKKE SEND INN FOR HØY LENGDE! Lengde 4 tilsvarer 95^4 = 81.450.625 forskjellige kombinasjoner som alt lagres i en liste
    #Ved Unbreakable velger jeg å genrere alle mulige keys av en viss lengde, sjekker først alle keys som er gyldige ord
    #før den deretter går videre på strenger av den gitte lengden.
    #Det er ikke nødvendig å generere alle de stringsene, holder å teste ord fra ordlisten som key for unbreakable
    def decode_bruteforce(self,encode_text,cipher,lengde=None):
        self.cipher = cipher
        c = 0
        possible_answer = []
        if isinstance(cipher,Unbreakable):
            status,answer = self.check_prevused_keys(encode_text,lengde)
            if status:possible_answer.append(answer)

        rang = cipher.possible_keys(lengde)
        for key in rang:
            self.set_key(key)
            decoded = self.operate_cipher(encode_text).lower()
            decoded_words = decoded.split()
            print(decoded)
            if all(self.bi_search(word) for word in decoded_words) and decoded_words != []:
                if isinstance(cipher, Unbreakable):
                    file = open("prev_keys.txt","a")
                    file.write("\n"+key),file.close()
                possible_answer.append((decoded,key))
            # if c%1500==0:
            #     print("Loading...")
            # c+=1
        return possible_answer

    def check_prevused_keys(self,encoded_text,lengde):
        file = open("prev_keys.txt","r")
        read = [x for x in file.read().split("\n") if len(x) == lengde]

        for key in read:
            self.set_key(key)
            decoded = self.operate_cipher(encoded_text).lower()
            decoded_words = decoded.split()
            if all(self.bi_search(word) for word in decoded_words):
                file.close()
                return (True,decoded)
        file.close()
        return (False,"x")

def main():
    melding = "Hello"
    caesar = Caesar()
    multiplucative = Multiplicative()
    affine = Affine()
    unbreakable = Unbreakable()
    rsa = RSA()

    key_c = caesar.generate_keys()
    key_m = multiplucative.generate_keys()
    key_a = affine.generate_keys()
    key_send,key_mot = unbreakable.generate_keys("faj")
    key_sender,key_motaker = rsa.generate_keys()

    # print("Caesar: ")
    # enc_c = caesar.encode(melding,key_c)
    # dec_c = caesar.decode(enc_c,key_c)
    # print(enc_c + "\n" + dec_c + "\n")
    #
    #
    # print("Multi: ")
    # enc_m = multiplucative.encode(melding, key_m)
    # dec_m = multiplucative.decode(enc_m, key_m)
    # print(enc_m + "\n" + dec_m + "\n")


    print("Affine: ")
    enc_a = affine.encode(melding, key_a)
    dec_a = affine.decode(enc_a, key_a)
    print(enc_a + "\n" + dec_a + "\n")


    # print("Unbreakable: ")
    # enc_u = unbreakable.encode(melding, key_send)
    # dec_u = unbreakable.decode(enc_u, key_mot)
    # print(enc_u + "\n" + dec_u + "\n")
    #
    #
    # print("RSA: ")
    # enc_r = rsa.encode(melding, key_sender)
    # dec_r = rsa.decode(enc_r, key_motaker)
    # print(str(enc_r) + "\n" + dec_r + "\n")

    print("Hacker: ")
    hacker = Hacker("english-text.txt")
    # print("CaesarHack: " + str(hacker.decode_bruteforce(enc_c,caesar)))
    # print("MultiHack: " + str(hacker.decode_bruteforce(enc_m,multiplucative)))
    print("AffineHack: " + str(hacker.decode_bruteforce(enc_a,affine)))
    # print("UnbreakableHack: " + str(hacker.decode_bruteforce(enc_u,unbreakable,3))) #lengde




main()
























