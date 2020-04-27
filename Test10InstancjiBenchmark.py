
from math import sqrt
from multiprocessing import freeze_support

import Greedy
import ACO
def printResults(greedySol, AcoSol):
    print("Algorytm zachłanny: \n" + str(greedySol) + "\n")
    print("Ant Colony Optimization: \n" + str(AcoSol) + "\n")
    jakosc = "Algorytm ACO okazał się lepszy o " + str(
        qualityComparedToGreedy(greedySol[0], AcoSol[0])) + "% względem algorytmu zachłannego"
    print(jakosc)
def qualityComparedToGreedy(greedyLen, AcoLen):
    return round((greedyLen*100/AcoLen)-100,2)

def distance(x1, x2, y1, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

class Graph:
    def __init__(self,n,points): #constructor
        self.matrix = [[0 for i in range(n)] for j in range(n)] #adjacency matrix
        for i in range(len(points)): #we fill our matrix with the distances
            #[p, x, y,] = points[i].split(' ')
            kkk = points[i].split(' ')
            p = kkk[0]
            x = kkk[1]
            y = kkk[2]
            p, x, y = int(p)-1, int(x), int(y)
            for j in range(i, len(points)):
                #[p1, x1, y1] = points[j].split(' ')
                kkk = points[j].split(' ')
                p1 = kkk[0]
                x1 = kkk[1]
                y1 = kkk[2]
                p1, x1, y1 = int(p1)-1, int(x1), int(y1)
                self.matrix[p][p1] = self.matrix[p1][p] = round(distance(x, x1, y, y1),2)

if __name__ == '__main__':
    fileName = "WynikiInstancjiBenchmarkowych.txt"
    file = open(fileName, "w")
    file.write("ACO;Optimal\n")
    optimal =[7542,118282,1610,14379,538,426,21282,44303,1211,675]
    # berlin52 : 7542
    # bier127 : 118282
    # bayg29 = 1610
    # lin105 : 14379
    # eil76 : 538
    # eil51 : 426
    # kroA100 : 21282
    # pr107 : 44303
    # rat99 : 1211
    # st70 : 675


    i=0
    while i<10:
        if(i==0):
            contents = open("berlin52.txt", "r").readlines()  # load data
            print("wyniki dla berlin52:")
        if(i==1):
            contents = open("bier127.txt", "r").readlines()  # load data
            print("wyniki dla bier127:")
        if (i == 2):
            contents = open("bayg29.txt", "r").readlines()  # load data
            print("wyniki dla bayg29:")
        if (i == 3):
            contents = open("lin105.txt", "r").readlines()  # load data
            print("wyniki dla lin105:")
        if (i == 4):
            contents = open("eil76.txt", "r").readlines()  # load data
            print("wyniki dla eil76:")

        if (i == 5):
            contents = open("eil51.txt", "r").readlines()  # load data
            print("wyniki dla eil51:")

        if (i == 6):
            contents = open("kroA100.txt", "r").readlines()  # load data
            print("wyniki dla kroA100:")

        if (i == 7):
            contents = open("pr107.txt", "r").readlines()  # load data
            print("wyniki dla pr107:")

        if (i == 8):
            contents = open("rat99.txt", "r").readlines()  # load data
            print("wyniki dla rat99:")
        if (i == 9):
            contents = open("st70.txt", "r").readlines()  # load data
            print("wyniki dla st70:")

        n = int(contents[0]) # number of vertex
        contents = contents[1:] #coordinates of vertex (starts at one)
        graph =Graph(n, contents)
        AcoSol = ACO.antcolony(graph)
        print("Optymalne rozwiazanie: \n" + str(optimal[i]) + "\n")
        print("Ant Colony Optimization: \n" + str(AcoSol) + "\n")
        file.write(str(AcoSol[0]) + ";" + str(optimal[i]) + "\n")
        print("---------------------------------------------------------------------")
        i=i+1

