# -*- coding: utf-8 -*-
import networkx as nkx
class Requisicao:
    def __init__(self, org,dest,qtd):
        self.i = org
        self.j = dest
        self.qtd = qtd


class Rede:
	def __init__(self, g=[],lr=[]):
        self.lReq = lr
        self.Grafo = g
    def lerlReq(arq):
        return 0
    def lerGrafo(arq):
        return 0

class Resposta:
    def __init__(self):
        self.lgrafos = []
        self.attReq = []


