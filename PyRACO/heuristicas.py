# -*- coding: utf-8 -*-

import kapov as kp
import numpy as np
import time
import struct_graph as strgr
import random
import copy
import criaantes as cra
import criasemlim as csl

def switch_bf(argument):
    switcher = {
        'kapov_bfd': kp.kapovBFD,
        'kapov_ffd': kp.kapovFFD,
        'criaantes_bfd': cra.criaBFD,
        'criaantes_ffd': cra.criaFFD,
        'criasemlim_bfd': csl.criaslBFD,
        'criasemlim_ffd': csl.criaslFFD,
    }

    obj = switcher.get(argument, lambda *args: "Invalid Algoritm")
    return obj()



class Hsolver():

    def __init__(self,metodo,niter,mord):
        self.solver = switch_bf(metodo)
        self.niter = niter
        self.ord = mord
        self.semente = 0

    def setseed(self,i):
        self.semente = 1000 + i * 100

    def solve(self,I):
        self.tinit = time.time()
        bGl = []
        bLr = []
        random.seed(self.semente)
        Lreq = I.splitReq()
        Fo = np.inf  # Inicializando a Função objetivo com infinito
        maxv = max(Lreq, key=lambda maxcmin: maxcmin.cmin)
        maxcm = maxv.cmin  # Atribuindo o maior caminho minimo dos dados


        for i in range(self.niter):
            Glist = []  # Lista de grafos
            Lresp = []  # Lista com os caminhos e os indices dos grafos da requisições
            g = I.CriaGrafo()
            Glist.append(strgr.Rede(g, len(Glist) + 1))
            random.shuffle(Lreq)  # Randomizando a Lista de requisição
            if self.ord == 'cm':
                Lreq.sort(key=lambda cammin: cammin.cmin, reverse=True)  # Ordenando a Lista de requisiçao em ordem decrescente em relação o Cammin
            elif self.ord == 'fm':
                Lreq.sort(key=lambda cammin: cammin.mxf)
            elif self.ord == 'cm_fm':
                Lreq.sort(key=lambda cammin: (cammin.cmin,cammin.mxf),reverse=True)
            elif self.ord == 'fm_cm':
                Lreq.sort(key=lambda cammin: (cammin.mxf,cammin.cmin),reverse=True)

            result = self.solver.solve(Lreq, Glist, I,Lresp, maxcm, Fo)  # Metodo Kapov
            if result < Fo:
                Fo = result
                bGl = Glist
                bLr = Lresp




        tfim = time.time() - self.tinit
        return [Fo,bGl,bLr,tfim]

    def solve1it(self, I):
        self.tinit = time.time()
        random.seed(self.semente)
        Lreq = I.splitReq()
        Lresp = []  # Lista com os caminhos e os indices dos grafos da requisições
        maxv = max(Lreq, key=lambda maxcmin: maxcmin.cmin)
        maxcm = maxv.cmin  # Atribuindo o maior caminho minimo dos dados
        Glist = [strgr.Rede(I.CriaGrafo(), 1)]  # Lista de grafos
        random.shuffle(Lreq)  # Randomizando a Lista de requisição
        
        if self.ord == 'cm':
            Lreq.sort(key=lambda cammin: cammin.cmin, reverse=True)  # Ordenando a Lista de requisiçao em ordem decrescente em relação o Cammin
        elif self.ord == 'fm':
            Lreq.sort(key=lambda cammin: cammin.mxf)
        elif self.ord == 'cm_fm':
            Lreq.sort(key=lambda cammin: (cammin.cmin,cammin.mxf),reverse=True)
        elif self.ord == 'fm_cm':
            Lreq.sort(key=lambda cammin: (cammin.mxf,cammin.cmin),reverse=True)
        
        result = self.solver.solve(Lreq, Glist, I,Lresp, maxcm, np.inf)  # Metodo Kapov
        tfim = time.time() - self.tinit

        return [result, Glist,Lresp, tfim]

