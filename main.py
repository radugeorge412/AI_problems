import math


class NodParcurgere:

    gr = None  # trebuie setat sa contina instanta problemei
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            if nod.parinte is not None:
                if nod.parinte.info[3] == 1:
                    mbarca1 = self.__class__.gr.malInitial
                    mbarca2 = self.__class__.gr.malFinal
                else:
                    mbarca1 = self.__class__.gr.malFinal
                    mbarca2 = self.__class__.gr.malInitial
                print(">>> Barca s-a deplasat de la malul {} la malul {} cu {} oameni.".format(mbarca1 , mbarca2,
                        abs(nod.info[0]+nod.info[1]-nod.parinte.info[0]-nod.parinte.info[1])))
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisLung:
            print("Nr noduri: ", len(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if infoNodNou == nodDrum.info:
                return True
            nodDrum = nodDrum.parinte

        return False


    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return (sir)

    #------------------------------------------------

    def __str__(self):
        if self.info[3] == 1:
            barcaMalInitial = "<barca>"
            barcaMalFinal = "       "
        else:
            barcaMalInitial = "       "
            barcaMalFinal = "<barca>"
        return ("Mal: " + self.gr.malInitial + " Canibali: {} Misionari: {} Fantome: {} {} |||  Mal:" + self.gr.malFinal + " Canibali: {} Misionari: {} Fantome: {} {}").format(
            self.info[0], self.info[1] ,self.info[2], barcaMalInitial, self.__class__.gr.N - self.info[0],
            self.__class__.gr.N - self.info[1], self.__class__.gr.NF - self.info[2], barcaMalFinal)

#Graful problemei
class Graph:
    
    M = None
    NF = None
    N = None

    def __init__(self, nume_fisier):


        f = open(nume_fisier,"r")
        text = f.read()
        #extragem input-ul
        text = text.split("\n")
        listaInit = []

        for i in text:
            txt = i.split("=")
            listaInit.append(txt)

        listaInfoFisier = []
        lungime = len(listaInit)
        for i in range(lungime):
            listaInfoFisier.append(listaInit[i][1])
        #Vom avea listaInfoFisier[0] = canibali/misionari , [1]=locuri, [2]=fantome , [3]=mal init, [4] = mal final
        #-----------------------------------------
        #atribuirea informatiilor
        self.__class__.N = int(listaInfoFisier[0]) #canibalii si misionarii
        self.__class__.M = int(listaInfoFisier[1]) #numarul de locuri din barca
        self.__class__.NF = int(listaInfoFisier[2]) #numarul de fantome
        self.__class__.malInitial = listaInfoFisier[3]
        self.__class__.malFinal = listaInfoFisier[4]
        self.start = (self.__class__.N,self.__class__.N,self.__class__.NF,1, 0)   # 1=barca e pe malul initial
        self.scopuri=[(0,0,self.__class__.NF,0,0)]  #stare finala = 0 oameni si toate fantomele pe malul initial

    def testeaza_scop(self,nodCurent):
        return nodCurent.info in self.scopuri

        #----------------------------------------

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):


        def test_conditie(mis, can, fan):
            return ((can+mis) >= fan and (mis>=can)) or (mis==0 and can>=fan)

        listaSuccesori = []
        #nodCurentInfo -> (CanibaliMalInitial, MisionariMalInitial,FantomeMalInitial,MalBarca)
        if nodCurent.info[3]==1:  #daca barca e pe malul initial
            canMalCurent = nodCurent.info[0]
            misMalCurent = nodCurent.info[1]
            fanMalCurent = nodCurent.info[2]
            canMalOpus = Graph.N - canMalCurent
            misMalOpus = Graph.N - misMalCurent
            fanMalOpus = Graph.NF - fanMalCurent
        else:   #daca barca e pe malul opus
            canMalOpus = nodCurent.info[0]
            misMalOpus = nodCurent.info[1]
            fanMalOpus = nodCurent.info[2]
            canMalCurent = Graph.N - canMalOpus
            misMalCurent = Graph.N - misMalOpus
            fanMalCurent = Graph.NF - fanMalOpus

        maxMisBarca = min(Graph.M, misMalCurent)
        for misBarca in range(maxMisBarca+1):
            if(misBarca == 0):
                minCanBarca = 1
                maxCanBarca = min(Graph.M, canMalCurent)
            else:
                minCanBarca = 0
                maxCanBarca = min(misBarca, canMalCurent, Graph.M-misBarca)

            for canBarca in range(minCanBarca,maxCanBarca+1):
                if canBarca == 0:
                    minFanBarca = 0
                    maxFanBarca = 0
                else:
                    if misBarca == 0:
                        minFanBarca = 0
                        maxFanBarca = min(canBarca, Graph.M - canBarca, fanMalCurent)

                    else:
                        minFanBarca = 0
                        maxFanBarca = 0

                for fanBarca in range(minFanBarca, maxFanBarca+1):
                   # print("fanBarca", fanBarca, maxFanBarca, fanMalCurent)
                    canMalCurentNou = canMalCurent - canBarca
                    misMalCurentNou = misMalCurent - misBarca
                    fanMalCurentNou = fanMalCurent - fanBarca
                    canMalOpusNou = canMalOpus + canBarca
                    misMalOpusNou = misMalOpus + misBarca
                    fanMalOpusNou = fanMalOpus + fanBarca
                    if(canMalCurentNou == 0 and misMalCurentNou != 0 and fanMalCurentNou!=0):
                        fanMalCurentNou = fanMalOpusNou - 1
                    if(canMalOpusNou == 0 and misMalOpusNou != 0 and fanMalOpusNou != 0):
                        fanMalOpusNou = fanMalOpusNou - 1
                    if not test_conditie(misMalCurentNou, canMalCurentNou, fanMalCurentNou):
                        continue
                    if not test_conditie(misMalOpusNou, canMalOpusNou, fanMalOpusNou):
                        continue
                    if nodCurent.info[3] == 1:
                        infoNodNou = (canMalCurentNou, misMalCurentNou, fanMalCurentNou, 0, fanMalOpusNou)
                    else:
                        infoNodNou = (canMalOpusNou, misMalOpusNou, fanMalOpusNou, 1, fanMalCurentNou)
                    if not nodCurent.contineInDrum(infoNodNou):
                        costSuccesor = misBarca+canBarca-fanBarca
                        listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costSuccesor, NodParcurgere.gr.calculeaza_h(infoNodNou, tip_euristica)))

        return listaSuccesori

    #================================================
    #euristica banala


    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala" :
            if infoNod not in self.scopuri:
                return 1
            return 0
        else:
            return 2*math.ceil((infoNod[0]+infoNod[1])/self.M)+(1-infoNod[3])-1
            #return 2*math.ceil((infoNod[0]+infoNod[1])/(self.M-1))+(1-infoNod[3])-1

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir


def uniform_cost(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.noduri.index(gr.start), gr.start, 0, None)]

    while len(c) > 0:
        print("Coada actuala: " + str(c))
        input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ", end="")
            nodCurent.afisDrum()
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                if c[i].g > s.g:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def ida_star(gr, nrSolutiiCautate):
    nodStart = NodParcurgere(gr.indiceNod(gr.start), gr.start, None, 0, gr.calculeaza_h(gr.start))
    limita = nodStart.f
    while True:

        print("Limita de pornire: ", limita)
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate)
        if rez == "gata":
            break
        if rez == float('inf'):
            print("Nu exista solutii!")
            break
        limita = rez
        print(">>> Limita noua: ", limita)
        input()


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate):
    print("A ajuns la: ", nodCurent)
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f
    if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
        print("Solutie: ")
        nodCurent.afisDrum()
        print(limita)
        print("\n----------------\n")
        input()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return 0, "gata"
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    minim = float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate)
        if rez == "gata":
            return 0, "gata"
        print("Compara ", rez, " cu ", minim)
        if rez < minim:
            minim = rez
            print("Noul minim: ", minim)
    return nrSolutiiCautate, minim


def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)




gr = Graph("input.txt")
NodParcurgere.gr = gr
outPut = open("output1.txt", "w")

print("\n\n##################\nSolutii obtinute cu A*:")
nrSolutiiCautate=3
a_star(gr, nrSolutiiCautate=3, tip_euristica="euristica banala")
outPut.close()
