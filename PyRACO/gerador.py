import numpy
import struct_graph as strgr
from  numpy.random import binomial as nbin
from numpy.random import choice as chc
from numpy.random import rand as rnd
import lerInst as li
import networkx as nkx



class Gerador:
	def __init__(self, arq):

		dictGen = li.LerXMLGen(arq)
		self.n = dictGen['NumNos']
		self.MaxGrau = dictGen['MaxGrau']
		self.Densidade = dictGen['Densidade']
		self.NumReq = dictGen['NumReq']
		self.Maxreq = dictGen['Maxreq']			#Retirar?
		self.prob = dictGen['Prob']				#Probabilidade do par O/D ser req
		self.MinReq = dictGen['MinReq']
		self.FatReqm = dictGen['FatReqm']       #NUmero de req
		self.FatACm = dictGen['FatACm']			#Numero max de req

	def criaIns(self):


		I = strgr.Instancia()

		#Criação da rede da intancia
		#Ladj = [[0]*self.n for ni in range(self.n)]
		#L = [[0]*self.n for ni in range(self.n)]
	
		'''for i in range(self.n):
			for j in range(i+1,self.n):
				aresta = nbin(1,self.Densidade)
				grau = sum(Ladj[i][k] for k in range(self.n))
				if grau < self.MaxGrau:  
				Ladj[i][j] = aresta
				Ladj[j][i] = aresta'''
		
		g = nkx.gnp_random_graph(self.n, self.Densidade)		
		Ladj = nkx.to_numpy_array(g,dtype=int) 
		I.Ladj = Ladj

		#Criaçaõ das requisições da instancia
		nr = self.n*(self.n-1)*(1+ self.FatReqm)
		N = list(range(self.n))
		A = [(i,j) for i in N for j in N if i!=j] 		#todas possíveis requisiçoes
		R = [a for a in A if rnd()<self.prob] 			#Definiçao das req utilizando prpb

		if len(R)<self.MinReq: #obdecer o min_reqs
			Ri = chc(list(range(len(A))), size=self.MinReq)
			R = [A[r] for r in Ri]

		max_req = int((nr/len(R) ) * (1+ self.FatACm) )+ 1
		nODreq = len(R)

		uR = rnd(nODreq)
		nR = uR * nr / sum(uR)
		nR = [max(1, min(int(i),max_req)) for i in nR] #número de requisições por par
		snR = sum(nR)

		while snR > nr:
			k = numpy.random.randint(len(nR)-1)
			if nR[k]>1:
				nR[k] = nR[k] -1
				snR = snR -1

		while snR < nr:
			k = numpy.random.randint(len(nR)-1)
			if nR[k]<max_req:
				nR[k] = nR[k] +1
				snR = snR +1

		#Lreq = numpy.zeros((self.n,self.n))
		Lreq = [[0] * self.n for i in range(self.n)]
		for rid, r in enumerate(R):
			i = r[0]
			j = r[1]
			Lreq[i][j] = nR[rid]

		I.Lreq = Lreq
		I.n = self.n

		return I
