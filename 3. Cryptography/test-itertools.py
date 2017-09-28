from itertools import permutations

def main():
    letters = ['a','b','c','d']
    print(permutations(letters,4))
    print (["".join(a) for a in permutations(letters, 4)])
main()