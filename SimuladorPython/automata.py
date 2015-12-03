import sys
import re
from estado import *
from Stack import *
###################################################################################
## AUTOR: Cristian Michel Perez Zarate 										     ##
##  La clase Automata se encarga de realizar todo trabajo respecto a la creacion ##
## y actualizacion de la pila en el cual se almacenan objetos de tipo estado     ##
###################################################################################
class Automata:
	def __init__(self):
		self.estados = Stack()


	#Este metodo se encarga de leer el fichero que incluye los estados en texto plano
	def leerArchivo(self):
		archivo = open("jugadas/5.dat", "r") 
		archivo.readline()
		#elimino el salto de linea al final
		linea = archivo.readline().rstrip('\n')
		#elimino el punto al final del texto y retorno dicho texto 
		return linea.rstrip('.')
	#Este metodo es el que crea la pila y agrega los objetos, hace un match entre los caracteres y los numeros 
	def crearPilaAutomata(self):
		guiones = self.leerArchivo()
		#guardo en la variable estados cada uno de los guiones separados por coma
		estadossinMatch = []
		estadossinMatch = guiones.split(",")
		for estado in estadossinMatch:
			
			match = re.match(r"([a-z]+)([0-9]+)",estado, re.I)
			if match:
				
				items = match.groups()
				escenario = items[0]
    			numeros = items[1]
    			cad_numero = str(numeros)
    			
    			base = cad_numero[0]
    			try:
    				jugador = int(cad_numero[1])
    			except: 
    				jugador = 0
    			
    			self.estados.push(Estado(escenario,base,jugador))




    		
    	






		


