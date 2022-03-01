import struct_graph as strgr
from  numpy.random import binomial as nbin
from numpy.random import choice as chc
import lerInst as li
import random



class Gerador:
	def __init__(self, arq):

		dictGen = li.LerXMLGen(arq)
		self.n = dictGen['NumNos']
		self.MaxGrau = dictGen['MaxGrau']
		self.Densidade = dictGen['Densidade']
		self.NumReq = dictGen['NumReq']
		self.Maxreq = dictGen['Maxreq']


	def criaIns(self):

		I = strgr.Instancia()

		Ladj = [[0]*self.n for ni in range(self.n)]
		for i in range(self.n):
			for j in range(i+1,self.n):
				aresta = nbin(1,self.Densidade)
				grau = sum(Ladj[i][k] for k in range(self.n))
				if grau < self.MaxGrau:  
					Ladj[i][j] = aresta
					Ladj[j][i] = aresta
		I.Ladj = Ladj
		reqpercapta = self.NumReq/(self.n*(self.n-1))
		if self.Maxreq <= reqpercapta:
			self.Maxreq = reqpercapta+1

		Lreq = [[0] * self.n for ni in range(self.n)]

		Preq = []

		for i in range(self.n):
			for j in range(self.n):
				if i != j:
					Preq.append((i,j))

		prob = 0.2
		for i in range(self.NumReq):
			ok = False
			while not ok:
				#o, d = chc(range(self.n), 2, replace=False) maneira antiga de escolha do par origem/destino
				ind = nbin(len(Preq), prob, 1)
				o, d = Preq[ind[0]]
				if Lreq[o][d] < self.Maxreq:
					ok = True
					Lreq[o][d]+=1
					if Lreq[o][d] == self.Maxreq:
						del(Preq[ind[0]])
		I.Lreq = Lreq
		I.n = self.n

		return I
