# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import statistics as st
import networkx as nkx
import itertools as it
import heuristicas as h
import time


def classificaInst(I):
    grafo = I.CriaGrafo()
    indGrafo = classificaGrafo(grafo)
    indReq = classificaReq(I.Lreq, I.n, I.lb)
    listaInd = indGrafo + indReq
    return listaInd


def classificaReq(R, n, lb):
    sai = [sum(r) for r in R]
    entra = [sum([linha[j] for linha in R]) for j in range(len(R))]
    # 5.3 - Número de Requisições
    nr = sum(sai)
    # 5.4 - Média Requisições
    mrs = nr / n
    # 5.5 - Máximo de Requisições que saem
    maxrs = max(sai)
    # 5.5 - Máximo de Requisições que chegam
    maxrc = max(entra)
    # 5.7 - Desvio padrão de requisições
    stdrs = st.stdev(sai)
    stdrc = st.stdev(entra)

    return [nr, mrs, maxrs, maxrc, stdrs, stdrc, lb]


def classificaGrafo(g):
    # 5.1 - Número de Nós
    n = g.number_of_nodes()
    # 5.2 - Número de Arcos
    a = g.number_of_edges()
    # 5.8 - |Arcos|/|Nos|
    r = a / n
    # 5.9 - Grau max dos nós

    ld_aux = g.degree
    ldegree = [i[1] for i in ld_aux]
    gdmax = max(ldegree)
    gdmin = min(ldegree)
    # 5.10 - Fluxo Máximo
    # 5.11 - Maior caminho mínimo

    maxmf = 0
    maxcmin = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                mxf, _ = nkx.maximum_flow(g, i, j)
                cmin = nkx.shortest_path_length(g, i, j)
                if mxf > maxmf:
                    maxmf = mxf
                if cmin > maxcmin:
                    maxcmin = cmin

    ind = [n, a, r, gdmax, gdmin, maxmf, maxcmin]

    return ind


def criaDFLearning(linst, linst_n, listaAlg, listOrd, nrep, seed):
    lobv = []
    for i in range(len(linst)):
        print(i)
        criaData(listaAlg, listOrd, nrep, linst[i], linst_n[i], seed, lobv)
        #lobv.append(obv)

    col = ['nome', 'nos', 'arcos', 'a/g', 'gmax', 'gmin', 'max_fm', 'max_cmin', 'nreq', 'mreq', 'max_reqs', 'max_reqc', 'std_reqs', 'std_reqc', 'LB', 'obj', 'metodo', 'tempo', 'semente', 'GAP']
    dfObv = pd.DataFrame(lobv, columns=col)

    return dfObv


def criaData(listaAlg, listOrd, nrep, Inst, inome, seed, observ):
    # executar todos os algoritmos, número de vezes específica e coletar o resultado
    #observ = []
    indicadores = classificaInst(Inst)

    mtd = ''
    for i in range(seed):
        for (A, O) in it.product(listaAlg, listOrd):
            metodo = h.Hsolver(A, nrep, O)
            metodo.setseed((i * 100 + 1000))
            [obj, _, _, tempo] = metodo.solvetemp(Inst)
            mtd = A + ' ' + O
            observ.append([inome] + indicadores + [obj, mtd, tempo, (i * 100 + 1000), ((obj - Inst.lb) / Inst.lb)])
    return 0
