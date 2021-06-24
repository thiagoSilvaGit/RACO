import struct_graph as strgr

import os

if __name__ == '__main__':
	pasta = "C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instâncias\\"
	nomes = [nome  for nome in os.listdir(pasta)]
	caminhos = [pasta + nome for nome in nomes]

	pastaR = "C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instânciaspk\\"
	nomesR = [nome[:nome.find('.txt')] +'.txt'  for nome in nomes]
	caminhosR = [pastaR + nome for nome in nomesR]
	arqRe = "C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instânciaspk\\Teste.txt"
	for arq in caminhos:
		strgr.toPickle(arqRe,arq)

	"""
	teste = "C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instânciaspk\\att.txt"

	Inst = strgr.lePickle(teste)
	print(Inst)
	"""