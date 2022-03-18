# -*- coding: utf-8 -*-
from re import A
import gurobipy as grb
import lerInst as li
import networkx as nkx
import numpy as np
import struct_graph as strgr
import cluster as cst
'''Conjuntos:
Arestas E(i,j)
Requisições R(s,d)
'''

'''Parametros:
param s{s,d}, numero de requisições entre o par (s,d)
'''

def Mrwae (req,I,LambdaT): 
#Leitura de arquiva para extrair os valores dos conjustos de arestas e requisições
#Conjunto E (arestas) e R (pares de requisições)
#Parametro r[s,d], numero de requisições entre os pares 
    
    model = grb.Model()
    model.Params.LogToConsole = 0
    E = []
    R = []
    V = []
    Ltotal = np.zeros((Inst.n,Inst.n))
    Lreq = I.splitReq()
    for i in range(I.n):
        V.append(i)
        for j in range (I.n):
            if I.Ladj[i][j]:
                E.append((i,j))
            #if Inst.Lreq[i][j] > 0:
                #R.append((i,j))
    
    #r = np.array(Inst.Lreq)
    r = np.zeros((I.n,I.n))
    for i in req:
        if (Lreq[i].i,Lreq[i].j) not in R:
            R.append((Lreq[i].i,Lreq[i].j))
        r[Lreq[i].i][Lreq[i].j] = 1 + r[Lreq[i].i][Lreq[i].j]

    names = [f'Lambda[{i}][{j}]' for i in E for j in R]
    Lambda = model.addVars(E,R,vtype = grb.GRB.BINARY, name = names)
    Lambda_max = model.addVar(vtype=grb.GRB.INTEGER, name = f'Lambda_max')
    model.update()

#R1(i,j) in E: Lambda_max >= sum{(s,r) in R}Lambda[i,j,s,d]
  
    for i in E:
        lhs = Lambda_max
        rhs = grb.quicksum([Lambda[i[0],i[1],j[0],j[1]] for j in R])   
        model.addConstr(lhs>=rhs, name = f'R1')

#R2 (s,d) in R, i in V: sum{j in V: (i,j) in E}Lambda[i,j,s,d] - sum{j in V: (j,i) in E}Lambda[j,i,s,d] 
# = r[s,d] : i = s || -r[s,d] : i =d || 0
    for i in V:
        for k in R:
            ls1= grb.quicksum([Lambda[i,j,k[0],k[1]] for j in V if (i,j) in E]) 
            ls2= grb.quicksum([Lambda[j,i,k[0],k[1]] for j in V if (j,i) in E] )
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
    for i in E:
        fls1 = grb.quicksum([Lambda[i[0],i[1],j[0],j[1]] for j in R])
        fls2 = LambdaT[i[0]][i[1]]
        fls = fls1 + fls2 
        frs = 25
        model.addConstr(fls <= frs, name = f'R3')

    model.update()
    
    model.setObjective(expr=Lambda_max, sense= grb.GRB.MINIMIZE)
    model.update()        
    
    model.optimize()

    
    print(f'OBJ: {model.ObjVal}')
    for i in E:
        Ltotal[i[0]][i[1]] = sum([Lambda[i[0],i[1],j[0],j[1]].x for j in R])
            #print(f'{[i[0],i[1]]}:{sum([Lambda[i[0],i[1],j[0],j[1]].x for j in R])}')

    return Ltotal
   

if __name__ == '__main__':
    arq = 'C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instâncias\\pickle\\eon.pickle'
    Inst = strgr.lePickle(arq)
    clt = cst.fcluster(arq)
    lamb = np.zeros((Inst.n, Inst.n))
    for i in range(len(clt)):
        Lbd = Mrwae(clt[i], Inst, lamb)
        
        for j in range(Inst.n):
            for k in range(Inst.n):
                lamb[j][k] = lamb[j][k] + Lbd[j][k]
     
    print(max([valor for linha in lamb for valor in linha]))