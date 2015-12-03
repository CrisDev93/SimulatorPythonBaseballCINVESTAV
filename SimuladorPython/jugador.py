import pygame
from pygame.locals import *
import sys
import threading
import time 
from movimientos import *
import sprites
from threading import Thread
import random
class Jugador(): 
	
	def __init__(self):
	
		self.rol =""
		self.equipo=0
		self.movimiento = False
		self.imagen=""
		self.numero = 0 
		self.x = 0
		self.y = 0
		self.fotogramas = []
		self.movs = Movimientos()
		self.sel = ""
		self.contador = 6
		self.bateador = False
		self.turno = False
		self.enCampo = False
		self.ultimo = False
		self.moviendose = False
		self.movimientoBalk = False
		self.velocidad = 10
		self.direccion = "Abajo"

	#------------getCoordenadasZonadeEspera --------------#
	#Metodo que retorna una posicion aleatoria respecto al area de descanzo
	def getCoordenadasZonadeEspera(self):
		return [random.randint(750,900),random.randint(184,200)]
	#---------- crearFotogramas ------------------------# 
	# Metodo que se encarga de crear la secuencia de imagenes contenidos en el archivo media.equipo1.png 
	#los cuales son los que se toman como objetos en la clase main.draw() y las crea respecto al numero de equipo a la cual pertenece. 
	def crearFotogramas(self):
		
		global fotogramas,sel
		if self.equipo == 1:
			self.fotogramas = sprites.grab_sprite_sheet('media/equipo1.png', 4, 3)  
		else:
			self.fotogramas = sprites.grab_sprite_sheet('media/equipo2.png', 4, 3)  
	#-------- getJugador ----------------------# 
	#Metodo el cual implementa una busqueda simple el cual itera el arreglo de los jugadores y devuelve al jugador con el cual
	#cumple el rol y el equipo que se les especifico
	#@param jugadoresLista es el objeto Array que contiene objetos de tipo Jugador y es donde se realiza la busqueda
	#@param rol es una cadena el cual contiene el rol a buscar 
	#@param equipo es un numero entero el cual contiene el equipo en el cual pertence ese rol 
	def getJugador(self,jugadoresLista,rol,equipo):
		for jugador in jugadoresLista:
			if jugador.rol == rol:
				return jugador
	
		return jugador
	#------------- defMovimiento ---------------# 
	#Metodo el cual retorna la direccion el cual la animacion se va a reproducir, esto tomando en cuenta 
	#las coordonadas a donde se dirige partiendo de su coordenada origen. 
	#@param objetivo es un arreglo de numeros enteros [integer,integer] el cual contiene las coordenadas a las que el jugador ira
	#@param actual es un arreglo de numeros enteros [integer,integer] el cual contiene las coordenadas en el cual el jugador parte (posicion actual)
	def defMovimiento(self,objetivo,actual):
		numerox = 0
		numeroy = 0
		if objetivo[0] > actual[0]: 
			numerox = objetivo[0] - actual[0]
		else: 
			numerox = actual[0] - objetivo[0]

		if objetivo[1] > actual[1]: 
			numeroy = objetivo[1] - actual[1]
		else: 
			numeroy = actual[1] - objetivo[1]

		if numerox > 10: 
			if objetivo[0] > actual[0]: 
				return "Derecha"
			else: 
				return "Izquierda"
		else:
			if objetivo[1] > actual[1]:
				return "Abajo"
			else: 
				return "Arriba"

		



   	def movimientoBount(self,cercano,pelota,coordsPelota,jugadores):
   		muestraWait = self.getJugador(jugadores,"wait",0)
   		corredor = self.getJugador(jugadores,"Bateador",muestraWait.equipo)
   		cercano.moverse(coordsPelota[0],coordsPelota[1],False)
   		while pelota.moviendose:
   			time.sleep(0.5)

   		pelota.moversePelota(528,515)
   		equipo = 0
   		if muestraWait.equipo == 1: 
   			equipo = 2 
   		else: 
   			equipo = 1

   		primeraBase = self.getJugador(jugadores,"Primera Base",equipo)
   		primeraBase.velocidad = 5
  		primeraBase.moverseConBalon(primeraBase,[561,559],pelota)
   		while corredor.moviendose:
   			time.sleep(0.5)
   		corredor.rol = "wait"
		corredor.ultimo = False
		gw = self.getCoordenadasZonadeEspera()
		threading.Thread(target = corredor.moverse, args = (gw[0],gw[1],False)).start()
		
	def AccionOut(self,cercano,objetivo,agenteBase,pelota,AgentepuestoOut,jugadores,tipo,coordsPelotaObjetivo,isHit):
		if isHit: 
			tipo = 2
		if tipo ==1: 
			print "De tipo 1"
			cercano.moverse(coordsPelotaObjetivo[0],coordsPelotaObjetivo[1],False)
			while pelota.moviendose:
				time.sleep(0.5)
			while agenteBase.moviendose:
				time.sleep(0.5)
			pelota.moversePelota(agenteBase.x,agenteBase.y)
			pelota.objX = agenteBase.x 
			pelota.objY = agenteBase.y
			#moverseConPelota(self,xObjetivo,yObjetivo,pelota)
			agenteBase.moverseConPelota(objetivo[0],objetivo[1],pelota)
			
			AgentepuestoOut.movimiento = False
			time.sleep(2)
			if AgentepuestoOut.rol == "Bateador":
				#MovimientoOut(self,jugadores,coordsout)
				print "Se puso Out a un bateador y habra cambios en tipo 1"
				self.MovimientoOut(jugadores)
			else: 
				print "Se puso Out a ",AgentepuestoOut.rol," y habra cambios en tipo 1"
				gw = self.getCoordenadasZonadeEspera()
				AgentepuestoOut.rol = "wait"
				AgentepuestoOut.ultimo = False
				threading.Thread(target = AgentepuestoOut.moverse, args = (gw[0],gw[1],False)).start()   

		if tipo == 2: 
			print "De tipo 2"
			if isHit: 
				cercano.moverse((coordsPelotaObjetivo[0] + 40 ),(coordsPelotaObjetivo[1] + 40),False)
			else: 
				cercano.moverse((coordsPelotaObjetivo[0] + 20 ),(coordsPelotaObjetivo[1] + 20),False)

			while pelota.moviendose:
				time.sleep(0.5)
			px = pelota.x 
			py = pelota.y
			cercano.moverse((px),(py),False)
			while agenteBase.moviendose:
				time.sleep(0.5)
			xp = agenteBase.x
			yp = agenteBase.y
			pelota.moversePelota(xp,yp)
			#moverseConPelota(self,xObjetivo,yObjetivo,pelota)
			while agenteBase.moviendose:
				time.sleep(0.5)
			agenteBase.moverseConPelota(objetivo[0],objetivo[1],pelota)
			if isHit == False:
				if AgentepuestoOut.rol == "Bateador":
					print "Se puso Out a un bateador y habra cambios en tipo 2"
					self.MovimientoOut(jugadores)

			







	def MovimientoOut(self,jugadores):
		#if bool(random.getrandbits(1)): 
			
			muestraWait = self.getJugador(jugadores,"wait",0)
			corredor = self.getJugador(jugadores,"Bateador",muestraWait.equipo)
			corredor.movimiento = False
			nuevoBateador = self.getBateador(jugadores,corredor.equipo)
			coordsw = (446,610)
			nuevoBateador.rol = "Bateador"
			nuevoBateador.ultimo = True
			nuevoBateador.bateador = True
			corredor.rol = "wait"
			corredor.ultimo = False
			while corredor.ultimo == True:
				corredor.ultimo = False
			while nuevoBateador.rol == "wait":
				nuevoBateador.rol = "Bateador"   
				nuevoBateador.ultimo = True
				print "Reasignando ..."
			nuevoBateador.velocidad = 15
			threading.Thread(target = nuevoBateador.moverse, args = (coordsw[0],coordsw[1],False)).start()
			gw = self.getCoordenadasZonadeEspera()
			corredor.velocidad = 15
			threading.Thread(target = corredor.moverse, args = (gw[0],gw[1],False)).start()   
			print "Nuevo bateador con el numero: ",nuevoBateador.numero," del equipo: ",nuevoBateador.equipo
	def moverse(self,xObjetivo,yObjetivo,isHome):
		while self.moviendose: 
			time.sleep(0.1)
		self.direccion = self.defMovimiento((xObjetivo,yObjetivo),(self.x,self.y))
		self.moviendose = True
		self.movimiento = True
		yo = self
		movimiento = True
		movs = Movimientos()
		
		coordenadasObjetivo = xObjetivo,yObjetivo

		movs.moverse(yo,coordenadasObjetivo)  
		moviendose =False
		self.moviendose = False

		if isHome:
			print "SOY HOME Y ME VOY A WAIT ZONE"
			
			
			self.rol = "wait"
			self.ultimo = False
			while self.ultimo == True:
				self.ultimo = False
			waitCords = self.getCoordenadasZonadeEspera()
			try:
				self.moverse(waitCords[0],waitCords[1],False)
			except Exception as e : 
				print "EL EROR ES EN JUGADOR LINEA 102",e
			

	def salirDelCampoOut(self,jugador,jugadores):
		if jugador.rol == "Bateador":
			nuevoBateador = self.getBateador(jugadores,jugador.equipo)
			nuevoBateador.rol = "Bateador"
			nuevoBateador.ultimo = True
			nuevoBateador.bateador = True
			jugador.rol = "wait"
			jugador.ultimo = False
			while jugador.ultimo:
				jugador.ultimo = False
			while nuevoBateador.rol == "wait":
				nuevoBateador.rol = "Bateador"
				nuevoBateador.ultimo = True
				print "Reasignando ..."
			xJ,yJ = 446,610
			print "Acabo de asignar a ---> ",nuevoBateador.rol,"Con el numero : ",nuevoBateador.numero," del EQUIPOOOO ",nuevoBateador.equipo
			threading.Thread(target = nuevoBateador.moverse, args = (xJ,yJ,False)).start()
			nw = self.getCoordenadasZonadeEspera()
			threading.Thread(target = jugador.moverse, args = (nw[0],nw[1],False)).start()   
		else: 
			jugador.rol = "wait"
			jugador.ultimo = False
			while jugador.ultimo:
				jugador.ultimo = False
			nw  = self.getCoordenadasZonadeEspera()
			threading.Thread(target = jugador.moverse, args = (nw[0],nw[1],False)).start()  







 	def moverseConPelota(self,xObjetivo,yObjetivo,pelota):
		while self.moviendose: 
			time.sleep(1)
		self.moviendose = True
		self.movimiento = True
		yo = self
		movimiento = True
		movs = Movimientos()
		
		coordenadasObjetivo = xObjetivo,yObjetivo

		movs.moverseConBalon(yo,coordenadasObjetivo,pelota)
		global moviendose 
		moviendose =False
		self.moviendose = False


	def getUltimo(self,jugadores,equipo):
		for ag in jugadores: 
			print "----> ",ag.rol,", Equipo: ",ag.equipo," Numero: ",ag.numero, " Ultimo = ",ag.ultimo
		for ag in jugadores:

			if ag.equipo == equipo and ag.ultimo == True:
				return ag

		for ag in jugadores:
			if ag.numero == 1 and ag.equipo == equipo:
				return ag

		return ""

	def getBateador(self,jugadores,equipo):
		bateador = ["",100]
		disponibles = False
		for jugador in jugadores:
			if jugador.bateador == False and jugador.equipo == equipo:
				disponibles = True

		if disponibles == False: 
			for jugador in jugadores:
				if jugador.equipo == equipo: 
					jugador.bateador = False

		for jugador in jugadores:
			if jugador.bateador == False and jugador.equipo == equipo:
				if jugador.numero < bateador[1]:
					bateador[0] = jugador
					bateador[1] = jugador.numero
		return bateador[0]

	

