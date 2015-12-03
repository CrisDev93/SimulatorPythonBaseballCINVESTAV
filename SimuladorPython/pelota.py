import sys 
import pygame 
import time
from threading import *
from movimientos import *
class Pelota(): 
	moviendose = False

	def __init__(self):

	
		self.x = 445
		self.y = 545
		self.figura = pygame.image.load("media/ball.png").convert_alpha()
		self.moviendose = False
		self.velocidad = 5
		self.objX = 0
		self.objY = 0
    	

	def moversePelota(self,coordenadasx,coordenadasy):
		coordenadas = coordenadasx,coordenadasy
		yo = self
		movs = Movimientos()
		self.moviendose = True
		try:
			movs.moverBalon(yo,coordenadas)
			self.moviendose = False
		except Exception as e:
			print "ERROR EN PELOTA LINEA 26",e 

	def setCoord(self,coords):
		self.x = coords[0]
		self.y = coords[1]
	


    			

