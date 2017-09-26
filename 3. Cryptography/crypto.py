
import string
import random
import crypto_utils
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

    def generate_keys(self):
        return random.randint(0,94)



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
    def generate_keys(self):
        key = random.randint(0,94)
        check = check_prev_remainder(key,95)
        while check != 1:
            key = random.randint(0,94)
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

    #Gir ikke 100% suksess
    def generate_keys(self):
        r1 = Affine.mul.generate_keys()
        r2 = random.randint(0,94)

        return [r1,r2]


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
            encode_key = random.randint(3, phi - 1)
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


class Hacker(Person):

    def __init__(self):
        pass


def main():
    melding = "https://open.spotify.com/track/02CIvwzfN65xAJaJQNhxNC"

    caesar = Caesar()
    multiplucative = Multiplicative()
    affine = Affine()
    unbreakable = Unbreakable()
    rsa = RSA()

    key_c = caesar.generate_keys()
    key_m = multiplucative.generate_keys()
    key_a = affine.generate_keys()
    key_send,key_mot = unbreakable.generate_keys("Koking")
    key_sender,key_motaker = rsa.generate_keys()

    print(Cipher.verify_1key(caesar,melding,key_c))
    print(Cipher.verify_1key(multiplucative, melding, key_m))
    print(Cipher.verify_1key(affine, melding, key_a))
    print(unbreakable.verify_2keys(melding,key_send,key_mot))
    print(rsa.verify_2keys(melding,key_sender,key_motaker))


main()
























