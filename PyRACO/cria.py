# -*- coding: utf-8 -*-

import lerInst as li
import numpy as np

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
	def __init__(self, lR, matAdj, matrsd, LM, matlambdaij):
        self.Ladj = matAdj
        self.r_sd = matrsd
        self.R = self.criaSetReq()
 	    self.grafo = self.criaGrafo()


	def Leitura(self, ArqEntrada):
        nf, adjf, Lreqf = li.lerTXT(ArqEntrada)  # Leitura do arquivo de dados
        self.Ladj = np.array(adjf)
        self.r_sd = np.array(Lreqf)


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
    def __init__(self, t, lR, matAdj, matrsd, LM, matlambdaij):
        self.R = self.criaSetReq()
        self.Ladj = matAdj
        self.r_sd = matrsd
        self.LambdaMax = LM
        self.lambdaij = matlambdaij
 	    self.grafo = self.criaGrafo()
 	    self.estagio = t
 	
    def criaGrafo(self):
        grafo = nkx.convert_matrix.from_numpy_matrix(
            self.Ladj, create_using=nkx.DiGraph)
        capacidade = 1 #criar capacidade
        nkx.set_edge_attributes(grafo, capacidade, "capacity")
    
        return grafo

    def criaSetReq(self):
        lr = [(s,d) for d in range(len(self.r_sd[s])) for s in range(len(self.r_sd[s])) if self.r_sd[s][d]>0]
        return lr
        		
	def trasicao(self,Dec,ParInc = []):
		self.estagio += 1 
		# equações de transição

        
