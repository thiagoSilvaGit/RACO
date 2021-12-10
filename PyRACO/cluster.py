# -*- coding: utf-8 -*-
import networkx as nkx
import numpy as np
import struct_graph as strgr
import xmlschema
import lerInst as li
import gerador as GR
import pyclustering
from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.utils.metric import type_metric, distance_metric
from pyclustering.cluster import cluster_visualizer_multidim


def my_func(L1, L2):
    cinter=0
    for i in range(len(L1)):
        if L1[i] == L2[i] and L1[i] == 1 and L2[i] == 1:
            cinter = cinter + 1
    return cinter

#class Cluster:
if __name__ == '__main__':
    teste = 'C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instâncias\\pickle\\eon.pickle'
    #teste = '../Instâncias/pickle/att.pickle'
    Inst = strgr.lePickle(teste)
    grafo = Inst.CriaGrafo()
    Lreq = Inst.splitReq()
    Lij = []
    #for x in range(len(Lreq)):
    #    Lij.append([Lreq[x].i,Lreq[x].j])
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
    
    #metric = distance_metric(type_metric.USER_DEFINED, func=my_func)
    metric = distance_metric(type_metric.EUCLIDEAN)
    distance = metric(Lij[12], Lij[13])
    print(distance)
    C1 = nkx.shortest_path(grafo,Lreq[12].i,Lreq[12].j)
    C2 = nkx.shortest_path(grafo,Lreq[13].i,Lreq[13].j)
    #p = [2,1]
    #print(p[0])
    start_centers = [Lij[5],Lij[12],Lij[25]]
    kmeans_instance = kmeans(Lij, start_centers,metric=metric)
    kmeans_instance.process()
    clusters = kmeans_instance.get_clusters()
    print(clusters)
    #visualizer = cluster_visualizer_multidim()
    #visualizer.append_clusters(clusters, Lij)
    #visualizer.show(max_row_size=3)
    