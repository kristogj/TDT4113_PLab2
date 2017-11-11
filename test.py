# print([x/100 for x in range(10,80)])
import random

liste = [0.4,0.3,0.9]

start = 0
ranged = []
for weight in liste:
    weight = weight + start
    ranged.append(set(x/1000 for x in range(int(start*1000),int(weight*1000))))
    start = weight
randomm = round(random.uniform(0,sum(liste)-0.001),2)
print(randomm)

for r in range(len(ranged)):
    if randomm in ranged[r]:
        print(True,r)