def main():
    husk = 2
    historie = [2,0,1,2,0,7,2,0,1,2,0,1,2]

    sub_sekvens = historie[-husk:] #[1,2]
    score = [0, 0, 0]  # Mest vanlig etter sub_sekvens
    index = -1




    for x in range(len(historie) - 1 - len(sub_sekvens), -1, -1): #OK
        if historie[x] == sub_sekvens[-1]:
            for y in range(x,x - len(sub_sekvens),-1):
                if x-len(sub_sekvens) < 0:
                    break
                if historie[y-len(sub_sekvens)+1:y+1] != sub_sekvens:
                    break
                score[historie[y+1]] += 1
                index-=1
            index = -1
    print(score)


main()