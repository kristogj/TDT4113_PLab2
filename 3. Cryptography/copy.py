# def decode_bruteforce(self, encode_text, cipher, lengde=None):
#     self.cipher = cipher
#     rang = cipher.possible_keys(lengde)
#     c = 0
#     if isinstance(cipher, Unbreakable):
#         status, answer = self.check_prevused_keys(encode_text)
#         if status: return answer
#     for key in rang:
#         self.set_key(key)
#         decoded = self.operate_cipher(encode_text).lower()
#         decoded_words = decoded.split()
#         count = 0
#         maks = 1
#         approx = []
#
#         if all(check(word) for word in decoded_words):
#
#         for word in decoded_words:
#             check = self.bi_search(word)
#             if check:
#                 count += 1
#         if count == len(decoded_words) and (decoded_words != []):
#             if isinstance(cipher, Unbreakable):
#                 file = open("prev_keys.txt", "a")
#                 file.write("\n" + key), file.close()
#             return decoded
#         else:
#             if count >= maks:
#                 maks = count
#                 approx.append(decoded)
#             count = 0
#
#         if c % 1500 == 0:
#             print("Loading...")
#         c += 1
#     return "Bruteforce failed, some possible answers: " + str(approx)