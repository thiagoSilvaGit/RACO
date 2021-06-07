# -*- coding: utf-8 -*-
import networkx as nkx
import numpy as np
import struct_graph as strgr

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
        npAdj = np.array(adjMtx)
        grafo = nkx.convert_matrix.from_numpy_matrix(npAdj)
        capacidade = 1
        nkx.set_edge_attributes(grafo, capacidade, "capacity")

        #Criação da lista de requisições
        listaReq = []
        reqMtx = np.array(reqMtx)
        for i in range(nnodes):
            for j in range(nnodes):
                if reqMtx[i][j]:
                    mxf,cmf = nkx.maximum_flow(grafo,i,j)    #Função para encontra o fluxo maximo   
                    cmin=nkx.shortest_path_length(grafo,i,j) #Funcao para encontrar o valor do caminho minimo
                    for k in range(reqMtx[i][j]):
                        listaReq.append(strgr.Requisicao(i,j,mxf,cmin))
                else:
                    pass

        return(nnodes,adjMtx,listaReq)