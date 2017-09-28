from bisect import bisect_left

def bi_contains(lst,item):
    return (item <= lst[-1]) and (lst[bisect_left(lst,item)] == item)

def main():
    liste = [1,2,3,4,5,6,7,8,9]
    liste2 = ['ab','ac','an']
    print(bi_contains(liste2,'ab'))
    print([x for x in range(0,95)])

main()

