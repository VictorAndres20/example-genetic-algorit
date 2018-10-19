import random

class Cromosoma:
    def __init__(self,letter):
        self.letter=letter
        self.fitness=0.0
        self.propability=0.0
        self.x=0

    def calculateFitness(self,compare):
        for i in range(0,len(self.letter)):
            if(self.letter[i]==compare[i]):
                self.x+=1
        
        self.fitness=2**self.x

class Algorithm:
    def __init__(self):
        self.getCompare()
        #Cromosomas
        self.cromosomas=[]
        #Seleccionados
        self.selected=[]
        #Valor del total de la funcion fitness
        self.totalFitness=0.0
        #Cantidad de indivuduos a seleccionar en el proceso de seleccion
        self.quantSelect=6

    def getCompare(self):
        file=open("palabra.txt")
        line=file.readline()
        self.compare=line.upper()
        file.close()

    def validateWord(self):
        print("Palabra ingresada ",end="")
        print(self.compare,end=" ")
        if(len(self.compare)>5 or len(self.compare)<5):
            print("no tiene una longitud de 5 caracteres")
            return False
        else:
            print("es válida")
            return True
        print()

    ############################
    # CREAR LA POBLACION INICIAL
    #
    def createInitPob(self,path):
        file=open(path)
        line=file.readline()
        while(line):
            muestra=line.split(" ")
            #Se crea el nuevo cromosoma
            cromosoma=Cromosoma(muestra[0])
            #Se calcula la funcion fitness
            cromosoma.calculateFitness(self.compare)
            #Se va acumulando el total de la funcion fitness
            self.totalFitness+=cromosoma.fitness
            #print("AGREGANDO:",end=" ")
            #print(cromosoma.letter,end=" fitness = ")
            #print(cromosoma.fitness)
            self.cromosomas.append(cromosoma)
            line=file.readline()

        print("Se ha agregado una población inicial de:",end=" ")
        print(len(self.cromosomas),end=" ")
        print("individuos")
        print("Total fitness de la población inicial es de:",end=" ")
        print(self.totalFitness)
        print()
    #
    ############################

    ############
    # SELECCION POR RULETA
    #
    def ruleta(self):
        self.asignProbability()
        self.cromosomas=sorted(self.cromosomas, key=lambda crom: crom.propability,reverse=True)
        self.selectorRuleta()

    #Asignar las probabilidades de seleccion
    def asignProbability(self):
        for i in range(0,len(self.cromosomas)):
            self.cromosomas[i].propability=(float(self.cromosomas[i].fitness)*float(100))/float(self.totalFitness)
            
        print("Se asignan probabilidades de selección\n")

    #Selccionar los individuos
    def selectorRuleta(self):
        self.selected=[]
        for i in range(0,self.quantSelect):
            rand=float(random.random())
            acum=0.0
            j=0
            while(j<len(self.cromosomas)):
                acum+=self.cromosomas[j].propability
                if(acum>=rand):
                    self.selected.append(self.cromosomas[j])
                    j=len(self.cromosomas)

                j+=1

        #Letras seleccionadas
        print("Individuos seleccionados por técnica de ruleta")
        for i in range(0,len(self.selected)):
            print(self.selected[i].letter,end=" -> letras correctas: ")
            print(self.selected[i].x,end=" -> fitness: ")
            print(self.selected[i].fitness)

        print()
    #
    ############

    ############
    # CRUCE UNIFORME
    #
    def cruce(self):
        pairs=self.generatePartner()
        self.cruceUniforme(pairs)

    def generatePartner(self):
        pairs=[]
        for i in range(int(self.quantSelect/2)):
            pairs.append([i,len(self.selected)-1-i])
        return pairs

    def cruceUniforme(self,pairs):
        #Mascara
        mask=self.getMask()
        print("Parejas seleccionadas")
        for i in range(len(pairs)):
            c1=self.selected[int(pairs[i][0])]
            c2=self.selected[int(pairs[i][1])]
            print(c1.letter,end=" vs ")
            print(c2.letter)
            self.selected[int(pairs[i][0])]=self.newWord(c1.letter,c2.letter,mask)
            self.selected[int(pairs[i][1])]=self.newWord(c2.letter,c1.letter,mask)

        print()

        #Letras cruzadas
        print("Cruce uniforme realizado")
        for i in range(0,len(self.selected)):
            print(self.selected[i].letter,end=" -> letras correctas: ")
            print(self.selected[i].x,end=" -> fitness: ")
            print(self.selected[i].fitness)

        print()


    def getMask(self):
        mask=[]
        for i in range(0,self.quantSelect-1):
            mask.append(random.randint(0,1))
        return mask

    def newWord(self,w1,w2,mask):
        nword=""
        for i in range(0,len(mask)):
            if(mask[i]==1):
                nword+=w1[i]
            else:
                nword+=w2[i]
        crom=Cromosoma(nword)
        crom.calculateFitness(self.compare)
        return crom

    #
    ############

    ############
    # MUTACION ALEATORIA
    #
    def mutacion(self):
        alf="ABCDEFGHIJKLMNOPQRSTUWXYZ";
        for i in range(0,len(self.selected)):
            rand1=random.randint(0,len(self.selected[i].letter)-1)
            rand2=random.randint(0,len(alf)-1)
            nword=""
            for j in range(0,len(self.selected[i].letter)):
                if(rand1 != j):
                    nword+=self.selected[i].letter[j]
                else:
                    nword+=alf[rand2]

            self.selected[i].letter=nword
            self.selected[i].x=0
            self.selected[i].fitness=0.0
            self.selected[i].calculateFitness(self.compare)


        print()
        #Letras Mutadas
        print("Mutación aleatoria realizada")
        for i in range(0,len(self.selected)):
            print(self.selected[i].letter,end=" -> letras correctas: ")
            print(self.selected[i].x,end=" -> fitness: ")
            print(self.selected[i].fitness)

        print()
        self.getProms()

    #
    ############

    def getProms(self):
        totalFit=0.0
        promFit=0.0
        for i in range(0,len(self.selected)):
            totalFit+=self.selected[i].fitness
        promFit=float(totalFit)/float(len(self.selected))
        print("Total fitness:",end=" ")
        print(totalFit)
        print("Promedio fitness:",end=" ")
        print(promFit)
        print()



class Main:
    def __init__(self):        
        self.presentation()
        self.algorithm=Algorithm()
        if(self.algorithm.validateWord()):
            #CREAR POBLACION INICIAL
            self.algorithm.createInitPob("muestra.txt")
            #PROCESO DE SELECCION
            self.algorithm.ruleta()
            #PROCESO DE CRUCE
            self.algorithm.cruce()
            #PROCESO DE MUTACIÓN
            self.algorithm.mutacion()

    def presentation(self):
        print("\n\nVíctor Andrés Pedraza León")
        print("Matemáticas aplicadas")
        print("Taller 2 - Algoritmos genéticos\n\n")

main=Main()
