# This is a sample Python script.
import networkx as nx
import lerInst as li
import numpy as np
import struct_graph as strgr
import linkedlist as ll
import networkx as nkx
import matplotlib.pyplot as plt
import random
import kapov as kv
import time
import gerador as G
import os
import pandas as pd
import heuristicas as h

# 1 - Executar os testes do artigo - ok
# 2 - Criar método par ler / converter  novas instâncias - ok
# 3 - Salvar todas as instâncias em pickle (pasta separada) - ok
# 4 - criar uma função para rodar uma única iteração - ok
# 4.1 - Entrada: método, parâmetros e configuração
# 4.2 - Entrada: instância
# 4.3 - Resultado de uma iteração, tempo, parâmetros de entrada e características (indicadores) da instância
# 4.4 - Retornar os resultados no formato de lista
# 5 - Criar uma função para retornar características das instâncias
# 5.1 - Número de Nós
# 5.2 - Número de Arcos
# 5.3 - Número de Requisições
# 5.4 - Média Requisições
# 5.5 - Máximo de Requisições
# 5.6 - Mínimo diferente de zero de requisições
# 5.7 - Desvio padrão de requisições
# 5.8 - |Arcos|/|Nos|
# 5.9  - Grau max dos nós


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

if __name__ == '__main__':

    #teste = '../Instâncias/pickle/eon.pickle'
    teste = 'C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instâncias\\pickle\\eon.pickle'
    Inst = strgr.lePickle(teste)

    niter = int(input('Digite o numero interções: '))
    metodo = input('Digite o nome do metodo: ')
    morde = input('Digite o nome do metodo de ordenação: ')
    #niter = 2
    #metodo = 'kapov_bfd'
    #morde = 'cm'
    if niter == 1:
        kpov = h.Hsolver(metodo, niter, morde)
        kpov.setseed(10)
        [obj, Glist, Resp, tempo] = kpov.solve1it(Inst)
    else:
        kpov = h.Hsolver(metodo, niter, morde)
        kpov.setseed(10)
        [obj, Glist, Resp, tempo] = kpov.solve(Inst)
#    for i in range(len(Resp)-1):
 #       for j in range(i+1, len(Resp)-1):
  #          for l in range(0,len(Resp[i].Cam)-1): #Transformar a lista de caminho encontrado em lista de arestas
   #             for k in range(0,len(Resp[j].Cam)-1):
    #                if Resp[i].Cam[l] == Resp[j].Cam[k] and Resp[i].Cam[l+1] == Resp[j].Cam[k+1]  and Resp[i].ig == Resp[j].ig:
     #                   print(f'Lista:{Resp[i].Cam} \t Grafo:{Resp[i].ig}')
      #                  print(f'Lista:{Resp[j].Cam} \t Grafo:{Resp[j].ig}')

    print(f'Objetivo:{obj} \t Tempo:{tempo}')


'''
    pasta = "C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instâncias - Copia1\\"
    nomes = [nome  for nome in os.listdir(pasta)]
    caminhos = [pasta + nome for nome in nomes]
    #arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    #arquivos_txt = [arq for arq in arquivos if arq.lower().endswith(".txt")]


    pastaR = "C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\ResultadosPy\\"
    nomesR = [nome[:nome.find('.txt')] +'_res.txt'  for nome in nomes]
    caminhosR = [pastaR + nome for nome in nomesR]
    #arquivosR = [arqRe for arqRe in caminhosR if os.path.isfile(arqRe)]
    #arquivosR_txt = [arqRe for arqRe in arquivosR if arqRe.lower().endswith(".txt")]


    for arq,arqRe in zip(caminhos, caminhosR): 
        I = strgr.Instancia()
        I.leTXT(arq)
        print(arq)
        for i in range(2):
            semente = 1000 + i*100
            random.seed(semente)
            Lreq = I.splitReq()

            Glist=[]   #Lista de grafos
            #n,adj,Lreq = li.lerTXT('brasil.txt') #Leitura do arquivo de dados
            Fo = float('inf') #Inicializando a Função objetivo com infinito
            #maxv2 = max([r.cmin for r in Lreq])
            maxv = max(Lreq, key = lambda maxcmin : maxcmin.cmin)
            maxcm = maxv.cmin    #Atribuindo o maior caminho minimo dos dados
            end_time = time.time() + 120
            countTimer = 0
            while time.time() < end_time:
                g = I.CriaGrafo()
                Glist.append(strgr.Rede(g,len(Glist)+1))
                if i==0:
                    with open(arqRe, 'w') as arqR:
                        arqR.write('Numero de arestas:' + str(g.number_of_edges()) + '\n')
                        arqR.write('Numero de nos:' + str(g.number_of_nodes()) + '\n\n')
        
                random.shuffle(Lreq)       #Randomizando a Lista de requisição
                Lreq.sort(key=lambda cammin: cammin.cmin,reverse=True)      #Ordenando a Lista de requisiçao em ordem decrescente em relação o Cammin
                #Lreq.sort(key=lambda cammin: (cammin.cmin,cammin.mxf),reverse=True)
                result = kv.mkapov(Lreq,Glist,I,maxcm,Fo)                 #Metodo Kapov

                if result < Fo:
                    Fo = result

                Glist.clear()

            #maxv.clear()
            with open(arqRe, 'a') as arqR:
                arqR.write('Numero de grafos utilizados:' + str(Fo) + '\n')
                arqR.write('Numero de requisições:'+ str(len(Lreq)) + '\n')
                arqR.write('Semente utilizada:' + str(semente) + '\n')
                arqR.write('\n')
            Lreq.clear()

        I.Lreq.clear()
        I.Ladj.clear()

    print(Fo)
'''
"""
    #print(g.edges(data=True)) 
    #nkx.draw(g,with_labels=True)
    #plt.show()
    #print(g.number_of_nodes())
    #print(g.nodes())
    #print(g.edges())

"""
'''
    gera = G.Gerador('geracao1.xml')
    I = gera.criaIns()
    I.imprimirTXT('teste.txt')
    g = I.CriaGrafo()
    nkx.draw(g,with_labels=True)
    plt.show()
'''
