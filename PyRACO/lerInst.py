# -*- coding: utf-8 -*-
import networkx as nkx
import numpy as np
import struct_graph as strgr
import xmlschema

def lerTXT(arq):

    with open(arq, 'r') as f:
        flines = f.readlines()
        f0split = flines[0].split()
        nnodes = int(f0split[0])

        adjMtx = []
        for i in range(nnodes):
            fsplit = flines[2 + i].split()
            fnum = [int(i) for i in fsplit]
            adjMtx.append(fnum)

        reqMtx = []
        for i in range(nnodes):
            fsplit = flines[nnodes + 3 + i].split()
            fnum = [int(i) for i in fsplit]
            reqMtx.append(fnum)

        #Criação do grafo
        #npAdj = np.array(adjMtx)
        #grafo = nkx.convert_matrix.from_numpy_matrix(npAdj)
        #capacidade = 1
        #nkx.set_edge_attributes(grafo, capacidade, "capacity")


        return(nnodes,adjMtx,reqMtx)

def LerXMLGen(arq):
    xs = xmlschema.XMLSchema('gera.xsd')
#    print(xs.is_valid(arq))
#    pprint(xs.to_dict(arq))
    my_dict = xs.to_dict(arq)
    return my_dict