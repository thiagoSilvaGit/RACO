# -*- coding: utf-8 -*-
from re import A
import gurobipy as grb
import lerInst as li
import networkx as nkx
import numpy as np
import struct_graph as strgr
import cluster as cst
import os
import time
import sys

'''Conjuntos:
Arestas E(i,j)
Requisições R(s,d)
'''

'''Parametros:
param s{s,d}, numero de requisições entre o par (s,d)
'''
#Modelo exato
def Mrwae (LambdaT,E,V,R,r): 
#Leitura de arquiva para extrair os valores dos conjustos de arestas e requisições
#Conjunto E (arestas) e R (pares de requisições)
#Parametro r[s,d], numero de requisições entre os pares 
    ti = time.time()

    model = grb.Model()
    model.Params.LogToConsole = 0
    Ltotal = np.zeros((Inst.n,Inst.n))
    
    #r = np.array(Inst.Lreq)

    names = [f'Lambda[{i}][{j}]' for i in E for j in R]
    idVars = [(e[0],e[1],s[0],s[1]) for e in E for s in R]
    Lambda = model.addVars(idVars,vtype = grb.GRB.INTEGER, name = names)
    Lambda_max = model.addVar(vtype=grb.GRB.INTEGER, name = f'Lambda_max')
    
    model.update()

#R1(i,j) in E: Lambda_max >= sum{(s,r) in R}Lambda[i,j,s,d]
  
    for i in E:
        lhs = Lambda_max
        rhs = grb.quicksum([Lambda[i[0],i[1],j[0],j[1]] for j in R]) + LambdaT[i[0]][i[1]]    #LambdaT são os valores das interações anteriores
        model.addConstr(lhs>=rhs, name = f'R1')

#R2 (s,d) in R, i in V: sum{j in V: (i,j) in E}Lambda[i,j,s,d] - sum{j in V: (j,i) in E}Lambda[j,i,s,d] 
# = r[s,d] : i = s || -r[s,d] : i =d || 0
    for i in V:
        for k in R:
            ls1 = grb.quicksum([Lambda[(i,j,k[0],k[1])] for j in V if (i,j) in E]) 
            ls2 = grb.quicksum([Lambda[(j,i,k[0],k[1])] for j in V if (j,i) in E] )
            ls = ls1 - ls2
            if i == k[0]:
                rs =  r[k[0]][k[1]]
            elif i == k[1]:
                rs = -r[k[0]][k[1]]
            else:
                rs = 0
            model.addConstr( ls == rs, name = f'R2')  


    #Restrição nova  
    #Lambda + LambaT < VALOR
    '''for i in E:
        fls1 = grb.quicksum([Lambda[i[0],i[1],j[0],j[1]] for j in R])
        fls2 = LambdaT[i[0]][i[1]]
        fls = fls1 + fls2 
        frs = 25
        model.addConstr(fls <= frs, name = f'R3')
'''
    
    model.setObjective(expr=Lambda_max, sense= grb.GRB.MINIMIZE)
    tf = time.time() - ti
    tempo = [tf]        #Tempo criaçao
    ti = time.time()    
    model.optimize()
    tempo.append(time.time()-ti) 
    
    #print(model.status)
    if model.status != 2:
        return Ltotal, model.status

    #print(f'OBJ: {model.ObjVal}')
    for i in E:
        Ltotal[i[0]][i[1]] = sum([Lambda[i[0],i[1],j[0],j[1]].x for j in R])
            #print(f'{[i[0],i[1]]}:{sum([Lambda[i[0],i[1],j[0],j[1]].x for j in R])}')

    return Ltotal, model.status, tempo
   
#Modelo relaxado
def Mrwaerf (R,Rrl,r,rrl,LambdaT,E,V):
    

#Leitura de arquiva para extrair os valores dos conjustos de arestas e requisições
#Conjunto E (arestas) e R (pares de requisições)
#Parametro r[s,d], numero de requisições entre os pares 
   #trazer de fora 
    ti = time.time()
    model = grb.Model()
    model.Params.LogToConsole = 0
            #if Inst.Lreq[i][j] > 0:
                #R.append((i,j))
    
    #r = np.array(Inst.Lreq)
    
    Ltotal = np.zeros((Inst.n,Inst.n))
    names = [f'Lambda[{i}][{j}]' for i in E for j in R]
    idVars = [(e[0],e[1],s[0],s[1]) for e in E for s in R]
    Lambda = model.addVars(idVars,vtype = grb.GRB.INTEGER, name = names)
    Lambda_max = model.addVar(vtype=grb.GRB.INTEGER, name = f'Lambda_max')
    names = [f'Lambda[{i}][{j}]' for i in E for j in Rrl]
    idVars = [(e[0],e[1],s[0],s[1]) for e in E for s in Rrl]
    l = model.addVars(idVars,vtype = grb.GRB.CONTINUOUS, name = names)
    model.update()

#R1(i,j) in E: Lambda_max >= sum{(s,r) in R}Lambda[i,j,s,d] + sum{(sl,rl) in Rrl} l[i,j,sl,rl] + LambdaT[i,j]  
    for i in E:
        lhs = Lambda_max
        rhs = grb.quicksum([Lambda[i[0],i[1],j[0],j[1]] for j in R]) + LambdaT[i[0]][i[1]] + grb.quicksum([l[i[0],i[1],j[0],j[1]] for j in Rrl])    #LambdaT são os valores das interações anteriores
        model.addConstr(lhs>=rhs, name = f'R1')

#R2 (s,d) in R, i in V: sum{j in V: (i,j) in E}Lambda[i,j,s,d] - sum{j in V: (j,i) in E}Lambda[j,i,s,d] 
# = r[s,d] : i = s || -r[s,d] : i =d || 0
    for i in V:
        for k in R:
            ls1 = grb.quicksum([Lambda[(i,j,k[0],k[1])] for j in V if (i,j) in E]) 
            ls2 = grb.quicksum([Lambda[(j,i,k[0],k[1])] for j in V if (j,i) in E] )
            ls = ls1 - ls2
            if i == k[0]:
                rs =  r[k[0]][k[1]]
            elif i == k[1]:
                rs = -r[k[0]][k[1]]
            else:
                rs = 0
            model.addConstr( ls == rs, name = f'R2')  

#R3 (s,d) in Rrl, i in V: sum{j in V: (i,j) in E}l[i,j,s,d] - sum{j in V: (j,i) in E}l[j,i,s,d] 
# = rrl[s,d] : i = s || -rrl[s,d] : i =d || 0
    for i in V:
        for k in Rrl:
            ls1 = grb.quicksum([l[(i,j,k[0],k[1])] for j in V if (i,j) in E]) 
            ls2 = grb.quicksum([l[(j,i,k[0],k[1])] for j in V if (j,i) in E] )
            ls = ls1 - ls2
            if i == k[0]:
                rs =  rrl[k[0]][k[1]]
            elif i == k[1]:
                rs = -rrl[k[0]][k[1]]
            else:
                rs = 0
            model.addConstr( ls == rs, name = f'R3')  


    
    model.setObjective(expr=Lambda_max, sense= grb.GRB.MINIMIZE)        
    tf = time.time() - ti
    tempo = [tf]         #Tempo Criaçao     
    ti = time.time()
    model.optimize()
    tempo.append(time.time()-ti)       #Tempo execução


    #print(model.status)
    if model.status != 2:
        return Ltotal, model.status,tempo

    #print(f'OBJ: {model.ObjVal}')
    for i in E:
        Ltotal[i[0]][i[1]] = sum([Lambda[i[0],i[1],j[0],j[1]].x for j in R])
            #print(f'{[i[0],i[1]]}:{sum([Lambda[i[0],i[1],j[0],j[1]].x for j in R])}')

    return Ltotal, model.status,tempo

#Relaxacao do modelo
def relaxandfix(I,cluster):    
    E = []
    R = []
    V = []
    ti = time.time()    
    tempo = []
    lamb = np.zeros((Inst.n, Inst.n))
    Ltotal = np.zeros((Inst.n,Inst.n))
    Lreq = I.splitReq()
    for i in range(I.n):
        V.append(i)
        for j in range (I.n):
            if I.Ladj[i][j]:
                E.append((i,j))
    tf = time.time() - ti
    tempo.append(tf)
    ti = time.time()
    for idc,req in enumerate(cluster):
        ti = time.time()
        R = []
        r = np.zeros((I.n,I.n))
        for i in req:
            if (Lreq[i].i,Lreq[i].j) not in R:
                R.append((Lreq[i].i,Lreq[i].j))
            r[Lreq[i].i][Lreq[i].j] = 1 + r[Lreq[i].i][Lreq[i].j]

        Rrl = []
        rrl = np.zeros((I.n,I.n))
        for k in range(idc+1,len(cluster)):
            for i in cluster[k]:
                if (Lreq[i].i,Lreq[i].j) not in Rrl:
                    Rrl.append((Lreq[i].i,Lreq[i].j))
                rrl[Lreq[i].i][Lreq[i].j] = 1 + rrl[Lreq[i].i][Lreq[i].j]
        tf = time.time() - ti
        tempo.append(tf)
    
        Fo, status, tempex = Mrwaerf(R,Rrl,r,rrl,lamb,E,V)
        tempo += tempex

        for j in range(Inst.n):
            for k in range(Inst.n):
                lamb[j][k] = lamb[j][k] + Fo[j][k]
    
    return lamb, status, tempo

#Funcao para a resolucao do problema exato 
def func(I,cluster):
    E = []             #Lista de arestas
    V = []             #Lista de vertices
    ti = time.time()
    tempo = []
    lamb = np.zeros((Inst.n, Inst.n))       #Inicializando lambda com todos os indices zerados
    Ltotal = np.zeros((Inst.n,Inst.n))      #Inicializando o resultado final com todos os indices zerados 
    Lreq = I.splitReq()
    for i in range(I.n):
        V.append(i)
        for j in range (I.n):
            if I.Ladj[i][j]:
                E.append((i,j))

    tf = time.time() - ti        #tempo de criaçao E/V
    ti = time.time()
    tempo.append(tf)
    for i in range(len(cluster)):
        R = []
        r = np.zeros((I.n,I.n))
        ti = time.time()
        for k in cluster[i]:
            if (Lreq[k].i,Lreq[k].j) not in R:
                R.append((Lreq[k].i,Lreq[k].j))
            r[Lreq[k].i][Lreq[k].j] = 1 + r[Lreq[k].i][Lreq[k].j]
        tempo.append(time.time() - ti)             #Tempo parametro
        Lbd, status, tempex = Mrwae(lamb, E, V, R, r)
        tempo += tempex
        for j in range(Inst.n):
            for k in range(Inst.n):
                lamb[j][k] = lamb[j][k] + Lbd[j][k]

    return lamb,status,tempo

if __name__ == '__main__':
    pasta = sys.argv[1]           #Instancias
    nomes = [nome for nome in os.listdir(pasta)]
    caminhos = [pasta + nome for nome in nomes]
    nomesI = [nome[:nome.find('.pickle')] for nome in nomes]
    resp = sys.argv[2]      #Resuultados
    met = sys.argv[3]       #Metodo de resolucao exato/relaxado
    nclt = int(sys.argv[4])      #Numero de requisicoes por cluster
    
    for Na, arq in enumerate(caminhos):
        Inst = strgr.lePickle(arq)
        lintemp = ""
        tempin = time.time()
        clt = cst.fcluster(arq,nclt)
        tcf = time.time() - tempin
        if met == 'ex':   
            lamb, status, tempo = func(Inst,clt)
        elif met == 'rf':
            lamb, status, tempo = relaxandfix(Inst,clt)

        lintemp += f'Tempo de criacao E/V:{tempo[0]:.4f}\n'
        tempoTexe = 0
        tempoTcria = 0 
        tempoTpar = tempo[0]
        for i in range(len(clt)):
            #lintemp += f'\t{i}-Tempo de criacao R/r:{tempo[3*i + 1]}\n'
            #lintemp += f'\t{i}-Tempo de criacao modelo:{tempo[3*i + 2]:.4f}\n'
            #lintemp += f'\t{i}-Tempo de criacao execucao:{tempo[3*i + 3]:.4f}\n'
            tempoTpar += tempo[3*i + 1]
            tempoTexe += tempo[3*i + 3] 
            tempoTcria += tempo[3*i + 2] 
            
        lintemp += f'Tempo total: {sum(tempo):.4f}\n'
        lintemp += f'Tempo total criacao: {tempoTcria:.4f}\n'
        lintemp += f'Tempo total execucao: {tempoTexe:.4f}\n'
        lintemp += f'Tempo de clusterizacao:{tcf:.4f}\n'  
        lintemp += f'Tempo total parametro: {tempoTpar:.4f}\n'        
        if status != 2:
            with open(resp, 'a') as arqR:
                arqR.write('Arquivo:' + str(nomesI[Na]) + '\n')
                arqR.write('Numero de clusters gerados: ' + str(len(clt)) + '\n')
                arqR.write('Instancia inviavel codigo de status: ' + str(status) + '\n\n')
        
        else:
            with open(resp, 'a') as arqR:
                arqR.write('Arquivo:' + str(nomesI[Na]) + '\n')
                arqR.write('Numero de clusters gerados: ' + str(len(clt)) + '\n')
                arqR.write('Função objetivo: ' + str(max([valor for linha in lamb for valor in linha])) + '\n\n')
                arqR.write(lintemp + '\n')

        #print(max([valor for linha in lamb for valor in linha]))