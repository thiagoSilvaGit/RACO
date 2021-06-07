# -*- coding: utf-8 -*-
import networkx as nkx
import numpy as np
import networkx as nkx

#Função para criar Grafo
def CriaGrafo(adjMtx):
    npAdj = np.array(adjMtx)
    grafo = nkx.convert_matrix.from_numpy_matrix(npAdj,create_using=nkx.DiGraph)
    capacidade = 1
    nkx.set_edge_attributes(grafo, capacidade, "capacity")
    return (grafo)


class Requisicao:
    def __init__(self, org,dest,mxf,cmin):
        self.i = org
        self.j = dest
        self.mxf = mxf
        self.cmin = cmin



class Rede:
    def __init__(self, g, numg):
        self.Grafo = g
        self.numg = numg


"""
class Resposta:
    def __init__(self):
        self.lgrafos = []
        self.attReq = []
"""
