# -*- coding: utf-8 -*-
import networkx as nkx
import numpy as np
import struct_graph as strgr
import xmlschema
import lerInst as li
import gerador as GR
from pyclustering.cluster.kmeans import kmeans
from pyclustering.utils.metric import type_metric, distance_metric


def my_func(L1, L2):
    C1 = nkx.shortest_path(grafo,L1[0],L1[1])
    C2 = nkx.shortest_path(grafo,L2[0],L2[1])
    Camin1 = [(C1[m],C1[(m+1)]) for m in range(len(C1)-1)]
    Camin2 = [(C2[m],C2[(m+1)]) for m in range(len(C2)-1)]
    cinter = [i for i in Camin1 if i in Camin2]
    return len(cinter)

#class Cluster:
if __name__ == '__main__':
    teste = 'C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instâncias\\pickle\\eon.pickle'
    #teste = '../Instâncias/pickle/att.pickle'
    Inst = strgr.lePickle(teste)
    grafo = Inst.CriaGrafo()
    Lreq = Inst.splitReq()
    Lij = []
    for x in range(len(Lreq)):
        Lij.append([Lreq[x].i,Lreq[x].j])
    metric = distance_metric(type_metric.USER_DEFINED, func=my_func)
    distance = metric(Lij[10], Lij[12])
    print(distance)
    array = np.array(Lreq)
    start_centers = [[0,0],[1,1],[2,2],[3,3]]
    kmeans_instance = kmeans(Lij, start_centers,metric=metric)
    kmeans_instance.process()
    clusters = kmeans_instance.get_clusters()
    
