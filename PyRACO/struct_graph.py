# -*- coding: utf-8 -*-
import networkx as nkx
import numpy as np
import networkx as nkx
import lerInst as li

#Função para criar Grafo


class Instancia:
    def __init__(self):
        self.Lreq = []
        self.Ladj = []
        self.n = 0

    def leTXT(self, file):
        nf, adjf, Lreqf = li.lerTXT(file)  # Leitura do arquivo de dados
        self.n = nf
        self.Ladj = adjf
        self.Lreq = Lreqf


    def imprimirTXT(self, pfile):
        with open(pfile, 'w') as pf:
            pf.write(str(self.n) + '\n\n')
            linhas = []
            for linha in self.Ladj:
                slinha = ''
                for i in linha:
                    slinha += '{} '.format(i)
                slinha += '\n'
                linhas.append(slinha)
            pf.writelines(linhas)

            pf.write('\n')
            linhas = []
            for linha in self.Lreq:
                slinha = ''
                for i in linha:
                    slinha += '{} '.format(i)
                slinha += '\n'
                linhas.append(slinha)
            pf.writelines(linhas)

    def splitReq(self):
        listaReq = []
        reqMtx = np.array(self.Lreq)
        grafo = self.CriaGrafo()
        for i in range(self.n):
            for j in range(self.n):
                if reqMtx[i][j]:
                    mxf, cmf = nkx.maximum_flow(grafo, i, j)  # Função para encontra o fluxo maximo
                    cmin = nkx.shortest_path_length(grafo, i, j)  # Funcao para encontrar o valor do caminho minimo
                    for k in range(reqMtx[i][j]):
                        listaReq.append(Requisicao(i, j, mxf, cmin))
        return listaReq

    def CriaGrafo(self):
        npAdj = np.array(self.Ladj)
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
