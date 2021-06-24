# -*- coding: utf-8 -*-

import kapov as kp
import numpy as np
import time
import struct_graph as strgr
import random
import copy

def switch_bf(argument):
    switcher = {
        'kapov_bfd': kp.kapov,
        'kapov_ffd': kp.kapov,
    }

    obj = switcher.get(argument, lambda *args: "Invalid Algoritm")
    return obj()



class Hsolver():

    def __init__(self,metodo = 'kapov_bfd',niter = 100):
        self.solver = switch_bf(metodo)
        self.niter = niter
        self.semente = 0

    def setseed(self,i):
        self.semente = 1000 + i * 100

    def solve(self,I):
        self.tinit = time.time()
        random.seed(self.semente)
        Lreq = I.splitReq()
        Fo = float('inf')  # Inicializando a Função objetivo com infinito
        maxv = max(Lreq, key=lambda maxcmin: maxcmin.cmin)
        maxcm = maxv.cmin  # Atribuindo o maior caminho minimo dos dados


        for i in range(self.niter):
            Glist = []  # Lista de grafos
            bGl = []
            g = I.CriaGrafo()
            Glist.append(strgr.Rede(g, len(Glist) + 1))
            random.shuffle(Lreq)  # Randomizando a Lista de requisição
            Lreq.sort(key=lambda cammin: cammin.cmin, reverse=True)  # Ordenando a Lista de requisiçao em ordem decrescente em relação o Cammin
            result = self.solver.solve(Lreq, Glist, I, maxcm, Fo)  # Metodo Kapov
            if result < Fo:
                Fo = result
                bGl = Glist



        tfim = time.time() - self.tinit

        return [Fo,bGl,tfim]

    def solve1it(self, I):
        self.tinit = time.time()
        random.seed(self.semente)
        Lreq = I.splitReq()
        maxv = max(Lreq, key=lambda maxcmin: maxcmin.cmin)
        maxcm = maxv.cmin  # Atribuindo o maior caminho minimo dos dados
        Glist = [strgr.Rede(I.CriaGrafo(), 1)]  # Lista de grafos
        random.shuffle(Lreq)  # Randomizando a Lista de requisição
        Lreq.sort(key=lambda cammin: cammin.cmin, reverse=True)  # Ordenando a Lista de requisiçao em ordem decrescente em relação o Cammin
        result = self.solver.solve(Lreq, Glist, I, maxcm, np.inf)  # Metodo Kapov
        tfim = time.time() - self.tinit

        return [result, Glist, tfim]

