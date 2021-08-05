#coding: utf-8

import TPD.TemplatePD as tpd
import sys
import math
import random
import numpy as np
import copy as c
from numpy.random import standard_normal, normal
from numpy import array, zeros, sqrt, shape, eye
from Leitor.leitorXML import * #importa arquivo leitorXML
import csv
from pprint import pprint
import time
import matplotlib.pyplot
import basisfunction as bf
import numpy.linalg as npla
import numpy.random as nrd
from scipy.optimize import least_squares

def stpsze_ln50up100(it):
	ss = 0.5 + min(it/200,0.5)
	return ss

def stpsze_ln100dn80(it):
	ss = 1 - min(it/500,0.2)
	return ss

def stpsze_cte1(it):
	return 1

def switch_stpsze(argument):
	switcher = {
		'ln50up100': stpsze_ln50up100, 
		'ln100dn80': stpsze_ln100dn80,
		'cte1': stpsze_cte1
	}
	return switcher.get(argument, lambda *args: "Invalid Lambda")

#---------------------------------------------------------------------------------------
#reescrever essa classe
class Gerador(tpd.Gerador):
	def __init__(self):
		x=0
#---------------------------------------------------------------------------------------

##@b Classe Silo 
#@brief Parâmetros que definem os silos
class Silo():
##@b Método Construtor
#@brief Parâmetros dos silos
#@details
#@param name nome do silo
#@param Vol_ini volume inicial do silo
#@param L_inf limite inferior do silo
#@param L_sup limite superior do silo
	def __init__(self, name, Vol_ini, L_inf, L_sup):
		self.name=name;
		self.Vol_ini=Vol_ini
		self.L_inf=L_inf
		self.L_sup=L_sup
		self.hist_nvl=[] #cria a lista de histórico de níveis
		self.nvl=Vol_ini

##@b Método atualiza_nvl
#@brief Atualiza o nível dos silos
#@details Atualiza o nível do silo e o adiciona à lista hist_nvl
#@param nvl nível do silo
	def atualiza_nvl(self,nvl):
		self.hist_nvl.append(self.nvl)
		self.nvl=nvl #atualiza o nível

##@b Método save_hist
#@brief Cria um arquivo de histórico dos níveis
	def save_hist():
		fname = 'hist_{}.csv'.format(self.name)
		with open(fname,'wb') as myfile:
			wr = csv.writer(myfile, quoting = csv.QUOTE_ALL)
			wr.writerow(['Estágio',self.name])
			for h in range(len(self.hist_nvl)):
				wr.writerow([h,self.hist_nvl])


##@b Classe Problema
#@brief Parâmetros que definem a instância do problema
#@details Faz a leitura do arquivo de entrada, e salva os dados
class Problema(tpd.Problema):

##@b Método Construtor
#@brief Parâmetros da instância
#@param te taxa de entrada do silo, lista com o nome e parâmetros da distribuição
#@param ts taxa de saída do silo, lista com o nome e parâmetros da distribuição
#@param vel velocidade do tripper
#@param P_ini posição inicial do tripper
#@param y1 coeficiente da folga positiva
#@param y2 coeficiente da folga negativa
#@param caminho pasta do teste
	def __init__(self, te, ts, vel, P_ini, y1, y2, c):
		
		self.distTe = te[0]  # t[0] nome da função de distribuição
		self.parTe = te[1:]  # t[1:] restante da lista com os parâmetros da distribuição
		self.distTs = ts[0]  # t[0] nome da função de distribuição
		self.parTs = ts[1:]  # t[1:] restante da lista com os parâmetros da distribuição
		self.vel = vel       # velocidade do triper
		self.P_ini =P_ini
		self.y1 = y1
		self.y2 = y2
		self.lst_silos = [] #lista de silos - nome, volume inicial e limites inferior e superior
		self.caminho = c


##@b Método Leitura
#@brief Faz o carregamento dos dados das instâncias
#@param ArqEntrada arquivo da instância
	def Leitura(self,ArqEntrada):
		Instancia = LerXML(ArqEntrada) #Instancia recebe a leitura do arquivo da instância
		distte = Instancia["Problema"]["distTe"] # Tem que jogar no Switch !!!!!
		parte =  Instancia["Problema"]["parTe"]
		self.te = [distte] + parte #cria te como uma lista com o nome e os parametros

		distts = Instancia["Problema"]["distTs"] # Tem que jogar no Switch !!!!!
		parts =  Instancia["Problema"]["parTs"]
		self.ts = [distts] + parts

		self.vel = Instancia["Problema"]["Velocidade"]
		self.P_ini = Instancia["Problema"]["P_ini"]
		self.y1 = Instancia["Problema"]["y1"]
		self.y2 = Instancia["Problema"]["y2"]
		#self.lst_silos = [] #lista de silos
		for i in Instancia["Silo"]: #para cada silo:
			self.lst_silos.append(Silo(i["@name"],i["Vol_ini"],i["L_inf"],i["L_sup"])) #adiciona à lst_silos nome, volume inicial e limites inferior e superior de cada silo
		
		

##@b Classe Estado
#@brief Representa o estado do sistema
#@details Armazena as variáveis de estado, faz a transição entre os estágios e calcula a função objetivo
class Estado(tpd.Estado):

##@b Método Construtor
#@brief Parâmetros da instância
#@details Atualiza o nível inicial dos silos, os adiciona à lista hist_nvl e calcula as folgas
#@param silos lst_silos
#@param p_ini posição do tripper
	def __init__(self, silos, p_ini, dt):
		self.silos=[]
		self.silos= c.deepcopy(silos) #silos é uma cópia de lst_silos, recebido como parâmetro

		for i in range (len(self.silos)): #inicializa os níveis e o histórico de níveis
			self.silos[i].nvl=self.silos[i].Vol_ini
			self.silos[i].hist_nvl.append(self.silos[i].Vol_ini) #adiciona o volume inicial à lista de histórico de níveis

		self.pos = p_ini
		self.A = [] #cria lista da folga
		self.B = []

		for i in range(len(self.silos)): #cálculo das folgas de cada silo
			self.A.append(max(self.silos[i].nvl-self.silos[i].L_sup,0)) #atualiza as folgas
			self.B.append(max(self.silos[i].L_inf-self.silos[i].nvl,0))
		self.tau = 0.0
		self.deltat = dt

##@b Método Xrandom
#@brief Gera estado de forma aleatória
	def Xrandom(self):
		total = sum([self.silos[i].nvl for i in range(len(self.silos))])
		lnvl = [random.randint(0,10) for i in range(len(self.silos))]
		total2= sum(lnvl)
		volinc= [total*lnvl[k]/(total2) for k in range(len(self.silos))]
		lsilos = [Silo(str(k),volinc[k], self.silos[k].L_inf, self.silos[k].L_sup) for k in range(len(self.silos))]
		self.silos= c.deepcopy(lsilos)
		self.pos = random.randint(1,len(self.silos))

##@b Método Calc
#@brief Cálculo da fo
#@details Penalização pelas folgas
#@param lpar lista de parâmetros do problema = [y1, y2, te, ts]
#@retval ret valor do cálculo da função objetivo
	def Calc(self,lpar):
		y1 = lpar[0]
		y2 = lpar[1]
		ret = 0
		for i in range(len(self.silos)): #função objetivo: acumulado das penalizações das folgas de cada silo
			ret = ret  + y1*self.A[i] + y2*self.B[i]
		return ret

	def GraficoLinha(self):
		plt.pyplot.plot( self.hist_nvl)
		plt.pyplot.show()
		return 1
#-----------------------------------------------------------------------------
##@b Método Volume de passagem
#@brief Calcula a quantidade a ser depositada pelo tripper nos silos que estão no caminho
#@details Verifica se o silo corrente está no caminho a ser percorrido. Se sim, retorna o volume a ser depositado
#@param i silo de origem
#@param j silo de destino
#@param k silo corrente
#@param te taxa de entrada
#@param t tempo que o tripper fica sobre o silo
#@retval volume a ser depositado
	def volPassagem(self,i,j,k,te,t):
		orig = i
		dest = j
		at = k+1
		te = te 
		t = t  
		
		if orig<dest:
		    if orig < at < dest: #verifica se o silo atual está no caminho		        
		        aux = 1
		    else:		        
		        aux = 0
		else:		    
		    if dest < at < orig:		        
		        aux = 1
		    else:		        
		        aux = 0
		
		return aux*(te*t)# retorna o volume

#------------------------------------------------------------------------------
##@b Método transicao
#@brief Realiza a transição entre os estados
#@details Atualiza as variáveis, depois de tomada a decisão - Gera a incerteza, calcula a nova posição do tripper, atualiza os níveis e as folgas de cada silo
#@param d instância da classe decisao
#@param lpar lista de parâmetros do problema = [y1, y2, Te, Ts, vel]
#@retval d.custo custo da transição
	def transicao(self,d,lpar):

		y1 = lpar[0]
		y2 = lpar[1]
		Te = lpar[2]
		Ts = lpar[3] 
		vel = lpar[4]
		
		#incerteza = GeraIncerteza(['lognormal',10,2],['normal',10,2])
		incerteza = GeraIncerteza(Te,Ts) #QUANDO TIVER O ARQUIVO DA INSTANCIA PRONTO
		saida = incerteza.gerar() #gera as incertezas
		te = saida[0]
		ts = saida[1]
#		while True:
#			if te < (len(self.silos)-0.2)*ts:
#				saida = incerteza.gerar() #gera as incertezas
#				te = saida[0]
#			else:
#				break
		#print(f"te: {te}")
		#print(f"ts: {ts}")
		
		ori = self.pos

		# Passagem de estagio
		#print('\nTransição:')
		#print('estágio {}  - posição {}'.format(self.estagio,self.pos)) #estagio: estagio atual do sistema, pos = posição atual do tripper
		#print('decisão: {}'.format(d.x)) #decisão tomada: movimento escolhido para ser realizado
		self.estagio = self.estagio+1 #atualiza o estágio para o próximo
		w = self.pos + d.x #cálculo da nova posição (posicao+movimento)
		self.pos=w #atualiza a posição
		#print(f"Nova p0sição: {w}")
		#print('estágio {}  - posição {}'.format(self.estagio,self.pos)) #imprime o estágio e a posição nova
		#print('custo da decisão {} \n'.format(d.custo)) #custo de ter tomado a decisão sem as políticas
		#----------------------------------------------------------------------------------------
		#ACRESCENTAR CALCULO TEMPO DE RELOGIO como TEMPO DE DESLOCAMENTO
		delta = abs(d.x)/vel #calculo do tempo de deslocamento		
		self.tau = self.tau + delta + d.duracao #calculo do tempo de relógio
		#----------------------------------------------------------------------------------------		
		#----------------------------------------------------------------------------------------
		#NO NIVEL DO SILO (s_vol), CONSIDERAR TEMPO DE DESLOCAMENTO DELTA, TAXA DE PASSAGEM SE ESTIVER NO CAMINHO, INCERTEZAS E DURAÇÃO DA ALIMENTAÇÃO d(x)
		if d.x == 0:
			t = 0
		else:
			t = self.deltat # tempo que o tripper fica sobre cada silo
		
		for i in range(len(self.silos)): #para cada silo:
			tp = self.volPassagem(ori,w,i,te,t)
			if self.pos ==(i+1) : #testa se a posição do tripper é a posição do silo. Se v:
				s_vol = self.silos[i].nvl + (te - ts)*d.duracao + tp - delta*ts #cálculo do novo nível
				s_vol = max(s_vol, 0) #deixa os niveis dentro dos limites de capacidade
				s_vol = min(s_vol, 100)
				self.silos[i].nvl = s_vol

				self.silos[i].hist_nvl.append(s_vol)
				self.A[i] = (max(s_vol - self.silos[i].L_sup, 0))  # atualiza folga
				self.B[i] = (max(self.silos[i].L_inf - s_vol, 0))  # atualiza folga

			else: #se o tripper não está sobre o silo:
				s_vol = self.silos[i].nvl - ts*d.duracao + tp - delta*ts
				s_vol = max(s_vol, 0)
				s_vol = min(s_vol, 100)
				self.silos[i].nvl = s_vol
				self.silos[i].hist_nvl.append(s_vol)				
				self.A[i] = (max(s_vol - self.silos[i].L_sup, 0))  # atualiza folga
				self.B[i] = (max(self.silos[i].L_inf - s_vol, 0))  # atualiza folga
		#----------------------------------------------------------------------------------------
		#print("Níveis: ", end=" ")
		#for i in range(len(self.silos)):			
			#print(self.silos[i].nvl, end=" ")
		#print()
		return d.custo #retorna o custo da transição

##@b Classe Decisao
#@brief Organiza a decisão tomada pela politica, padronizando a decisão
class Decisao(tpd.Decisao):
##@b Método Construtor

#@brief Parâmetros resultantes do metodo de solução (solver)
#@param x movimento escolhido
#@param r retorno com as políticas
#@param c retorno sem as politicas
#@param d duração da alimentação
	def __init__(self,x,r,c,d):
		self.x=x
		self.fit = r
		self.custo = c
		self.duracao = d
		

##@b Classe GeraIncerteza
#@brief Gera as incertezas das taxas de entrada e saída
class GeraIncerteza:

##@b Método Construtor
#@brief 
#@param lparE lista de parâmetros da taxa de entrada [nome da distribuição, parâmetros da distribuição]
#@param lparS lista de parâmetros da taxa de saída [nome da distribuição, parâmetros da distribuição]
	def __init__(self, lparE, lparS):
		self.te = self.switch_dist(lparE[0]) #escohe a distribuição pra te
		self.ts = self.switch_dist(lparS[0]) #escolhe a distribuição pra ts
		self.lE = lparE[1:] #parametros da distribuição
		self.lS = lparS[1:]
		
	def cte(self,par):
		return par[0]
	def norm(self, par): 
		saida = nrd.normal(par[0],par[1])
		return saida
	def logn(self, par):
		saida = nrd.lognormal(par[0],par[1])
		return saida   
	def gamma(self, par):
		saida = nrd.gamma(par[0],par[1])
		return saida
	def beta(self, par):
		saida = nrd.beta(par[0],par[1])
		return saida 
	def uni(self, par):
		saida = nrd.uniform(par[0],par[1])
		return saida

	def switch_dist(self,argument):
		switcher = {
			'normal': self.norm,
			'lognormal': self.logn,
			'gamma':  self.gamma,
			'beta': self.beta,
			'uniform': self.uni,
			'cte': self.cte
		}
		return switcher.get(argument, lambda *args: "Invalid distribution")

##@b Método gerar
#@brief Gera as incertezas
#@details Chama a distribuição e retorna a incerteza
#@retval rte incerteza taxa de entrada
#@retval rts incerteza taxa de saída
	def gerar(self):
		rte = self.te(self.lE) #chama a função da distribuição
		rts = self.ts(self.lS)
		return [rte,rts] 


##@b Classe politica
#@brief Políticas para a resolução do problema
class politica():
##@b Método Construtor
#@param lbs lista das basisfunction - cada elemento da lista é o endereço de uma função  	#lembrar que lbs[0] é a constante (1)
#@param lcoef lista dos coeficientes das políticas
#@param gam
#@param lamb:  função com protótipo (float) lambdam(int it) para definir o lambda para a atualização de B
	def __init__(self,lbs,lcoef,gam,lamb,dt,c,lind):
		self.lBasis = lbs
		self.B = eye(len(lcoef)) #B: matriz identidade de dimensão = tamanho de lcoef
		self.Theta = array(lcoef) #theta = lcoef (binária - 1 se a basis function será usada) array cria arranjo de dados numéricos
		#print('Theta: {}'.format(self.Theta))
		self.gamma = gam #gamma = fator de desconto
		self.lambdam = lamb #lambda = stepsize eq.9.31 pg.352
		self.deltat = dt #variação de t pra o método de solução 
		self.it=0
		self.itp = 0
		self.caminho = c
		self.log = 0
		self.lind = lind
	
	def setLog(self,b):
		self.log = b
		
	def resetB(self):
		self.B = eye(len(self.lBasis))
		return 0
	
	def valesp_n(self,par): # retorna a média distribuição normal 
		return par[0]

	def valesp_l(self,par): #calcula a média distribuição lognormal 
		return math.exp(par[0]+(par[1]**2/2))

	def valesp_g(self,par): 
		return par[0]/par[1]
		
	def valesp_b(self,par): 
		return par[0]/(par[0]+par[1])
		
	def valesp_u(self,par): 
		return (par[0]+par[1])/2
		
	def valesp_c(self,par):
		return par[0]

	def switch_valesp(self,argument):
		switcher = {
			'normal': self.valesp_n, 
			'lognormal': self.valesp_l,
			'gamma': self.valesp_g,
			'beta': self.valesp_b, 
			'uniform': self.valesp_u, 
			'cte': self.valesp_c
		}
		return switcher.get(argument, lambda *args: "Invalid distribuition")

#---------------------------------------------------------------------------------------------
##@b Método retorno
#@brief Calcula o custo da decisão
#@details Com base no destino e duração calcula o custo da política gulosa e os custos das demais políticas
#@param EstX instância da classe Estado
#@param lpar lista de parâmetros do problema 
#@param dest silo de destino
#@param dur tempo de alimentação
#@retval r custo da política gulosa
#@retval r2 custo das políticas implementadas
	def retorno(self,EstX,lpar,dest,dur):		
		dest = dest
		l_silo=[]
		l_silo = c.deepcopy(EstX.silos) #copia de silos = lst_silos [nome, volume inicial e limites inferior e superior]
		EstX2 = c.deepcopy(EstX) #copia de EstX
		EstX2.pos = dest+1 #atualiza a posição
		y1 = lpar[0]
		y2 = lpar[1]
		Te = lpar[2] #lista da distribuição de te 
		Ts = lpar[3] #lista da distribuição de ts
		vel = lpar[4]
		r=0
		f1=[]
		f2=[]
		dx = dur
		#print(f"dx: {dx}")
		#print(f"Posição antes: {EstX.pos}")
		#print(f"Posição depois: {EstX2.pos}")
		self.nte = Te[0] #nome da distribuição te
		self.pte = Te[1:] #parâmetros da distribuição te
		self.nts = Ts[0]
		self.pts = Ts[1:]
		
		
		self.teesp = self.switch_valesp(self.nte) #escolhe a função de distribuição
		self.tsesp = self.switch_valesp(self.nts)
		te = self.teesp(self.pte) #chama a função e recebe a média
		ts = self.tsesp(self.pts)
		#print(f"te: {te}")
		#print(f"ts: {ts}")
#		while True: #AQUI TAMBÉM?? OU SÓ NA TRANSIÇÃO??
#			if te < (len(EstX.silos)-0.2)*ts:
#				te = self.teesp(self.pte)
#			else:
#				break

		for i in range(len(l_silo)): # cálculo das folgas de cada silo:
			f1.append(max((l_silo[i].nvl-l_silo[i].L_sup),0))
			f2.append(max((l_silo[i].L_inf-l_silo[i].nvl),0))
			
		delta = abs(EstX.pos-EstX2.pos)/vel #calculo do tempo de deslocamento		
		EstX2.tau = EstX2.tau + delta + dx #calculo do tempo de relógio
		#print(f"delta: {delta}")
		#print(f"tau: {EstX2.tau}")
		
		if abs(EstX.pos-EstX2.pos) == 0:
			t = 0
		else:
			t = self.deltat #calculo do tempo que o tripper fica sobre cada silo
		
		
		#print('Posic: {}  - mov: {} - posi: {}'.format(Posic,mov,EstX2.pos))
		for i in range(len(EstX2.silos)): #para cada silo
			tp = EstX2.volPassagem(EstX.pos,EstX2.pos,i,te,t)
			#print(f"tp silo {i+1}: {tp}")
			if EstX2.pos ==(i+1) : #testa de a posição corrente é  a posição atual do silo. Se v:
				s_vol = EstX2.silos[i].nvl + (te - ts)*dx + tp - delta*ts #calcula o nível do silo
				EstX2.silos[i].nvl= max(s_vol,0) #atualiza nível
				EstX2.silos[i].nvl = min(s_vol, 100)
				EstX2.silos[i].nvl = s_vol
				EstX2.silos[i].hist_nvl.append(s_vol)
				EstX2.A[i]=( max(s_vol -EstX2.silos[i].L_sup,0)) #atualiza folga
				EstX2.B[i]=( max(EstX2.silos[i].L_inf-s_vol ,0)) #atualiza folga

			else: #se o tripper nao está sobre o silo:
				s_vol = EstX2.silos[i].nvl - ts*dx + tp - delta*ts
				EstX2.silos[i].nvl =  max(s_vol,0)
				EstX2.silos[i].nvl = min(s_vol, 100)
				EstX2.silos[i].nvl = s_vol
				EstX2.silos[i].hist_nvl.append(s_vol)
				EstX2.A[i]=( max(s_vol -EstX2.silos[i].L_sup,0))
				EstX2.B[i]=( max(EstX2.silos[i].L_inf - s_vol ,0) )

		#print("Níveis: ", end=" ")
		#for i in range(len(EstX2.silos)):			
			#print(EstX2.silos[i].nvl, end=" ")
		#print()
		
		r = EstX2.Calc(lpar) #r = valor da fo = custo sem as politicas 
		listaBasis = [self.lBasis[i](EstX2,lpar) for i in range(len(self.lBasis))] # chama cada política, e adiciona seu retorno à listaBasis
		#print(f"Retorno das políticas: {listaBasis}")
		lr2 = [listaBasis[i]*self.Theta[i] for i in range(len(self.lBasis))]
		#print(f"lr2: {lr2}")
		#print('lr2: {}'.format(lr2))
		r2 = sum(lr2) #soma o vetor lr2
		#print ('Soma dos retornos das políticas:',r2)
		r2 = r2 + r #soma com o valor de r pra saber qual movimento produz os melhores resultados considerando-se todas as politicas
		#print ('Soma dos retornos das políticas com o custo do movimento:',r2)

		return [r,r2] #retorna r=custo da politica gulosa e r2=custo de usar as políticas
#---------------------------------------------------------------------------------------------
	
	def derExpP(self,dx, EstX,j,lpar):
		l_nvl = []		
		j = j+1 #atualiza a posição
		x = 0
		vel = lpar[4]
		Te = lpar[2] #lista da distribuição de te 
		Ts = lpar[3] #lista da distribuição de ts
		self.nte = Te[0] #nome da distribuição te
		self.pte = Te[1:] #parâmetros da distribuição te
		self.nts = Ts[0]
		self.pts = Ts[1:]		
		self.teesp = self.switch_valesp(self.nte) #escolhe a função de distribuição
		self.tsesp = self.switch_valesp(self.nts)
		te = self.teesp(self.pte) #chama a função e recebe a média
		ts = self.tsesp(self.pts)
		
		for i in range(len(EstX.silos)): #copia os niveis
			l_nvl.append(EstX.silos[i].nvl)
				
		if abs(EstX.pos-j) == 0:
			t = 0
		else:
			t = self.deltat #calculo do tempo que o tripper fica sobre cada silo		
		delta = abs(EstX.pos-j)/vel #calculo do tempo de deslocamento		
		for i in range(len(l_nvl)): #atualiza os níveis
			tp = EstX.volPassagem(EstX.pos,j,i,te,t)
			if j ==(i+1) : #testa de a posição corrente é  a posição atual do silo. Se v:
				s_vol = l_nvl[i] + (te - ts)*dx + tp - delta*ts #calcula o nível do silo
				l_nvl[i] = max(s_vol,0) #atualiza nível
				l_nvl[i] = min(s_vol, 100)
				l_nvl[i] = s_vol
			else: #se o tripper nao está sobre o silo:
				s_vol = l_nvl[i] - ts*dx + tp - delta*ts
				l_nvl[i] =  max(s_vol,0)
				l_nvl[i] = min(s_vol, 100)
				l_nvl[i] = s_vol	
		
		for i in range(len(l_nvl)):	#calculo da derivada	
			x += 0.1*(te-ts)*math.exp(0.1*(l_nvl[i] + (te - ts)*dx - delta*ts - 60))
			#print(f"x={x}")
		return x
		
		
	def derExpN(self,dx,EstX,j,lpar):
		l_nvl = []		
		j = j+1 #atualiza a posição
		x = 0
		vel = lpar[4]
		Te = lpar[2] #lista da distribuição de te 
		Ts = lpar[3] #lista da distribuição de ts
		self.nte = Te[0] #nome da distribuição te
		self.pte = Te[1:] #parâmetros da distribuição te
		self.nts = Ts[0]
		self.pts = Ts[1:]		
		self.teesp = self.switch_valesp(self.nte) #escolhe a função de distribuição
		self.tsesp = self.switch_valesp(self.nts)
		te = self.teesp(self.pte) #chama a função e recebe a média
		ts = self.tsesp(self.pts)
		
		for i in range(len(EstX.silos)):
			l_nvl.append(EstX.silos[i].nvl)
				
		if abs(EstX.pos-j) == 0:
			t = 0
		else:
			t = self.deltat #calculo do tempo que o tripper fica sobre cada silo		
		delta = abs(EstX.pos-j)/vel #calculo do tempo de deslocamento		
		for i in range(len(l_nvl)):
			tp = EstX.volPassagem(EstX.pos,j,i,te,t)
			if j ==(i+1) : #testa de a posição corrente é  a posição atual do silo. Se v:
				s_vol = l_nvl[i] + (te - ts)*dx + tp - delta*ts #calcula o nível do silo
				l_nvl[i] = max(s_vol,0) #atualiza nível
				l_nvl[i] = min(s_vol, 100)
				l_nvl[i] = s_vol
			else: #se o tripper nao está sobre o silo:
				s_vol = l_nvl[i] - ts*dx + tp - delta*ts
				l_nvl[i] =  max(s_vol,0)
				l_nvl[i] = min(s_vol, 100)
				l_nvl[i] = s_vol	
		
		for i in range(len(l_nvl)):		
			x += 0.1*(te-ts)*math.exp(-0.1*(l_nvl[i] + (te - ts)*dx - delta*ts - 40))
			#print(f"x={x}") 
		return x
	
	def derG(self,dx,EstX,j,lpar):
		#print("\t ####### GULOSA:")
		l_nvl = []		
		j = j+1 #atualiza a posição
		x = 0
		vel = lpar[4]
		y1 = lpar[0]
		y2 = lpar[1]
		Te = lpar[2] #lista da distribuição de te 
		Ts = lpar[3] #lista da distribuição de ts
		self.nte = Te[0] #nome da distribuição te
		self.pte = Te[1:] #parâmetros da distribuição te
		self.nts = Ts[0]
		self.pts = Ts[1:]		
		self.teesp = self.switch_valesp(self.nte) #escolhe a função de distribuição
		self.tsesp = self.switch_valesp(self.nts)
		te = self.teesp(self.pte) #chama a função e recebe a média
		ts = self.tsesp(self.pts)
		#print(f"\t\t[y1,y2,Te,Ts] = [{y1}{y2}{Te}{Ts}]")
		#print(f"\t\t[te,ts] = [{te}{ts}]")
		
		for i in range(len(EstX.silos)):
			l_nvl.append(EstX.silos[i].nvl)
		#print(f"Níveis: {l_nvl}")
		
		if abs(EstX.pos-j) == 0:
			t = 0
		else:
			t = self.deltat #calculo do tempo que o tripper fica sobre cada silo		
		delta = abs(EstX.pos-j)/vel #calculo do tempo de deslocamento		
		for i in range(len(l_nvl)):
			tp = EstX.volPassagem(EstX.pos,j,i,te,t)
			if j ==(i+1) : #testa de a posição corrente é  a posição atual do silo. Se v:
				s_vol = l_nvl[i] + (te - ts)*dx + tp - delta*ts #calcula o nível do silo
				l_nvl[i] = max(s_vol,0) #atualiza nível
				l_nvl[i] = min(s_vol, 100)
				l_nvl[i] = s_vol
			else: #se o tripper nao está sobre o silo:
				s_vol = l_nvl[i] - ts*dx + tp - delta*ts
				l_nvl[i] =  max(s_vol,0)
				l_nvl[i] = min(s_vol, 100)
				l_nvl[i] = s_vol
		#print(f"Níveis: {l_nvl}")		
		
		for i in range(len(l_nvl)):		
		    if l_nvl[i] > EstX.silos[i].L_sup:
			    x += y1*(te-ts)
		    elif l_nvl[i] < EstX.silos[i].L_inf:
			    x += -y2*(te-ts)
		    else:
			    x += 0
		#print(f"x = {x}")

		return x
	
	def derDesvP(self,dx, EstX,j,lpar):
		#print("DESVIO")
		l_nvl = []		
		j = j+1 #atualiza a posição		
		soma = 0
		Te = lpar[2] #lista da distribuição de te
		Ts = lpar[3] #lista da distribuição de ts
		vel = lpar[4] 
		self.nte = Te[0] #nome da distribuição te
		self.pte = Te[1:] #parâmetros da distribuição te
		self.nts = Ts[0]
		self.pts = Ts[1:]	
		self.teesp = self.switch_valesp(self.nte) #escolhe a função de distribuição
		self.tsesp = self.switch_valesp(self.nts)
		te = self.teesp(self.pte) #chama a função e recebe a média
		ts = self.tsesp(self.pts)
		
		for i in range(len(EstX.silos)):
			l_nvl.append(EstX.silos[i].nvl)
				
		if abs(EstX.pos-j) == 0:
			t = 0
		else:
			t = self.deltat #calculo do tempo que o tripper fica sobre cada silo		
		delta = abs(EstX.pos-j)/vel #calculo do tempo de deslocamento		
		for i in range(len(l_nvl)):
			tp = EstX.volPassagem(EstX.pos,j,i,te,t)
			if j ==(i+1) : #testa de a posição corrente é  a posição atual do silo. Se v:
				s_vol = l_nvl[i] + (te - ts)*dx + tp - delta*ts #calcula o nível do silo
				l_nvl[i] = max(s_vol,0) #atualiza nível
				l_nvl[i] = min(s_vol, 100)
				l_nvl[i] = s_vol
			else: #se o tripper nao está sobre o silo:
				s_vol = l_nvl[i] - ts*dx + tp - delta*ts
				l_nvl[i] =  max(s_vol,0)
				l_nvl[i] = min(s_vol, 100)
				l_nvl[i] = s_vol
		
		for i in range(len(l_nvl)):	
			soma=soma+l_nvl[i] #soma os níveis dos silos
		vbar = soma / len(l_nvl)
		#print(f"soma:{soma}")
		#print(f"vbar:{vbar}")		
		x1 = (2*te)/len(l_nvl)
		x2 = [l_nvl[j-1] - vbar]
		x3 = x2[0]
		#print(f"x2:{x2}")
		#print(f"x3:{x3}")
		x = x1*x3
		#print(f"x={x}")

		return x
	
	
	def SolverDer(self,EstX,j,lpar): #calcula o tempo de abastecimento do silo
		#print("Entrou na SolverDer")
		dx = np.array([1.0]) #tempo inicial
		lparam = [self.lind,EstX,j,lpar]
		#print("-x-")
		t = least_squares(self.Der, dx, args=lparam,bounds=(0.5,100))
		#print("-x-x-")
		#print("saindo da SolverDer")
		return t.x[0]	
        
    #um dos paramtros: quais indicadoras estao sendo usadas - se tiver usando, soma a derivada na equação
	#FAZER UMA FUNÇÃO PRINCIPAL E COLCOAR UM IF LA PRA SABER QUAIS INDICADORAS TAO SENDO USADAS PRA SABER QUAL FUNÇÃO VAI SOMAR A DERIVADA DELA LA TAMBEM
	def Der(self, dx, lind, EstX,j,lpar): #faz a montagem da derivada, com as derivas das indicadoras usadas em relaçao a dx 
		#print('############# Função DER ############')
		#print('\t Lista de Indicadores: {}'.format(lind))
		#print('\t dx:{}'.format(dx))
		#print('\t j: {}'.format(j))
		#print('\t lpar: {}'.format(lpar))
		resd = 0
		#print("Entrou na Der")
		if "CM" in lind:
			rest = self.derG(dx, EstX,j,lpar)
			#print('\t Parcial CM: {}'.format(rest))
			resd += rest
		if "JD" in lind:
			rest = self.derDesvP(dx,EstX,j,lpar)
			#print('\t Parcial JD: {}'.format(rest))
			resd += rest
		if "CAPMAX" in lind:
			rest = self.derExpP(dx, EstX,j,lpar)
			#print('\t Parcial CAPMAX: {}'.format(rest))
			resd += rest
		if "CAPMIN" in lind:
			rest = self.derExpN(dx,EstX,j,lpar)
			#print('\t Parcial CAPMIN: {}'.format(rest))
			resd += rest

		#print('\t Der: {}'.format(resd))

		#print("######################################")
		#print("Saindo da Der")
		return resd
#---------------------------------------------------------------------------------------------
##@b Método solverSilo
#@brief Calcula a duração ótima da alimentação e o custo para o silo j
#@details 
#@param EstX instância da classe Estado
#@param lpar lista de parâmetros do problema 
#@param siloj silo a ser testado
#@retval r duração ótima, custo sem indicadoras, custo com indicadoras
	def solverSilo(self,EstX, lpar, siloj, lind):
		#resolver através da discretização do tempo
		# crescendo o tempo até o momento que começar a diminuir *** olha se pode substituir por outro método
		#para computar o custo, chama a função retorno
		j = siloj
		#print(f"Solversilo silo {j+1}")
		t = self.SolverDer(EstX,j,lpar) #calcula o tempo
		#print(f"Tempo:{t}")
		r = self.retorno(EstX,lpar,j,t) #retorna r=custo da politica gulosa e r2=custo de usar as políticas
		#print(f"Custos: {r}")
								
		r.insert(0,t) #adiciona a duracao na primeira posicao da lista de resultados
		#print(f"Retorno solver silo: silo {j+1}, duração, custo gulosa e custo com indicadoras: {r}")
		return r # retornar a duração ótima e o custo para o silo [duração, custo sem indicadoras, custo com indicadoras]
#---------------------------------------------------------------------------------------------

##@b Método solver
#@brief Soluciona o problema
#@details Testa a ida para todos os silos e escolhe o melhor deles, baseado no custo com os indicadores
#@param EstX instância da classe Estado
#@param lpar lista de parâmetros do problema
#@retval d instância da classe Decisão
	def solver(self,EstX, lpar,lind):
	    #---------------------------------------------------------------------------------------------
	    #Fazer um for para cada possível destino
	    # chamar a função solverSilo e guardar a duração e o custo em uma lista
	    # Escolher o melhor destino 
	    res1 = []
	    res2 = []
	    
	    
	    for i in range(len(EstX.silos)):	    	
	    	ss = self.solverSilo(EstX, lpar, i,lind)
	    	#print(f"Silo {i+1} - duracao, custo sem indicadoras e custo com indicadoras: {ss}") 
	    	res1.append(ss)
	    	res2.append(ss[2])
	    	
	    #print(res2)
	    ind = res2.index(min(res2)) #escolha do melhor destino: menor custo com os indicadores
	    #print(f"Melhor silo: {ind+1}" ) #PQ NA INSTANCA, OS SILOS COMECAM EM 1
	    m = res1[ind] #duração e custos do melhor destino
	    #print(f"Duração e custos do melhor silo: {m}")
	    x = ind+1 - EstX.pos #calcula o movimento a ser realizado 
	    d = Decisao(x,m[2],m[1],m[0]) #passa como parametros movimento, custo com as políticas, custo sem as politicas e duração da alimentação
	    aaa = [x,m[2],m[1],m[0]]	    
	    #print(f"Retorno da solver: {aaa}")
	    
	    return d #retorna uma instancia da classe decisao
	    #---------------------------------------------------------------------------------------------



	def calc_erro_m(self,C,fgf):
		#print('Função Calc_erro_m\n \tC: {} \n\t fgf: {} \n\t Theta:{}'.format(C,fgf,self.Theta))
		aux = npla.multi_dot([fgf,self.Theta]) #calcula o produto escalar de fgf e teta
		return C - aux #retorna o erro

	def calc_denm(self,phi,fgf): #calcula o denominador de teta
		##print("COMPARANDO DENOMNADORES:")
		m1 = np.matmul(self.B, np.transpose(np.matrix(phi)))
		m2 = np.matmul(np.matrix(fgf),m1)
		#print (m2[0,0])
		#a2 = np.transpose(fgf)
		#a3 =  np.matmul(np.matmul(fgf,self.B),phi)
		##print(a3)



		denm = self.lambdam(self.itp) + m2[0,0] # denominador ->alterado em  eq.9.31 pg.352 # lambda>1: aumenta o peso do histórico na atualização de B; lambda<1: aumenta o peso de observações recentes


		if (denm>0.0)&(denm<0.00001):
			denm +=0.01 #to avoid numerical issues;
		else:
			if (denm<0.0)&(denm >-0.00001):
				denm -=0.01; #to avoid numerical issues
		return denm

	def UpdateB_m(self,phi_m, fgf):
		texto = []
		texto.append("\n\n###############################################\n")
		texto.append('\tIT: {}\n'.format(self.it))
		texto.append('\tB: {}\n'.format(self.B))
		#print('\tshape B: {}\n'.format(self.B.shape))
		#print('\tshape phi_m: {}\n'.format(np.matrix(phi_m).shape))
		#print('\tshape fgf: {}\n'.format(np.matrix(fgf).shape))


		texto.append('\tshape B: {}\n'.format(self.B.shape))
		texto.append('\tshape phi_m: {}\n'.format(np.matrix(phi_m).shape))
		texto.append('\tshape fgf: {}\n'.format(np.matrix(fgf).shape))
		denm = self.calc_denm(phi_m,fgf) #calcula o denominador da formula de B
		texto.append('\tdenm: {}\n'.format(denm))
		mult1 = np.matmul(np.transpose(np.matrix(phi_m)),np.matrix(fgf))
		texto.append('\tmult1: {}\n'.format(mult1))
		mult2 = np.matmul(self.B,mult1)
		texto.append('\tmult2: {}\n'.format(mult2))
		mult = np.matmul(mult2,self.B)
		#print('\tmult: {}, shape {}\n'.format(mult, mult.shape))
		texto.append('\tmult: {}, shape {}\n'.format(mult, mult.shape))
		self.B = self.B - float((1/denm))*mult #atualiza B pela formula
		texto.append('\tapós atualizar B: {}\n'.format(self.B))
		if self.log:
			arquivo = self.caminho + 'Log/' + 'saida_B.txt'
			arq = open(arquivo , 'a')
			arq.writelines(texto)

			arq.close()
		del(texto)

	def UpdateTheta_m(self,erro,phi,fgf):
		texto = []
		texto.append("\n\n###############################################\n")
		texto.append('\tIT: {}\n'.format(self.it))
		texto.append('\tTheta: {}\n'.format(np.matrix(self.Theta)))
		#print('\tshape Theta: {}\n'.format(self.Theta.shape))
		#print('\tshape phi: {}\n'.format(np.matrix(phi).shape))
		#print('\tshape fgf: {}\n'.format(np.matrix(fgf).shape))

		texto.append('\tshape Theta: {}\n'.format(np.matrix(self.Theta).shape))
		texto.append('\tshape phi: {}\n'.format(np.matrix(phi).shape))
		texto.append('\tshape fgf: {}\n'.format(np.matrix(fgf).shape))

		denm = self.calc_denm(phi,fgf) #calcula o denominador

		texto.append('\tdenm: {}\n'.format(denm))
		m1 = erro*np.matmul(self.B,np.transpose(np.matrix(phi)))
		texto.append('\tm1: {}\n'.format(m1))
		m2 = (1/denm)*m1
		texto.append('\tm2: {}\n'.format(m2))
		newTh = np.matrix(self.Theta) + np.transpose(m2)
		self.Theta = array(newTh)[0]  #atualiza theta pela formula
		texto.append('\tapós atualizar Theta: {}\n'.format(self.Theta))
		if self.log:
			arquivo = self.caminho + 'Log/' + 'saida_Theta.txt'
			arq = open(arquivo, 'a')		
			arq.writelines(texto)
			arq.close()
		del(texto)

#@param S Estado
#@param lpar lista de parâmetros do problema = [y1, y2, te, ts]
	def calc_phi(self, S, lpar):

		#basis* indicadores
		phi  = [self.lBasis[i](S,lpar) for i in range(len(self.Theta))]#chama as políticas
		a_phi = array(phi)
		#print (a_phi)
		#print("-----")
		return a_phi #retorna os resultados das políticas

#@param S Estado
#@param Smp Estado após a transição
#@param lpar lista de parâmetros do problema = [y1, y2, te, ts]
	def calc_phiGammaPhi(self, S,Smp,lpar):
		phi_m = self.calc_phi( S,lpar) #calculo de phi usando o estado antes da transição
		phi_mp = self.calc_phi( Smp,lpar) #calculo de phi usando o estado depois da transição
		phiGammaPhi = phi_m - self.gamma*phi_mp # operação matricial
		return phiGammaPhi #phiGammaPhi

#@param	self Política
#@param	a retorno da classe solver [d=x,fit,custo]

#@param Sm Estado
#@param Smp1 Estado após a transição
#@param lpar lista de parâmetros do problema = [y1, y2, te, ts]
	def updPol(self,a,Sm,Smp1,lpar):
		texto = []
		texto.append("\n\n###############################################\n")
		texto.append('\tIT: {}\n'.format(self.it))
		texto.append('\tTheta: {}\n'.format(self.Theta))
		texto.append('\tB: {}\n'.format(self.B))
		
		custo = Sm.Calc(lpar) #antes da transição
		texto.append('\tC^m: {}\n'.format(custo))
		#recursive least squares
		#step 6d algoritmo 10.10 pag 407
		#custo = self.retorno(Sm,lpar,a.x) #para calcular o custo a.x:movimento a ser realizado
		##print("CONFERINDO CUSTO")
		##print(custo)

		##print(custo[1])
		##print(a.fit)
		phi_m = self.calc_phi(Sm,lpar) #chama a função calc_phi, phi_m = resultados das políticas
		texto.append('\tphi_m: {}\n'.format(phi_m))
		fgf =  self.calc_phiGammaPhi(Sm,Smp1,lpar) #chama a função calc_phiGammaPhi, #phiGammaPhi é a diferença dos valores da política antes e depois da transição ??? = fgf = passo 6d
		texto.append('\tfgf: {}\n'.format(fgf))

		#setp 7b alg 10.10 pag 407 - eq. 10.23 via rls - tem que calcular erro, b e teta
		erro = self.calc_erro_m(custo,fgf) #calcula o erro
		texto.append('\terro: {}\n'.format(erro))
		self.UpdateTheta_m(erro,phi_m, fgf) #atualiza teta
		texto.append('\tapós atualizar Theta: {}\n'.format(self.Theta))
		self.UpdateB_m(phi_m, fgf) #atualiza B
		texto.append('\tapós atualizar B: {}\n'.format(self.B))
		if self.log:
			arquivo = self.caminho + 'Log/' + 'saida_updpol.txt'
			arq = open(arquivo, 'a')
			arq.writelines(texto)

			arq.close()
		del(texto)
		return erro

	def getStatLabels(self):
		thetafb =['Theta_fb'+ str(i) for i in range(len(self.lBasis))]
		return thetafb

	def getStatistics(self):
		return self.Theta


class ADP(tpd.Trainer):

	def __init__(self,c):
		self.caminho = c
		self.log = 0
	
	def setLog(self,b):
		self.log = b

##@b approxPIA
#@brief Algoritmo da Figura 10.10 de Power(2011), Dado uma política inicial, encontra uma política "ótima" a partir de uma estratégia de #aprendizado
#@details
# --
#
#
#@param P objeto instanciado da classe Problema que possua, funções de custo, função de transição e estado

#@param B lista de basis function para gerar os indicadores de aproximação do estado
#@param A política inicial:  objeto instanciado da classe Politica que dado um estado retorna uma ação
#@param n número de iterações do Policy Iteration Algorithm
#@param m tamanho da simulção de Monte Carlo para convergência do valor
#@retval Alinha: objeto instanciado atualizado da classe Politica que dado um estado retorna uma ação
	def approxPIA(self,P,A,n,m,deltat,lind):
		texto = []
		lpar = [P.y1,P.y2,P.te,P.ts,P.vel] 
		Stat = []
		Alinha = c.deepcopy(A) #step 4: inicializar a política (lbs,lcoef,gam,lamb,deltat,caminho)
		Sm = Estado(P.lst_silos, P.P_ini,deltat)  # iniciar o estado inicial (step 2) estado inicial: P_ini e lst_silos
		for i in range(n): #para cada iteração
			texto.append("\n\n#######################################################################\n")
			texto.append("\tFunção approxPIA(self,P,A,n,m) iteração {}\n".format(i))
			texto.append("\tTheta(Alinha): {}\n".format(Alinha.Theta))
			Am = c.deepcopy(Alinha) #cópia da política
			#Am.resetB()
			Am.itp = 0
			for j in range(m):
				#print(f"Iteração: {i} {j}")
				Am.it= m*i +j
				Am.itp = Am.itp + 1
				texto.append("\t\titeração i={},j={}\n".format(i,j))
				texto.append("\t\tTheta(Am): {}\n".format(Am.Theta))
				Smp1 = c.deepcopy(Sm) #cópia do estado
				#step 5: gera a incerteza do cenário
				a = Alinha.solver(Smp1,lpar,lind) #gerar a ação com a política atual step 6a
				#custo = Alinha.retorno(Smp1,lpar,a.x) #mas a solver já chama o retorno, precisa disso??
				Smp1.transicao(a,lpar) # gerar novo estado a partir da transição do atual step 6b 
				custo = Smp1.Calc(lpar) # calcula custo real da F.O. # Alterado por Thiago 18/05/2020
				erro = Am.updPol(a,Sm,Smp1,lpar) #chama a função updPol step 6d
				texto.append("\t\tapós atualizar Theta(Am): {}\n".format(Am.Theta))
				Stat.append([custo] +[erro] + list(Am.getStatistics()) + list(Alinha.getStatistics())) #Am.getStatistics() retorna teta #tirar o indice [1] do custo - adiciona à Stat o custo e o teta atualizado
				del(Sm)
				Sm = c.deepcopy(Smp1) #estado depois da tansição vira o estado antes da transição da proxim iteração
				del(Smp1)
				print(f"Fim Iteração: {i} {j}")
			del(Alinha)
			Alinha = c.deepcopy(Am) #step 8: atualizar a política para a iteração i+1
			texto.append("\tTheta(Alinha): {}\n".format(Alinha.Theta))
			del(Am)
		self.adpStat(['custo'] + ['erro'] + Alinha.getStatLabels() + ['{}_curr'.format(i) for i in Alinha.getStatLabels()],Stat,n,m)
		#print(Alinha)
		if self.log:
			arquivo = self.caminho + 'Log/' + 'saida.txt'
			with open(arquivo, 'w', newline='') as arq:
				arq.writelines(texto)
		del(texto)
		return Alinha

	def adpStat(self,labels,Stats,n, m):
		self.StatLab = labels
		self.StatData = [[] for i in range(len(labels))] #uma lista vazia para cada label
		#print('Função adpStat:\n\t dim(Stats):{}\n\t n*m: {}'.format(len(Stats),n*m))

		#print('\n\t dim(labels):{}\n\t dim(Stats[0])n*m: {}'.format(len(labels),len(Stats[0])))
		for i in range(len(labels)): #cada label e um grafico, custo, teta1,teta2,....,teta6
			for j in range(n):
				auxn = []
				for k in range(m):
					#print('i:{}\t j:{}\t k:{}\t j*n+k: {}, Stats[j*m+k]:{}'.format(i,j,k,j*m+k,Stats[j*m+k]))
					auxn.append(Stats[j*m+k][i])
				self.StatData[i].append(auxn)

	def graficoStat(self,idStat):
		k = int((len(self.StatData) -2)/2)
		n = len(self.StatData[idStat])
		m = len(self.StatData[idStat][0])
		s= range(n*m)
		matplotlib.pyplot.figure(figsize=(30,30))
		
		matplotlib.pyplot.rcParams.update({'font.size': 40})
		
		local = self.caminho + 'Graficos/'
		if idStat == 0:
			y = [self.StatData[idStat][i][j] for i in range(n) for j in range(m)]
			matplotlib.pyplot.clf()
			matplotlib.pyplot.plot(s, y, label='custo')
			matplotlib.pyplot.title("Custo ao Longo do Tempo ")
			matplotlib.pyplot.xlabel("Estágios")
			matplotlib.pyplot.ylabel("Valor")
			matplotlib.pyplot.savefig(local+'Custo.png')
		else:
			if idStat == 1:
				y = [self.StatData[idStat][i][j] for i in range(n) for j in range(m)]
				matplotlib.pyplot.clf()
				matplotlib.pyplot.plot(s, y, label=self.StatLab[1])
				matplotlib.pyplot.title("Erro ao Longo do Tempo ")
				matplotlib.pyplot.xlabel("Estágios")
				matplotlib.pyplot.ylabel("Valor")
				matplotlib.pyplot.savefig(local + 'Erro.png')
			else:
				y1 = [self.StatData[idStat][i][j] for i in range(n) for j in range(m)]
				y2 = [self.StatData[idStat + k][i][j] for i in range(n) for j in range(m)]
				matplotlib.pyplot.clf()
				'''md = np.mean(y1) #calcula media
				sd = np.std(y1) #calcula desvio padrao
				print("--------------------------------")
				print(md)
				print(sd)
				md = float(md)
				sd = float(sd)
				print(md)
				print(sd)
				linf = md-2*sd #calcula o limite inferior como o valor da média menos duas vezes o valor do desvio padrão
				lsup = md+2*sd
				print(linf)
				print(lsup)
				linf = float(linf)
				lsup = float(lsup)'''
				

				matplotlib.pyplot.plot(s, y1, label='Variação ao longo das '+ str(m)+' iterações')
				matplotlib.pyplot.plot(s, y2, label='Variação ao longo das '+ str(n)+' iterações')
				matplotlib.pyplot.title('Coeficientes da função ' +self.StatLab[idStat]+' ao Longo do Tempo ')
				matplotlib.pyplot.xlabel("Estágios")
				matplotlib.pyplot.ylabel("Valor")
				matplotlib.pyplot.legend()
				#matplotlib.pyplot.axis([linf, lsup, 0, s]) # [xmin, xmax, ymin, ymax]
				matplotlib.pyplot.savefig(local+' função '+self.StatLab[idStat]+'.png')



##@b Classe simuladorTripper
#@brief Simula a dinâmica do processo
class simuladorTripper(tpd.Simulador):

	def __init__(self,c):
		self.caminho = c

##@b Método simulacao
#@brief Simula o processo para cada iteração
#@details Dá a decisão tomada, seu custo, e o custo total ao longo das iterações
#@param EstX instância da classe Estado
#@param pol instância da classe Política
#@param lpar lista de parâmetros do problema = [y1, y2, te, ts]
#@param niter número de iterações
#@param t tempo
#@retval custo custo de todas as iterações
	def simulacao(self, EstX,pol,lpar,niter,t,lind):
		custo = 0
		start=time.time()
		dx = 0
		for i in range (niter): #para cada iteração:
			#print("\nIteração ", i)
			y = EstX.pos
			d = pol.solver(EstX,lpar,lind) #chama a função solver, que retorna a decisão - d = instância da classe decisão - 3 elementos
			ci = EstX.transicao(d,lpar) #faz a transição dos estados - custo é o custo do movimento, sem as políticas
			custo = custo+ci #soma o custo ao longo das iterações
			#print("Custo iteração {}: {}".format(i, custo))
			dx += d.duracao
		
		end = time.time()
		t = end-start
		print("Tempo de simulação 1:",t)
		print("Somatorio dx:",dx)
		#print("Custo total da política:",custo)
		
		return custo #retorna o custo de todas as iterações
		
	def simulacao2(self, Est,pol,lpar,niter,lind):
		print("Coeficientes da politica:",pol.Theta)
		start=time.time()
		custo = 0
		Stat = [['i']+['j']+['custo'] + pol.getStatLabels() + ['silo_{}'.format(k) for k in range(len(Est.silos))] +['pos']+ ['dx']]
		for i in range (niter): #para cada iteração:
			Est.Xrandom()
			custo = Est.Calc(lpar)
			stat = [i]+[0]+[custo] + [pol.lBasis[k](Est,lpar) for k in range(len(pol.lBasis))] + [Est.silos[k].nvl for k in range(len(Est.silos))] + [Est.pos] + [0]
			Stat.append(stat)

			for j in range(100):
				d = pol.solver(Est,lpar,lind) #chama a função solver, que retorna a decisão - d = instância da classe decisão - 3 elementos
				ci = Est.transicao(d,lpar) #faz a transição dos estados - custo é o custo do movimento, sem as políticas
				custo = Est.Calc(lpar)
				stat = [i]+[j+1]+[custo] + [pol.lBasis[k](Est,lpar) for k in range(len(pol.lBasis))] + [Est.silos[k].nvl for k in range(len(Est.silos))] + [Est.pos] + [d.duracao]
				Stat.append(stat)
		arquivo  = 	self.caminho + 'Log/' + 'saida_sim.csv'
		with open(arquivo, 'w', newline='') as myfile:
			wr = csv.writer(myfile)
			for l in Stat:
				wr.writerow(l)
		del(Stat)
		end = time.time()
		t = end-start
		print("Tempo de simulação 2:",t)
		return 0 #retorna o custo de todas as iterações


##@b graficoTripper
#@brief Plota o gráfico
	def graficoTripper(self,Estado,niter):
		s=[]
		for h in range(niter+1):
			s.append(h)
		matplotlib.pyplot.figure(figsize=(50,50))
		for l in range(len(Estado.silos)):
			matplotlib.pyplot.scatter(s,Estado.silos[l].hist_nvl,s=250,label=Estado.silos[l].name)
			matplotlib.pyplot.plot(s,Estado.silos[l].hist_nvl,'k:')

		matplotlib.pyplot.xlabel("Estágios")
		matplotlib.pyplot.ylabel("Nivel dos Silos")
		matplotlib.pyplot.title("Nível dos Silos ao Longo do Tempo ")
		matplotlib.pyplot.xticks(s,rotation=90)
		matplotlib.pyplot.legend(bbox_to_anchor=(1.02,1),loc=2,borderaxespad=0.)

		#matplotlib.pyplot.show()
		arquivo = self.caminho + 'Graficos/' + 'Niveis.png'
		matplotlib.pyplot.savefig(arquivo) #salva o gráfico



'''
class Gerador(tpd.Gerador):
	def __init__(self):
		x=0
	def gera_instancia(self):
		arq = open('lista.xml', 'w')
		texto = []
		texto.append('<?xml version="1.0" encoding="UTF-8"?>\n')
		texto.append('<Tripper_instGen ArqName = "teste">\n')
		texto.append('<Problema>\n')

		texto.append('<Te>')
		x=random.randint(500,700)
		texto.append(str(x))
		texto.append('</Te>\n')

		texto.append('<Ts>')
		x=random.randint(200,300)
		texto.append(str(x))
		texto.append('</Ts>\n')
		##print ("Entrou no gerador")
		num_s = input ('Informe o número de silos: ')


		texto.append('<P_ini>')
		#x=random.randint(1,num_s)
		x=1
		texto.append(str(x))
		texto.append('</P_ini>\n')

		texto.append('<y1>')
		x=random.random()
		texto.append(str(x))
		texto.append('</y1>\n')

		texto.append('<y2>')
		x=random.random()
		texto.append(str(x))
		texto.append('</y2>\n')

		texto.append('</Problema>\n\n')

		for i in range(num_s):

			texto.append('<Silo name="Silo_')
			texto.append(str(i+1))
			texto.append('">\n')

			texto.append('<Vol_ini>')
			x=random.randint(3000,5000)
			texto.append(str(x))
			texto.append('</Vol_ini>\n')

			texto.append('<L_inf>')
			#x=random.randint(1000,3000)
			x=0
			texto.append(str(x))
			texto.append('</L_inf>\n')

			texto.append('<L_sup>')
			#x=random.randint(7000,10000)
			x=100
			texto.append(str(x))
			texto.append('</L_sup>\n')

			texto.append('</Silo>\n\n')

		texto.append('</Tripper_instGen>\n')


		arq.writelines(texto)
		arq.close()
'''


