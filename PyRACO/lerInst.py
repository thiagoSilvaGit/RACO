# -*- coding: utf-8 -*-
import networkx as nkx
import numpy as np

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

        npAdj = np.array(adjMtx)
        grafo = nkx.convert_matrix.from_numpy_matrix(npAdj)

        return(nnodes,adjMtx,reqMtx,grafo)