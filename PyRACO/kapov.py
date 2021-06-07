
import random 
import struct_graph as strgr
import networkx as nkx
import numpy as np
import matplotlib.pyplot as plt

def mkapov(Lreq,Glist,Adj,Maxv,melhor):

	mc = []     #Lista para converter a lista do caminho em lista de arestas encontrado
	
	
	for k in range(len(Lreq)-1):
		ig = 0 #Auxiliar para percorrer a lista de grafo
		caminho = True # Indicador se encontrou o caminho da requisição

		while caminho:
			
			if(nkx.has_path(Glist[ig].Grafo,Lreq[k].i,Lreq[k].j)):      #Verifica a existencia de caminho entre a origem e destino no grafo atual
				Camin = nkx.shortest_path(Glist[ig].Grafo,Lreq[k].i,Lreq[k].j)
				tamanho = len(Camin)-1      #Tamanho do caminho encontrado para origem e destino
			
			else:
				tamanho = float('inf')
			
			if(tamanho <= Maxv): #Verifica se o caminho encontrado é menor que o maior caminho minimo da instancia 
				for l in range(0,len(Camin)-1): #Transformar a lista de caminho encontrado em lista de arestas
					mc.append((Camin[l],Camin[l+1]))
				
				Glist[ig].Grafo.remove_edges_from(mc)
				mc.clear()
				Camin.clear()
				caminho = False

			elif (Glist[ig].numg < len(Glist)):   #Verifica se o grafo atual é o ultimo grafo da lista
				ig = ig + 1
				Camin.clear()

			elif (Glist[ig].numg == len(Glist)):  #Verifica se o grafo atual é o ultimo grafo da lista    
				if len(Glist) == melhor-1:        #Verifica se o numero de grafos ja criado é igual a melhor solução atual
					Camin.clear()
					return melhor
				else:
					g = strgr.CriaGrafo(Adj)
					Glist.append(strgr.Rede(g,len(Glist)+1))
					Camin.clear()
					ig = ig + 1

	return len(Glist)   


