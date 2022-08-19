# -*- coding: utf-8 -*-
import networkx as nkx
import numpy as np
import struct_graph as strgr
import xmlschema
import lerInst as li
import gerador as GR
from sklearn.cluster import AgglomerativeClustering
import pyclustering
from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.kmedoids import kmedoids

from pyclustering.utils.metric import type_metric, distance_metric,euclidean_distance
from pyclustering.cluster import cluster_visualizer_multidim
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from sklearn.metrics import pairwise_distances
import random 
import math 


def my_func1(L1, L2):
    '''cinter=0
    for i in range(len(L1)):
        if L1[i] == L2[i] and L1[i] == 1 and L2[i] == 1:
            cinter = cinter + 1'''
    global grafo
    C1 = nkx.shortest_path(grafo,math.ceil(L1[0]),math.ceil(L1[1]))
    Camin1 = [(C1[m],C1[(m+1)]) for m in range(len(C1)-1)]
    C2 = nkx.shortest_path(grafo, math.ceil(L2[0]),math.ceil(L2[1]))
    Camin2 = [(C2[m],C2[(m+1)]) for m in range(len(C2)-1)]
    return len(set(Camin1).intersection(Camin2))
    #return cinter

def my_func2(L1, L2):
    #eucl = euclidean_distance(L1,L2)
    eucl = np.linalg.norm(np.array(L1)-np.array(L2))
    return (1/(eucl+1))
    #return (-eucl)

def my_funcA(L):
    return pairwise_distances(L, metric= my_func1)

#class Cluster:
def fcluster(arq,numR):
#if __name__ == '__main__':
    #teste = 'C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instâncias\\pickle\\eon.pickle'
    #teste = '../Instâncias/pickle/att.pickle'
    global grafo
    Inst = strgr.lePickle(arq)
    grafo = Inst.CriaGrafo()
    Lreq = Inst.splitReq()
    Lij = []                  #lista dos vetores binarios dos caminhos minimos das requisições
    LRij = []                 #Lista dos pares O/D das requisiçoes
    cent = []                 #centroides
    ladjMtx = np.array(Inst.Ladj)
    ledges = []               #vetor de arcos da rede
    for i in range(Inst.n):
        for j in range(Inst.n):
            if ladjMtx[i][j]:
                ledges.append((i,j))        
    for k in range(len(Lreq)):
        Radj = [0] * len(ledges)               #vetor binario de indicaçao do caminho utilizado pela Req
        C = nkx.shortest_path(grafo, Lreq[k].i,Lreq[k].j)
        Camin = [(C[m],C[(m+1)]) for m in range(len(C)-1)]
        LRij.append([Lreq[k].i,Lreq[k].j])                  
        for a in range(len(Camin)):
            for s in range(len(ledges)):
                if Camin[a] == ledges[s]:
                    Radj[s] = 1
        Lij.append(Radj.copy())
        C.clear()
        Camin.clear()
        Radj.clear()    

    
    

    metric = distance_metric(type_metric.USER_DEFINED, func=my_func2)
    #metric = distance_metric(type_metric.EUCLIDEAN)
    random.seed(1000)
    #start_centers = kmeans_plusplus_initializer(LRij,5).initialize()

    #centers = np.random.choice(list(range(len(Lij))),8)
    #start_centers = [Lij[r] for r in centers]
    #kmedoids_instance = kmedoids(Lij, start_centers, metric=metric)
    #kmeans_instance = kmeans(Lij, start_centers, metric=metric)
    #kmeans_instance.process()
    #kmedoids_instance.process()
    #clusters = kmeans_instance.get_clusters()
    #clusters = kmedoids_instance.get_clusters()

    L = np.array(Lij)
    #L = np.array(LRij)
    NC =  math.ceil(len(Lij)/numR)

    clusters = AgglomerativeClustering(n_clusters= NC).fit(L) #affinity = my_funcA, linkage = 'average').fit(L)
        
    #visualizer = cluster_visualizer_multidim()
    #visualizer.append_clusters(clusters, Lij)
    #visualizer.show(max_row_size=3)
    #for i in clusters[1]:
    #    print(Lreq[i].i)
    #    print(Lreq[i].j)
    #print(len(clusters))
    #print(clusters.n_clusters_)
    
    clt = []
    for c in range (clusters.n_clusters_):
        clt.append([i for i in range(len(clusters.labels_)) if clusters.labels_[i] == c]) 
    
    return clt 