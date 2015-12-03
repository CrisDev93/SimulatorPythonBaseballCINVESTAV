import sys

#Clase que define un estado en el automata
#@param escenario cadena que contiene el escenario a ejecutar ejemplo: h  que significa hit
#@param base numero entero que define la base a la cual se ejecuta ese estado ejemplo: 1
#@param jugador numero entero el cual define el numero del jugador a la cual ese estado tomara efecto, es muy 
#importante definirlo ya que mantiene la estabilidad en el simulador y la sincronizacion de los movimientos con el resto
class Estado():
	  def __init__(self,escenario,base,jugador):
	  	self.escenario = escenario
	  	self.base = base
	  	self.jugador = jugador
	  
	  	
	  	
	  