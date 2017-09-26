#Stein Saks Papir

import random
import matplotlib.pyplot as plt

#****************SPILLER SUPERCLASS****************
class Spiller():

    #Dictionary som holder info om spillerenes trekk, antar at alle kampene til motstanderen er kjent
    #også de som er mot andre motstandere enn deg selv
    #Struktur: {spiller1:[trekk1,trekk2,trekk3,trekk4...],spiller2:[trekk1...]}
    spiller_info = {}
    #Holder aksjonsverdien
    _trekk = {0:"Stein",1:"Saks",2:"Papir"}

    def __init__(self,spillernavn):
        self.name = spillernavn
        Spiller.spiller_info[self] = []

    #Returnerer hva spilleren velger. Stein saks eller papir
    def velg_aksjon(self):
        return

    #Skal motta hva resultatet på et enkelt spill ble
    #Skal legge til i Historie og Mest Vanlig
    def motta_resultat(self,motstander,trekk):
        Spiller.spiller_info[motstander].append(trekk)

    #Skal returnere navnet, slik at det kan rapporteres i grensesnittet
    def oppgi_navn(self):
        return self.spillernavn

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

#****************TILFELDIG CLASS****************
class Tilfeldig(Spiller):
    def __init__(self,name):
        Spiller.__init__(self,name)

    def velg_aksjon(self,motstander):
        return Aksjon(random.randint(0,2))


#****************SEKVENSIELL CLASS****************
class Sekvensiell(Spiller):
    def __init__(self,name):
        Spiller.__init__(self,name)
        self.i = 0

    def velg_aksjon(self,motstander):
        aksjon = Aksjon(self.i%3)
        self.i+=1
        return aksjon



# ****************MESTVANLIG CLASS****************
class MestVanlig(Spiller):
    def __init__(self,name):
        Spiller.__init__(self,name)

    #Ser på det mest brukte trekket til motstanderen
    #Hvis ingen trekk returner random
    #Hvis like mange, velges det tidligste trekket av [stein,saks,papir]
    def velg_aksjon(self,motstander):
        motstander_trekk = Spiller.spiller_info[motstander]
        if len(motstander_trekk) == 0:
            return Aksjon(random.randint(0,2))
        stein = motstander_trekk.count(Aksjon(0))
        saks = motstander_trekk.count(Aksjon(1))
        papir = motstander_trekk.count(Aksjon(2))
        liste = [stein,saks,papir]
        max_index = liste.index(max(liste)) #Finner index til trekket med høyest frekvens
        return Aksjon(motsatte(self,max_index))


#****************HISTORIKER CLASS****************
class Historiker(Spiller):
    def __init__(self,name,husk):
        Spiller.__init__(self,name)
        self.husk = husk

    def velg_aksjon(self,motstander):
        historie = Spiller.spiller_info[motstander]
        sub_sekvens = historie[-self.husk:]
        score = [0,0,0] #Mest vanlig trekk etter sub_sekvens
        for x in range(len(historie) - 1 - len(sub_sekvens),-1,-1): #-len(sub) pga man trenger ikke regne med siste trekk
            if historie[x] == sub_sekvens[-1]:
                if x - len(sub_sekvens) < 0:
                    break
                if historie[x - len(sub_sekvens) + 1:x + 1] != sub_sekvens:
                    break
                score[historie[x + 1].get_value()] += 1
        valg = motsatte(self,score.index(max(score)))
        return Aksjon(valg)



#****************AKSJON CLASS****************
class Aksjon:

    def __init__(self,num):
        #0 = Stein, 1 = Saks, 2 = papir
        self.aksjon = num

    def __eq__(self, a2):
        return a2.aksjon == self.aksjon

    def __gt__(self, a2):
        a = {0:2,1:0,2:1}
        return a[self.aksjon] != a2.aksjon

    def get_value(self):
        return self.aksjon

    def __repr__(self):
        return Spiller._trekk[self.aksjon]

    def __str__(self):
        return Spiller._trekk[self.aksjon]




# ****************ENKELTSPILL CLASS****************
#Setter opp en enkelt kamp
class EnkeltSpill:

    def __init__(self,spiller1,spiller2):
        self.s1 = spiller1
        self.s2 = spiller2
        #Poeng
        self.ps1 = 0
        self.ps2 = 0

    #Utfører spillet mellom spiller 1 og 2
    #Spørr hver spiller om deres valg
    #Bestem resultat. 1 poeng til vinner, 0 til taper. 0.5 til hver ved uavgjort
    #Rapporter valgene og resultatene tilbake til spiller
    def gjennomfør_spill(self):
        self.a1 = self.s1.velg_aksjon(self.s2)
        self.a2 = self.s2.velg_aksjon(self.s1)
        if self.a1 == self.a2:
            self.ps1,self.ps2 = 0.5,0.5
        elif self.a1 > self.a2:
            self.ps1,self.ps2 = 1,0
        else:
            self.ps1,self.ps2 = 0,1

        self.s1.motta_resultat(self.s2, self.a2)
        self.s2.motta_resultat(self.s1, self.a1)

    def winner(self):
        if self.ps1 == self.ps2:
            return 'Ingen'
        elif self.ps1 > self.ps2:
            return self.s1
        else:
            return self.s2

    def get_score(self):
        return [self.ps1,self.ps2]

    def __str__(self):
        return str(self.s1) + ": " + str(self.a1) + ". " + str(self.s2) + " : " + \
               str(self.a2) + " --> " + str(self.winner()) + " vinner"



# ****************MANGESPILL CLASS****************
class MangeSpill:

    def __init__(self,spiller1,spiller2,antall_spill):
        self.s1 = spiller1
        self.s2 = spiller2
        self.antall_spill = antall_spill

    def arranger_enkeltspill(self):
        return EnkeltSpill(self.s1,self.s2)

    def arranger_turnering(self):
        tot_s1 = 0
        tot_s2 = 0
        gevinst_s1 = []
        x_akse = []
        count = 0
        for x in range(0,self.antall_spill):
            enkel = self.arranger_enkeltspill()
            enkel.gjennomfør_spill()
            score = enkel.get_score()
            tot_s1 += score[0]
            tot_s2 += score[1]

            ##PYPLOT##
            count+=1
            x_akse.append(count)
            gevinst_s1.append(tot_s1/count)

            print(enkel)

        ##PYPLOT##
        plt.plot(x_akse,gevinst_s1)
        plt.axis([0,self.antall_spill,0,1])
        plt.grid(True)
        plt.axhline(y=0.5,linewidth=0.5, color="r")
        plt.xlabel("Antall Spill")
        plt.ylabel("Gevinstprosent: " + str(self.s1))
        plt.show()

        print("\nTotal score i turneringen:\n" + str(self.s1) + ": " + str(tot_s1) + " poeng" +
              "\n" + str(self.s2) + ": " + str(tot_s2) + " poeng")




#*****************HJELPEFUNKSJONER*****************
def motsatte(self, num):
    a = {0: 2, 1: 0, 2: 1}
    return a[num]


def main():
    s1 = Historiker('Kristoffer',2)
    s2 = MestVanlig('William')

    mange = MangeSpill(s1,s2,1000)
    mange.arranger_turnering()





main()