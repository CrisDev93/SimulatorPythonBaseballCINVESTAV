import pygame
from pygame.locals import *
import sys
import threading
import time 
import random
class Movimientos: 
	
	posicionesJugadores = [("Primera Base",[528,515]),("Segunda Base",[420,480]),("Tercera Base",[340,555]),("Jardinero Izquierdo",[313,431]),("Jardinero Central",[450,393]),("Jardinero Derecho",[594,411]),("Pitcher",[445,545]),("Bateador",[446,610]),("Catcher",[446,642])]
	bases = [("Primera Base",[561,559]),("Segunda Base",[456,489]),("Tercera Base",[349,562]),("Home",[454,632])]
	

	def getCoordenadasRol(self,rol):
		for pos in self.posicionesJugadores:
			if pos[0] == rol:
				return pos[1]
		return [random.randint(750,900),random.randint(184,200)]

	def moverse(self,jugador,coordenadas):
 
		jugador.movimiento = True
		sumarx = False
		sumary = False
		if jugador.x < coordenadas[0]:
			sumarx =True
		if jugador.y < coordenadas[1]:
			sumary = True

		keyX = False
		keyY =  False
		while jugador.movimiento:
			miliseconds = float(jugador.velocidad)
			seconds = float( miliseconds / 1000 )
			
			time.sleep(seconds)
			jugador.moviendose = True
			if (keyX  and keyY):
				jugador.movimiento = False				
			else: 
				if jugador.x == coordenadas[0]:
					keyX = True
					jugador.direccion = jugador.defMovimiento(coordenadas,(jugador.x,jugador.y))
				else:
					if sumarx:
						jugador.x+=1
					else:
						jugador.x-=1
				if jugador.y == coordenadas[1]:
					keyY = True
					jugador.direccion = jugador.defMovimiento(coordenadas,(jugador.x,jugador.y))
				else:
					if sumary:
						jugador.y+=1
					else:
						jugador.y-=1
		
		jugador.movimiento = False
	def moverseConBalon(self,jugador,coordenadas,balon):
		
		sumarx = False
		sumary = False
		if jugador.x < coordenadas[0]:
			sumarx =True
		if jugador.y < coordenadas[1]:
			sumary = True

		keyX = False
		keyY =  False
		miliseconds = float(jugador.velocidad)
		seconds = float( miliseconds / 1000 )
		while jugador.movimiento:

			balon.setCoord((jugador.x,jugador.y))
			
			
			time.sleep(seconds)
			jugador.moviendose = True
			if (keyX  and keyY):
				jugador.movimiento = False				
			else: 
				if jugador.x == coordenadas[0]:
					keyX = True
				else:
					if sumarx:
						jugador.x+=1
					else:
						jugador.x-=1
				if jugador.y == coordenadas[1]:
					keyY = True
				else:
					if sumary:
						jugador.y+=1
					else:
						jugador.y-=1		
	def moverBalon(self,pelota,coordenadas):
		sumarx = False
		sumary = False
		if pelota.x < coordenadas[0]:
			sumarx =True
		if pelota.y < coordenadas[1]:
			sumary = True

		keyX = False
		keyY =  False
		key = True
		while key:
			miliseconds = float(pelota.velocidad)
			seconds = float( miliseconds / 1000 )
			
			time.sleep(seconds)
			pelota.moviendose = True
			if (keyX  and keyY):
				key = False				
			else: 
				if pelota.x == coordenadas[0]:
					keyX = True
				else:
					if sumarx:
						pelota.x+=1
					else:
						pelota.x-=1
				if pelota.y == coordenadas[1]:
					keyY = True
				else:
					if sumary:
						pelota.y+=1
					else:
						pelota.y-=1

	def getCoordenadasZonadeEspera(self):
		return [random.randint(750,900),random.randint(184,200)]
	def cambioEquipo(self,jugadores):
		roles = ["Pitcher","Primera Base","Segunda Base","Tercera Base","Jardinero Derecho","Jardinero Izquierdo","Jardinero Central","Campo Corto","Catcher"]
		ofensivo = []
		defensivo = []

		for jugador in jugadores:
			if jugador.turno == True: 
				defensivo.append(jugador)
			else: 
				ofensivo.append(jugador)

		bateador = defensivo[0].getUltimo(jugadores,defensivo[0].equipo)
		print "El ultimo de equipo ",bateador.equipo," es: ",bateador.numero
		bateador.rol = "Bateador"
		bateador.turno = False
		bateador.enCampo = True
		bateador.bateador = True
		bateador.ultimo = True
		btmp = self.getCoordenadasRol("Bateador")
		threading.Thread(target=bateador.moverse,args =(btmp[0],btmp[1],False)).start()
		print "Asignado Bateador con el numero: ",bateador.numero		
		for d in range(len(defensivo)):
			if not defensivo[d].rol == "Bateador": 
				defensivo[d].rol = "wait"
				defensivo[d].turno = False
				defensivo[d].enCampo = False
				gw = defensivo[d].getCoordenadasZonadeEspera()
				threading.Thread(target =defensivo[d].moverse,args =(gw[0],gw[1],False)).start()


		for d in range(len(ofensivo)):
				ofensivo[d].rol = roles.pop()
				ofensivo[d].turno = True
				ofensivo[d].enCampo = True
				cd = self.getCoordenadasRol(ofensivo[d].rol)
				threading.Thread(target =ofensivo[d].moverse,args =(cd[0],cd[1],False)).start()
		print "Ofensivos: ",len(ofensivo)," Defensivos: ",len(defensivo)


			


		
