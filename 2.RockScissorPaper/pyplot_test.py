import matplotlib.pyplot as plt


def rett_line():
    plt.plot([1, 2, 3, 4])
    plt.ylabel("Numbers")
    plt.show()

def punkter():
    plt.plot([1,2,3,4],[1,4,9,16],'ro') #Første liste er x akse, mens neste er yakse. 'ro' betyr bare at det er punkter. -b er standard og er en blå linje
    plt.axis([0,6,0,20]) #[xmin,xmax,ymin,ymax]
    plt.show()

def main():
    punkter()



main()