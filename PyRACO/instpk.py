# -*- coding: utf-8 -*-

import struct_graph as strgr
import os

if __name__ == '__main__':
    lb = []
    pasta = "C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instâncias\\"
    #pasta = '../Instâncias/'
    nomes = [nome for nome in os.listdir(pasta)]
    caminhos = [pasta + nome for nome in nomes]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    nomesR = [nome[nome.find('Instâncias\\') + len('Instâncias\\'):nome.find('.txt')] + '.pickle' for nome in arquivos]
    pastapk = pasta + "pickle\\"
    #pastapk = pasta + "pickle/"
    arqLB = "C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\LB.txt"
    with open(arqLB, 'r') as f:
        flines = f.readlines()
        for x in range(50):
            f0split = flines[x].split()
            lb.append([f0split[0] + '.pickle', int(f0split[1])])

    for ida, arq in enumerate(arquivos):
        I = strgr.Instancia()
        for x in range(50):
            if nomesR[ida] == lb[x][0]:
                best = lb[x][1]
        I.leTXT(arq, best)
        arqpk = pastapk + nomesR[ida]
        strgr.toPickle(arqpk, I)

    #teste = "C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instâncias\\pickle\\zib54.pickle"
    #teste = '../Instâncias/pickle/att.pickle'
    #Inst = strgr.lePickle(teste)
    #print(Inst.lb)