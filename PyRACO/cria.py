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
	
		self.Ladj = []              #Lista de adjacentes
		self.r_sd = []              #Lista de requisiçoes
		if arq is not None:
			self.Leitura(arq) 


	def Leitura(self, ArqEntrada):
		nf, adjf, Lreqf = li.lerTXT(ArqEntrada)  # Leitura do arquivo de dados
		self.Ladj = adjf
		self.r_sd = Lreqf
		self.nf = nf
		self.grafo = self.criaGrafo()

	def criaEstado0(self):
		grf = copy.deepcopy(self.grafo) 
		lR = self.criaLReq()
		lelij = [0 for e in self.grafo.edges]

		self.E0 = Estado(0, grf, 1, lelij, lR)
		return copy.deepcopy(self.E0)
		
	def criaGrafo(self):
		grf = nkx.convert_matrix.from_numpy_matrix(np.array(self.Ladj), create_using=nkx.DiGraph)
		capacidade = 1 #criar capacidade
		nkx.set_edge_attributes(grf, capacidade, "capacity") # como setar a capacidade diferente para cada arco
		return grf

	def criaLReq(self):
		lr = [(s,d,self.r_sd[s][d]) for d in range(len(self.r_sd[s])) for s in range(len(self.r_sd)) if self.r_sd[s][d]>0]
		return lr

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
	def __init__(self, t, grafo, LM, listaedgeslambdaij, lr):
 		self.estagio = t
		self.grafo = grafo
		self.LambdaMax = LM
		self.lambdaij = listaedgeslambdaij # lista com o lij para cada posição da lista de edges do grafo
		self.lR = lr
 	
				
	def trasicao(self,Dec,ParInc = []):
		self.estagio += 1 
		# equações de transição
		
		self.atualiza_lr(Dec)
		self.atualiza_lambda(Dec)
		
	def atualiza_lr(self, d):
		self.lR[d.req][2] -= 1 
		if  self.lR[d.req][2] < 1:
			del self.lR[d.req]
		

	def atualiza_lambda(self, d):
	
		for edge in d.path:
			e = self.lambdaij.index(e) 
			self.lambdaij[e] += 1

		self.LambdaMax = max(self.lambdaij)
		
		for k,(i,j) in enumerate(self.grafo.edges):
			self.grafo[i][j]['capacity'] = self.LambdaMax - self.lambdaij[k] 
		
 # Para 12/08 implementar decisão e politica
		

class Decisao:
	''' Classe que organiza a decisão tomada pela politica
		Objetivos: 1) padronizar o formato da decisao
		Métodos Obrigatórios: 
				  - def imprime()
		Variáveis Obrigatórias:
				   
	'''

	def __init__(self, ParDec):
		'''
		   Construtor
		   \par ParDec - Lista de parametros resultantes do metodo de solucao
		   posição 0 - id da lista de requisição
		   posição 1 - lista de caminho
		   DEVE SER SOBRESCRITO
		'''  
		self.req = ParDec[0]
		self.path = ParDec[1]
		 
	def imprime(self):
		'''
		   Metodo que imprime as informacoes da decisao
		   DEVE SER SOBRESCRITO
		'''
		return 0 


class Politica:
	''' Classe que representa uma politica apra a solucao do problema
		Objetivos: 1) Resolver o subproblema
		Métodos Obrigatórios: 
				  - solver() 
		Variáveis Obrigatórias:
				   
	'''
	def __init__(self, ParPol):
		'''
		   Construtor
		   \par ParPol - lista com parâmetros para a politica
  
		   DEVE SER SOBRESCRITO
		'''  

	def solver(self,EstX):
		'''
		   Metodo de solucao
		   \par EstX - instancia da classe estado
		   \return - deve retornar uma instancia da classe decisao
  
		   DEVE SER SOBRESCRITO
		'''
		
		
		### QUAIS INDICADORES SERAO ALTERADO COM ALTERAÇÃO NO ESTADO
		'''
		Comprimento de onda: Tamanho do comprimento de onda máximo, par de arco (i,j) com maior utilização, 
		par de arco (i,j) com menor utilização, deficit máximo, deficit médio e deficit total, 
		max grau lógico (Req) por grau físico (arestas), médio grau lógico / grau físico;
		
		'''
		  
		return d
