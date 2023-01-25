# This is a sample Python script.
import networkx as nkx
import lerInst as li
import numpy as np
import struct_graph as strgr
import linkedlist as ll
import matplotlib.pyplot as plt
import random
import kapov as kv
import time
import gerador as G
import os
import pandas as pd
import heuristicas as h
import learning as lear
import sys
#import cria



# Criar método para rodar heurística com tempo
# rodar para lista de instâncias com todas as combinações de método  e 10 segundos
# Adaptar as sementes e alterar o criaDFlearning para rodar com mais de uma semente por instância

# Desenvolver modelos de classificação


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

if __name__ == '__main__':

	#/home/ICEA/05792717656/RACO	
	#teste = '../Instâncias/pickle/att.pickle'
	#teste = 'C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instâncias\\pickle\\eon.pickle'
	#Inst = strgr.lePickle(teste)

	Linst = []
	pasta = sys.argv[1]           #Instancias
	#pasta = '../Instâncias/pickle/'
	#pasta = "C:\\Users\\Artur Alvarenga\\Documents\\RACO\\Instâncias\\pickle\\"
	nomes = [nome for nome in os.listdir(pasta)]
	caminhos = [pasta + nome for nome in nomes]
	nomesI = [nome[:nome.find('.pickle')] for nome in nomes]
	nrep = int(sys.argv[2]) #numero de repetições / tempo de interação 
	seed = int(sys.argv[3]) #semente 
	saida = sys.argv[4]     #saida

	for k,arq in enumerate(caminhos):
		Linst.append(strgr.lePickle(arq))
		Linst[k].lb =22 #gambiarra
	

	Lmet = ['kapov_bfd', 'kapov_ffd', 'criaantes_bfd', 'criaantes_ffd', 'criasemlim_bfd', 'criasemlim_ffd']
	Lord = ['cm', 'fm', 'cm_fm', 'fm_cm']

	dfobv = lear.criaDFLearning(Linst, nomesI, Lmet, Lord, nrep, seed)
	#dfobv = lear.criaDFLearning([Inst, Inst], ['eon', 'eon'], ['kapov_bfd', 'kapov_ffd'], ['cm', 'fm'], 10, 3)

	#print(dfobv)
	dfobv.to_csv(saida)
