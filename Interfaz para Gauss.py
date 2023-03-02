# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:49:52 2023
Interfaz para graficas filtro de gauss
@author: César Daniel
"""

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pyperclip as pc
import numpy as np
from tkinter import filedialog
from pandas import read_excel,DataFrame
from scipy.ndimage import gaussian_filter1d

class GraphPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("Gráfica Actualizable")
        
        for i in range(9):
            root.rowconfigure(i, weight=3,minsize=10)
        for i in range(3):
            root.columnconfigure(i, weight=3, minsize=10)
        
        # Figura
        self.fig = plt.Figure(figsize=(5, 4), dpi=100)
        self.plot = self.fig.add_subplot(111)
        self.plot.set_xlabel("X-axis")
        self.plot.set_ylabel("Y-axis")
        self.plot.set_title("Gráfica Actualizable")

        # Lienzo
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0,column=0,rowspan=10)
        
        
        #Agregar cuadros de nombre para seleccionar con pandas
        self.X_Axis_label = tk.Label(self.root,text="Eje x")
        self.Y_Axis_label = tk.Label(self.root,text="Eje y")
        self.X_Axis_box = tk.Entry(self.root)
        self.Y_Axis_box = tk.Entry(self.root)
        
        self.X_Axis_label.grid(row=0,column=1)
        self.X_Axis_box.grid(row=0,column=2)
        self.Y_Axis_label.grid(row=1,column=1)
        self.Y_Axis_box.grid(row=1,column=2)
        
        
        # Se crea boton de actualización
        self.button = tk.Button(master=self.root, text="Leer Señal",command=self.find_File)
        self.button.grid(row=2,column=1,padx=0,pady=0,columnspan=2,sticky="ew")
        
        
        #Etiqueta de texto
        self.text_Sigma=tk.Label(root,text="Sigma")
        self.text_Sigma.grid(row=3,column=1)
        
        self.Sigma_box = tk.Entry(master=self.root)
        self.Sigma_box.grid(row=3,column=2)
        
        self.text_Order=tk.Label(root,text="Orden")
        self.text_Order.grid(row=4,column=1)
        
        self.Order_box = tk.Entry(master=self.root)
        self.Order_box.grid(row=4,column=2)
        
        self.text_Multiplicador=tk.Label(root,text="Multiplicador")
        self.text_Multiplicador.grid(row=5,column=1)
        
        self.Multiplicador_box = tk.Entry(master=self.root)
        self.Multiplicador_box.grid(row=5,column=2)
        
        
        # Se crea boton de actualización
        self.button_actualizar = tk.Button(master=self.root, text="Actualizar Gráfica", command=self.update_plot)
        self.button_actualizar.grid(row=6,column=1,padx=0,pady=0,columnspan=2)
        
        self.text_namefile = tk.Label(self.root, text="Nombre de archivo")
        self.box_namefile = tk.Entry(self.root)
        
        self.text_namefile.grid(row=7, column=1)
        self.box_namefile.grid(row=7, column=2)
        
        self.button_guardar_grafica = tk.Button(master=self.root, text="Guardar grafica", command=self.save_graph)
        self.button_guardar_grafica.grid(row=8,column=1,padx=0,pady=0,sticky="nsew",columnspan=2)
        
        self.button_guardar_señal = tk.Button(master=self.root, text="Guardar señal", command=self.save_signal)
        self.button_guardar_señal.grid(row=9,column=1,padx=0,pady=0,sticky="nsew",columnspan=2)
        
        

    def update_plot(self):
        self.plot.cla()
        #self.canvas.draw()
        self.signal_y_modificada = gaussian_filter1d(self.signal_y_original,sigma=int(self.Sigma_box.get()),order=int(self.Order_box.get()))
        self.signal_y_modificada = self.signal_y_modificada*float(self.Multiplicador_box.get())
        self.plot.plot(self.signal_x_original,self.signal_y_original,label="Original")
        self.plot.plot(self.signal_x_original,self.signal_y_modificada,label="Modificada")
        self.plot.legend()
        # Actualizar la gráfica
        self.canvas.draw()
        
    def find_File(self):
        self.archivo_excel = filedialog.askopenfilename(filetypes=[("Archivo de Excel", "*.xlsx")])
        self.df = read_excel(self.archivo_excel,index_col=0)
        
        self.signal_x_original = list(self.df[self.X_Axis_box.get()])
        self.signal_y_original = list(self.df[self.Y_Axis_box.get()])
        self.TypeOfVector()
        
    def save_graph(self):
        self.fig.savefig(str(self.box_namefile.get())+"_M"+str(self.Y_Axis_box.get())+".png",dpi=300)
        
    def save_signal(self):
        df=DataFrame(self.signal_y_modificada)
        print(df)
        df.to_excel(str(self.box_namefile.get())+"_M"+str(self.Y_Axis_box.get())+".xlsx", index=False,header=False)
        
    def TypeOfVector(self):
        if self.Y_Axis_box.get().find("Module") >= 0:
            self.signal_y_original = np.multiply(self.signal_y_original,100)
        elif self.Y_Axis_box.get().find("Phase") >= 0:
            contador = 0
            for i in list(self.signal_y_original):
                if i >= 0:
                    contador = contador + 1
                else:
                    contador = contador - 1
            if contador >= 0:
               self.signal_y_original = np.multiply(self.signal_y_original,-9)
            else:
               self.signal_y_original = np.multiply(self.signal_y_original,9) 
               

root = tk.Tk()
graph_plotter = GraphPlotter(root)
root.mainloop()

