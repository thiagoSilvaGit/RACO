# -*- coding: utf-8 -*-
import random
import struct_graph as strgr
import networkx as nkx
import numpy as np
import matplotlib.pyplot as plt
import kapov as kv


class criaBFD:

    def solve(self, Lreq, Glist, I, LR, Maxv, melhor):
        if(melhor == np.inf):
            result = kv.kapovBFD.solve(self, Lreq, Glist, I, LR, Maxv, np.inf)
            melhor = result + 1
            LR.clear()

        Glist.clear()
        for x in range(melhor-1):
            g = I.CriaGrafo()
            Glist.append(strgr.Rede(g, len(Glist)+1))

        mc = []  # Lista para converter a lista do caminho em lista de arestas encontrado
        auxCamin = []

        for k in range(len(Lreq)):
            ig = 0  # Auxiliar para percorrer a lista de grafo
            caminho = False  # Indicador se encontrou o caminho da requisição
            mincam = float('inf')
            while not caminho:
                # Verifica a existencia de caminho entre a origem e destino no grafo atual
                if(nkx.has_path(Glist[ig].Grafo, Lreq[k].i, Lreq[k].j)):
                    Camin = nkx.shortest_path(
                        Glist[ig].Grafo, Lreq[k].i, Lreq[k].j)
                    # Tamanho do caminho encontrado para origem e destino
                    tamanho = len(Camin)-1

                else:
                    tamanho = float('inf')

                if tamanho == Lreq[k].cmin:
                    # Transformar a lista de caminho encontrado em lista de arestas
                    for l in range(0, len(Camin)-1):
                        mc.append((Camin[l], Camin[l+1]))
                    LR.append(strgr.Resp(Camin.copy(), Glist[ig].numg))
                    Glist[ig].Grafo.remove_edges_from(mc)
                    mc.clear()
                    Camin.clear()
                    caminho = True

                # Verifica se o caminho encontrado é menor que o maior caminho minimo da instancia
                elif tamanho <= Maxv or mincam <= Maxv:
                    if tamanho < mincam:
                        mincam = tamanho
                        auxg = ig
                        auxCamin.clear()
                        auxCamin = Camin.copy()
                        Camin.clear()
                        if Glist[ig].numg == len(Glist):
                            # Transformar a lista de caminho encontrado em lista de arestas
                            for l in range(0, len(auxCamin)-1):
                                mc.append((auxCamin[l], auxCamin[l+1]))
                            LR.append(strgr.Resp(
                                auxCamin.copy(), Glist[auxg].numg))
                            Glist[auxg].Grafo.remove_edges_from(mc)
                            mc.clear()
                            auxCamin.clear()
                            caminho = True
                        else:
                            ig = ig + 1

                    # Verifica se o grafo atual é o ultimo grafo da lista
                    elif (Glist[ig].numg < len(Glist)):
                        ig = ig + 1
                        Camin.clear()

                    elif (Glist[ig].numg == len(Glist)):
                        # Transformar a lista de caminho encontrado em lista de arestas
                        for l in range(0, len(auxCamin)-1):
                            mc.append((auxCamin[l], auxCamin[l+1]))
                        LR.append(strgr.Resp(
                            auxCamin.copy(), Glist[auxg].numg))
                        Glist[auxg].Grafo.remove_edges_from(mc)
                        mc.clear()
                        auxCamin.clear()
                        caminho = True

                # Verifica se o grafo atual é o ultimo grafo da lista
                elif (Glist[ig].numg < len(Glist)):
                    ig = ig + 1
                    Camin.clear()

                # Verifica se o grafo atual é o ultimo grafo da lista
                elif (Glist[ig].numg == len(Glist)):
                    Camin.clear()
                    return melhor

        return len(Glist)


class criaFFD:

    def solve(self, Lreq, Glist, I, LR, Maxv, melhor):
        if(melhor == np.inf):
            result = kv.kapovBFD.solve(self, Lreq, Glist, I, LR, Maxv, np.inf)
            melhor = result + 1
            LR.clear()

        Glist.clear()
        for x in range(melhor-1):
            g = I.CriaGrafo()
            Glist.append(strgr.Rede(g, len(Glist)+1))

        mc = []  # Lista para converter a lista do caminho em lista de arestas encontrado

        for k in range(len(Lreq)):
            ig = 0  # Auxiliar para percorrer a lista de grafo
            caminho = False  # Indicador se encontrou o caminho da requisição

            while not caminho:
                # Verifica a existencia de caminho entre a origem e destino no grafo atual
                if(nkx.has_path(Glist[ig].Grafo, Lreq[k].i, Lreq[k].j)):
                    Camin = nkx.shortest_path(
                        Glist[ig].Grafo, Lreq[k].i, Lreq[k].j)
                    # Tamanho do caminho encontrado para origem e destino
                    tamanho = len(Camin)-1

                else:
                    tamanho = float('inf')

                # Verifica se o caminho encontrado é menor que o maior caminho minimo da instancia
                if(tamanho <= Maxv):
                    # Transformar a lista de caminho encontrado em lista de arestas
                    for l in range(0, len(Camin)-1):
                        mc.append((Camin[l], Camin[l+1]))
                    LR.append(strgr.Resp(Camin.copy(), Glist[ig].numg))
                    Glist[ig].Grafo.remove_edges_from(mc)
                    mc.clear()
                    Camin.clear()
                    caminho = True

                # Verifica se o grafo atual é o ultimo grafo da lista
                elif (Glist[ig].numg < len(Glist)):
                    ig = ig + 1
                    Camin.clear()

                # Verifica se o grafo atual é o ultimo grafo da lista
                elif (Glist[ig].numg == len(Glist)):
                    Camin.clear()
                    return melhor

        return len(Glist)
