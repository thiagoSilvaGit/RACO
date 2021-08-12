# -*- coding: utf-8 -*-

import lerInst as li
import numpy as np
import copy 
class Problema:
	''' Classe com os parametros que definem a instancia do problema
		Objetivo: Gerenciar a instância do problema
		Métodos Obrigatórios: 
				 - Leitura
				 - ImprimeResultados
				 - SalvaResultados
		Variáveis Obrigatórias:
				 - Arquivo de entrada
				 - Nome da Instância			

	'''
	def __init__(self, arq = None):
	
		self.Ladj = []
		self.r_sd = []
		if arq is not None:
			self.Leitura(arq) 


	def Leitura(self, ArqEntrada):
		nf, adjf, Lreqf = li.lerTXT(ArqEntrada)  # Leitura do arquivo de dados
		self.Ladj = adjf
		self.r_sd = Lreqf
		self.nf = nf

	def criaEstado0(self):
		matlambdaij = [[0 for i in range(nf)] for j in range(nf)]
		self.E0 = Estado(0,  self.Ladj, self.r_sd, 1, matlambdaij))
		return copy.deepcopy(self.E0)
		
	def ImprimeResultados(self):
		'''
			Metodo para impressao de resultados da analise
			DEVE SER SOBRESCRITO
		'''
		return 0 

	def SalvaResultados(self, ArqSaida):
		'''
			Metodo para escrita detalhada de resultados da analise
			\par ArqSaida  - Nome do arquivo de saida
			DEVE SER SOBRESCRITO
		'''
		return 0 


class Estado:
	def __init__(self, t, matAdj, matrsd, LM, matlambdaij):
 		self.estagio = t
		self.Ladj = matAdj
		self.r_sd = matrsd
		self.LambdaMax = LM
		self.lambdaij = matlambdaij

		self.R = self.criaSetReq()
 		self.grafo = self.criaGrafo()
 	
	def criaGrafo(self):
		grafo = nkx.convert_matrix.from_numpy_matrix(
			self.Ladj, create_using=nkx.DiGraph)
		capacidade = 1 #criar capacidade
		nkx.set_edge_attributes(grafo, capacidade, "capacity") # como setar a capacidade diferente para cada arco
		for i in range(len(self.Ladj)):
			for j in range(len(self.Ladj)):
				grafo[i][j]["capacity"] = matlambda[i][j]
		return grafo

	def criaSetReq(self):
		lr = [(s,d) for d in range(len(self.r_sd[s])) for s in range(len(self.r_sd[s])) if self.r_sd[s][d]>0]
		return lr
				
	def trasicao(self,Dec,ParInc = []):
		self.estagio += 1 
		# equações de transição
		
		self.atualiza_rsd(Dec)
		self.atualiza_lambda(Dec)
	def atualiza_rsd(self, d):
		return 0
		
	def atualiza_lambda(self, d):
		return 0
		
 # Para 12/08 implementar decisão e politica
		

		
