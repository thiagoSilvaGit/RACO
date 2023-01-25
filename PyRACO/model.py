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

def modelo(Inst,)
    model = grb.Model()
    Ltotal = np.zeros((Inst.n,Inst.n))
    Lambda_max = model.addVar(vtype=grb.GRB.INTEGER, name = f'Lambda_max')
    model.update()
