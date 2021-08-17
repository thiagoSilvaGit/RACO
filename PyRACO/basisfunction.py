# -*- coding: utf-8 -*-
import cria
import statistics as st
import networkx as nkx

def switch_bf(argument):
    switcher = {
        'NR':NR,
        'NMR':NMR,
                
    }

    obj = switcher.get(argument, lambda *args: "Invalid Basis Function")
    return obj()

class BF:
    def Calc_phi(self,estado_x):
        return 0
class NR(BF):
    def Calc_phi(self, estado_x):
        return self.NR(estado_x)

    def NR(estado_x):
        nr = sum(estado_x.r_sd)
        return nr

class NMR(BF):
    def Calc_phi(self, estado_x):
        return self.NR(estado_x)
    
    def NMR(estado_x):
        nr = sum(estado_x.rsd)
        nmr = nr/len(estado_x.V)
        return nmr

class MRS(BF):
    def Calc_phi(self, estado_x):
        return self.MRS(estado_x)
    
    def MRS(estado_x):
        sai = [sum(estado_x.r_sd[i][j] for j in range(len(estado_x.V))) for i in range(len(estado_x.V))]
        return sai

class MRD(BF):
    def Calc_phi(self, estado_x):
        return self.MRD(estado_x)

    def MRD(estado_x):
        entra = [sum(estado_x.r_sd[i][j] for i in range(len(estado_x.V))) for j in range(len(estado_x.V))]
        return entra

class DPRS(BF):
    def Calc_phi(self, estado_x):
        return self.DPRS(estado_x)

    def DPRS(estado_x):
        sai = [sum(estado_x.r_sd[i][j] for j in range(len(estado_x.V))) for i in range(len(estado_x.V))] 
        stdrs = st.stdev(sai)
        return stdrs           

class DPRD(BF):
    def Calc_phi(self, estado_x):
        return self.DPRD(estado_x)

    def DPRS(estado_x):
        entra = [sum(estado_x.r_sd[i][j] for i in range(len(estado_x.V))) for j in range(len(estado_x.V))] 
        stdrd = st.stdev(entra)
        return stdrd

class NN(BF):
    def Calc_phi(self, estado_x):
        return self.NN(estado_x)

    def NN(estado_x):
        nn = len(estado_x.V)
        return nn

class NA(BF):
    def Calc_phi(self, estado_x):
        return self.NA(estado_x)
    
    def NA(estado_x):
        na = len(estado_x.E)
        return na

class NMA(BF):
    def Calc_phi(self, estado_x):
        return self.NMA(estado_x)
    
    def NMA(estado_x):
        nma = len(estado_x.E) / len(estado_x.V)
        return nma

class GMX(BF):
    def Calc_phi(self, estado_x):
        return self.GMX(estado_x)

    def GMX(estado_x):
        adjMtx = self.r_sd = np.array(estado_x.E)
        g = nkx.convert_matrix.from_numpy_matrix(adjMtx, create_using=nkx.DiGraph)
        ld_aux = g.degree
        ldegree = [i[1] for i in ld_aux]
        gdmax = max(ldegree)
        return gdmax
	    
class GMN(BF):
    def Calc_phi(self, estado_x):
        return self.GMN(estado_x)

    def GMN(estado_x):
        adjMtx = self.r_sd = np.array(estado_x.E)
        g = nkx.convert_matrix.from_numpy_matrix(adjMtx, create_using=nkx.DiGraph)
        ld_aux = g.degree
        ldegree = [i[1] for i in ld_aux]
        gdmin = min(ldegree)
        return gdmin

class MCM(BF):
    def Calc_phi(self, estado_x):
        return self.MCM(estado_x)

    def MCM(estado_x):
        adjMtx = self.r_sd = np.array(estado_x.E)
        g = nkx.convert_matrix.from_numpy_matrix(adjMtx, create_using=nkx.DiGraph)
        maxcmin = 0
        for i in range(len(estado_x.V)):
            for j in range(len(estado_x.V)):
                if i != j:
                    cmin = nkx.shortest_path_length(g, i, j)
                    if cmin > maxcmin:
                        maxcmin = cmin
        return maxcmin
        
class MFM(BF):
    def Calc_phi(self, estado_x):
        return self.MFM(estado_x)

    def MCM(estado_x):
        adjMtx = self.r_sd = np.array(estado_x.E)
        g = nkx.convert_matrix.from_numpy_matrix(adjMtx, create_using=nkx.DiGraph)
        maxcmf = 0
        for i in range(len(estado_x.V)):
            for j in range(len(estado_x.V)):
                if i != j:
                    mxf, _ = nkx.maximum_flow(g, i, j)
                    if mfx > maxcmf:
                        maxcmf = mxf
        return maxcmf
