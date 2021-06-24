
import random 
import struct_graph as strgr
import networkx as nkx
import numpy as np
import matplotlib.pyplot as plt

class kapov:

	def solve(self,Lreq,Glist,I,Maxv,melhor):

		mc = []     #Lista para converter a lista do caminho em lista de arestas encontrado
		auxCamin = []

		for k in range(len(Lreq)-1):
			ig = 0 #Auxiliar para percorrer a lista de grafo
			caminho = False # Indicador se encontrou o caminho da requisição
			mincam = float('inf')
			while not caminho:
				if(nkx.has_path(Glist[ig].Grafo,Lreq[k].i,Lreq[k].j)):      #Verifica a existencia de caminho entre a origem e destino no grafo atual
					Camin = nkx.shortest_path(Glist[ig].Grafo,Lreq[k].i,Lreq[k].j)
					tamanho = len(Camin)-1      #Tamanho do caminho encontrado para origem e destino

				else:
					tamanho = float('inf')

				if tamanho == Lreq[k].cmin:
					for l in range(0,len(Camin)-1): #Transformar a lista de caminho encontrado em lista de arestas
						mc.append((Camin[l],Camin[l+1]))
					Glist[ig].Grafo.remove_edges_from(mc)
					mc.clear()
					Camin.clear()
					caminho = True

				elif tamanho <= Maxv or mincam <= Maxv: #Verifica se o caminho encontrado é menor que o maior caminho minimo da instancia
					if tamanho < mincam:
						mincam = tamanho
						auxg = ig
						auxCamin.clear()
						auxCamin = Camin.copy()
						Camin.clear()
						if Glist[ig].numg == len(Glist):
							for l in range(0,len(auxCamin)-1): #Transformar a lista de caminho encontrado em lista de arestas
								mc.append((auxCamin[l],auxCamin[l+1]))
							Glist[auxg].Grafo.remove_edges_from(mc)
							mc.clear()
							auxCamin.clear()
							caminho = True
						else:
							ig = ig + 1

					elif (Glist[ig].numg < len(Glist)):   #Verifica se o grafo atual é o ultimo grafo da lista
						ig = ig + 1
						Camin.clear()

					elif (Glist[ig].numg == len(Glist)):
						for l in range(0,len(auxCamin)-1): #Transformar a lista de caminho encontrado em lista de arestas
							mc.append((auxCamin[l],auxCamin[l+1]))
						Glist[auxg].Grafo.remove_edges_from(mc)
						mc.clear()
						auxCamin.clear()
						caminho = True

				elif (Glist[ig].numg < len(Glist)):   #Verifica se o grafo atual é o ultimo grafo da lista
					ig = ig + 1
					Camin.clear()

				elif (Glist[ig].numg == len(Glist)):  #Verifica se o grafo atual é o ultimo grafo da lista
					if len(Glist) == melhor-1:        #Verifica se o numero de grafos ja criado é igual a melhor solução atual
						Camin.clear()
						return melhor
					else:
						g = I.CriaGrafo()
						Glist.append(strgr.Rede(g,len(Glist)+1))
						Camin.clear()
						ig = ig + 1

		return len(Glist)


