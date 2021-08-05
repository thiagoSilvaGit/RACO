# -*- coding: utf-8 -*-

import lerInst as li
import numpy as np

class Estado:
    def __init__(self):
        self.R = []
        self.V = []
        self.E = []
        self.r_sd = 0
    
    def leTXT(self, file):
        nf, adjf, Lreqf = li.lerTXT(file)  # Leitura do arquivo de dados
        self.r_sd = np.array(Lreqf)
        for y in range(nf):
            for k in range(nf):
                if self.r_sd[y][k]:
                    self.R.append([y,k])
    
        adjMtx = np.array(adjf)
        for y in range(nf):
            self.V.append(y)
            for k in range(nf):
                if adjMtx[y][k]:
                    self.E.append([y,k])


        