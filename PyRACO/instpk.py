import struct_graph as strgr

import os

if __name__ == '__main__':
	
	pasta = "C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instâncias\\"
	#pasta = '../Instâncias/'
	nomes = [nome  for nome in os.listdir(pasta)]
	caminhos = [pasta + nome for nome in nomes]
	arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
	nomesR = [nome[nome.find('Instâncias\\') + len('Instâncias\\'):nome.find('.txt')] + '.pickle' for nome in arquivos]
	pastapk = pasta+ "pickle\\"
	#pastapk = pasta + "pickle/"

	for ida,arq in enumerate(arquivos):
		I = strgr.Instancia()
		I.leTXT(arq)
		arqpk = pastapk + nomesR[ida]
		print(arqpk)
		strgr.toPickle(arqpk ,I)

	

	#teste = "C:\\Users\\Artur Alvarenga\\Documents\\GitHub\\RACO\\Instânciaspk\\att.txt"
	#teste = '../Instâncias/pickle/att.pickle'
	#Inst = strgr.lePickle(teste)
	#print(Inst.Lreq)

