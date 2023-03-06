# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 12:17:48 2023

@author: César Daniel
"""
import pandas as pd
import numpy as np
import pyperclip as pc

class AnalisisDeSenales(object):
    def __init__(self,time_sample,n_sample):
        #Time sample in seconds, number fo samples per seconds
        self.time_sample = time_sample
        self.n = n_sample
        self.signals = self.clip2list()
        
    def clip2list(self):
        a = pc.paste().splitlines()
        a.pop(0)
        a.pop(len(a)-1)
        c = []
        for i in a:
            c.append(i.split("\t"))
        d = np.array(c).astype(float)
        return d
    
    def createTimeVector(self):
        self.TimeVector = np.arange(1/self.n,self.time_sample,1/self.n)
    
    def createDF(self):
        self.df= pd.DataFrame(data=self.signals,columns=["Module1","Module2","Phase1","Phase2"])
        self.df.insert(0,"Time",list(self.TimeVector),True)
                         
    def DFtoExcel(self,name):
        self.df.to_excel(name+".xlsx")
        
# tiempo = int(input("Ingrese tiempo de muestra\n"))
# muestreo = int(input("Ingrese numero de muestras en un segundo\n"))
tiempo=10
muestreo=1000
usuario=AnalisisDeSenales(tiempo,muestreo)
usuario.createTimeVector()
usuario.createDF()
nombre = str(input("Ingrese nombre de la señal\n"))
usuario.DFtoExcel(nombre)

