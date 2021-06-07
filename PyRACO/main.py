# This is a sample Python script.
import networkx as nx

import lerInst as li
import numpy as np
import struct_graph as strgr
import linkedlist as ll
import networkx as nkx
import matplotlib.pyplot as plt
import random 
import kapov as kv
import time 

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

if __name__ == '__main__':
    random.seed(30)
     
    Glist=[]   #Lista de grafos
    n,adj,Lreq = li.lerTXT('brasil.txt') #Leitura do arquivo de dados
    Fo = float('inf') #Inicializando a Função objetivo com infinito
    maxv = max(Lreq, key = lambda maxcmin : maxcmin.cmin)
    maxcm = maxv.cmin    #Atribuindo o maior caminho minimo dos dados
    
    end_time = time.time() + 300
    countTimer = 0
    while time.time() < end_time:
        g = strgr.CriaGrafo(adj)
        Glist.append(strgr.Rede(g,len(Glist)+1))
        
        random.shuffle(Lreq)       #Randomizando a Lista de requisição
        Lreq.sort(key=lambda cammin: cammin.cmin,reverse=True)      #Ordenando a Lista de requisiçao em ordem decrescente em relação o Cammin
        result = kv.mkapov(Lreq,Glist,adj,maxcm,Fo)                 #Metodo Kapov

        if result < Fo:
            Fo = result

        Glist.clear()

    print(Fo)


    #print(g.edges(data=True)) 
    #nkx.draw(g,with_labels=True)
    #plt.show()
    #print(g.number_of_nodes())
    #print(g.nodes())
    #print(g.edges())
    

    