# This is a sample Python script.
import networkx as nx

import lerInst as li
import numpy as np
import struct_graph as strgr
import linkedlist as ll
import networkx as nkx
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

if __name__ == '__main__':

    n,adj,req,g = li.lerTXT('brasil.txt')
    capacidade = 1
    nx.set_edge_attributes(g, capacidade, "capacity")
    print(g.edges(data=True))

    #print(g.number_of_nodes())
    #print(g.nodes())
    #print(g.edges())
    teste = np.array(req)
    listaReq = []
#    listaReq = ll.Link()
    for i in range(g.number_of_nodes()):
        for j in range(g.number_of_nodes()):
            if teste[i][j]:
                mxf,cm = nkx.maximum_flow(g,i,j)
                #cm=nkx.shortest_path_length(g,i,j) #Funcao para encontrar o valor do caminho minimo
                for k in range(teste[i][j]):
                    listaReq.append(strgr.Requisicao(i,j,mxf))
            else:
                pass
print(listaReq[0].i, listaReq[0].j, listaReq[0].qtd)

