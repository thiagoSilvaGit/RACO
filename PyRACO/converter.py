import numpy as np
import os
if __name__ == '__main__':

	pasta = "C:\\Users\\Artur Alvarenga\\Desktop\\instances\\set_z\\"
	nomes = [nome  for nome in os.listdir(pasta)]
	caminhos = [pasta + nome for nome in nomes]
	arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
	arquivos_net = [arq for arq in arquivos if arq.lower().endswith(".net")]

	#pastaC = "set_wC\\"
	#nomesC = [nome[:nome.find('.net')] +'.txt'  for nome in nomes]
	#caminhosC = [pastaC + nome for nome in nomesC]

	arq = "C:\\Users\\Artur Alvarenga\\Desktop\\instances\\set_y\\Y.5.5.net"
	#for arq in arquivos_net:

	with open(arq, 'r') as f:
		flines = f.readlines()
		f0split = flines[0].split()
		nnodes = int(f0split[0])
		nedges = int(f0split[1])
		matrizA = np.zeros((nnodes,nnodes), dtype=int)
		for x in range(nedges):
			f0split = flines[x+1].split()
			i = int(f0split[0])
			j = int(f0split[1])
			matrizA[i,j] = 1
	arqCV = arq[:arq.find('.5.net')] +'.100.5.txt' 
	with open(arqCV, 'w') as o:
		o.write(str(nnodes) + '\n\n')
		for l in range(nnodes):
			for k in range(nnodes):
				o.write(str(matrizA[l][k]) + '\t' )
			o.write('\n')	
	
	file = arq[:arq.find('.5.net')] +'.100.5.trf'
	with open(file, 'r') as o:
		flines = o.readlines()
		f0split = flines[0].split()
		nreq = int(f0split[0])
		
		matrizR = np.zeros((nnodes,nnodes), dtype=int)
		for h in range(nreq):
			f0split = flines[h+1].split()
			i = int(f0split[0])
			j = int(f0split[1])
			matrizR[i,j] = matrizR[i,j] + 1

	with open(arqCV, 'a') as o:
		o.write('\n')
		for l in range(nnodes):
			for k in range(nnodes):
				o.write(str(matrizR[l][k]) + '\t' )
			o.write('\n')	
			



	print(nreq)
	

