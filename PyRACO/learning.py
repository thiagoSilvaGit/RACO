# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import statistics as st
import networkx as nkx
import itertools as it
import heuristicas as h



def classificaInst(I):
    grafo = I.CriaGrafo()
    indGrafo = classificaGrafo(grafo)
    indReq = classificaReq(I.Lreq,I.nf)
    listaInd = indGrafo + indReq
    return listaInd

def classificaReq(R,n):

    sai = [sum(r) for r in R]
    entra = [sum([linha[n] for linha in R]) for j in range(len(R))]
    # 5.3 - Número de Requisições
    nr = sum(sai)
    # 5.4 - Média Requisições
    mrs = nr/n
    # 5.5 - Máximo de Requisições que saem
    maxrs = max(sai)
    # 5.5 - Máximo de Requisições que chegam
    maxrc = max(entra)
    # 5.7 - Desvio padrão de requisições
    stdrs = st.stdev(sai)
    stdrc = st.stdev(entra)

    return [nr, mrs, maxrs, maxrc, stdrs, stdrc]


    return 0

def classificaGrafo(g):
    # 5.1 - Número de Nós
    n = g.number_of_nodes()
    # 5.2 - Número de Arcos
    a = g.number_of_edges()
    # 5.8 - |Arcos|/|Nos|
    r = a/n
    # 5.9 - Grau max dos nós
    gdmax = max(g.Degree)
    gdmin = min(g.Degree)
    # 5.10 - Fluxo Máximo
    # 5.11 - Maior caminho mínimo

    maxmf = 0
    maxcmin = 0
    for i in range(n):
        for j in range(n):
            mxf, _ = nkx.maximum_flow(g, i, j)
            cmin = nkx.shortest_path_length(g, i, j)
            if mxf > maxmf:
                maxmf = mxf
            if cmin > maxcmin
                maxcmin = cmin

    ind = [n, a, r, gdmax, gdmin, maxmf,maxcmin]

    return ind


def criaDFLearning(Data)

    return 0

def criaData(listaAlg,listOrd,nrep, Inst, seed = 10):
    # executar todos os algoritmos, número de vezes específica e coletar o resultado

    indicadores = classificaInst(Inst)

    observ = []
    for (A,O) in it.product(listaAlg,listOrd):
        for i in range(nrep):
            metodo = h.Hsolver(A, 1, O)
            metodo.setseed(seed)
            res = metodo.solve1it(Inst)
            observ.append(indicadores + res)

    return observ