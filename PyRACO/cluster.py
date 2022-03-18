# -*- coding: utf-8 -*-
import networkx as nkx
import numpy as np
import struct_graph as strgr
import xmlschema
import lerInst as li
import gerador as GR
import pyclustering
from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.utils.metric import type_metric, distance_metric,euclidean_distance
from pyclustering.cluster import cluster_visualizer_multidim
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
import random 


def my_func1(L1, L2):
    cinter=0
    for i in range(len(L1)):
        if L1[i] == L2[i] and L1[i] == 1 and L2[i] == 1:
            cinter = cinter + 1
    return (-cinter)

def my_func2(L1, L2):
    eucl = euclidean_distance(L1,L2)
    #return (1/(eucl+1))
    return (-eucl)

#class Cluster:
def fcluster(arq):
#if __name__ == '__main__':
    #teste = 'C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instâncias\\pickle\\eon.pickle'
    #teste = '../Instâncias/pickle/att.pickle'
    Inst = strgr.lePickle(arq)
    grafo = Inst.CriaGrafo()
    Lreq = Inst.splitReq()
    Lij = []
    cent = []
    #metric = distance_metric(type_metric.USER_DEFINED, func=my_func)
    #distance = metric(Lij[10], Lij[12])
    #print(distance)
    array = np.array(Lreq)
    ladjMtx = np.array(Inst.Ladj)
    ledges = []
    for i in range(Inst.n):
        for j in range(Inst.n):
            if ladjMtx[i][j]:
                ledges.append((i,j)) 
    for k in range(len(Lreq)):
        Radj = [0] * len(ledges)
        C = nkx.shortest_path(grafo,Lreq[k].i,Lreq[k].j)
        Camin = [(C[m],C[(m+1)]) for m in range(len(C)-1)]
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
    start_centers = kmeans_plusplus_initializer(Lij,6).initialize()

    #start_centers = [cent[0],cent[1],cent[2],cent[3]]
    kmeans_instance = kmeans(Lij, start_centers, metric=metric)
    kmeans_instance.process()
    clusters = kmeans_instance.get_clusters()
    #visualizer = cluster_visualizer_multidim()
    #visualizer.append_clusters(clusters, Lij)
    #visualizer.show(max_row_size=3)
    #for i in clusters[1]:
    #    print(Lreq[i].i)
    #    print(Lreq[i].j)
    print(len(clusters))
    return clusters 