# -*- coding: utf-8 -*-
 
###################################################################################
## AUTOR: Cristian Michel Perez Zarate                                           ##
##  Este archivo Main es la encargada de ejecutar y crear todos los objetos      ##
## relaciodados al simulador, ejecuta los hilos necesarios para dibujar y mover  ##
## a los agentes                                                                 ##
##                                                                               ##
###################################################################################
 
import pygame
from pygame.locals import *
import sys
import threading
import time 
from jugador import *
import random
from automata import * 
from movimientos import *
from pelota import *
import math

# -----------
# Constantes
# -----------
 
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# -----------
# Variables
# -----------
fondo = ""
pelota = ""
screen = ""
key = True 
tux_pos_x = 0
tux_pos_y = 0
jugadores = []
automata = ""
roles = ["Pitcher","Primera Base","Segunda Base","Tercera Base","Jardinero Derecho","Jardinero Izquierdo","Jardinero Central","Campo Corto","Catcher"]
posicionesJugadores = [("Primera Base",[528,515]),("Segunda Base",[480,480]),("Tercera Base",[340,555]),("Jardinero Izquierdo",[313,431]),("Jardinero Central",[450,393]),("Jardinero Derecho",[594,411]),("Pitcher",[445,545]),("Bateador",[446,610]),("Catcher",[446,642]),("Campo Corto",[390,495])]
bases = [("Primera Base",[561,559]),("Segunda Base",[456,489]),("Tercera Base",[349,562]),("Home",[446,610])]
bateadorEquipo1 = 1
bateadirEquipo2= 1
lock = threading.Lock()
keyDraw = False
texto = "BESIBOL"
puntajeEquipo1="0"
puntajeEquipo2 = "0"
anuncioEquipo1= "EQUIPO 1: "+puntajeEquipo1
anuncioEquipo2= "EQUIPO 2: "+puntajeEquipo2
font=""
requerirBateador = False

                                                                                                                                                                                                                                                                                                     



def getwait():
        return [random.randint(750,900),random.randint(184,200)] 
def buscarporRol(rol):
    global lock
    lock.acquire(1)
    for jugador in jugadores:
        if jugador.rol == rol:
            tmp = jugador
            lock.release()
            return tmp
        else: 

            print "Disponible - > ",jugador.rol
    return ""
            

def getCoordenadasRol(rol):
    for pos in posicionesJugadores:
        if pos[0] == rol:
            return pos[1]

    return getwait()

def getCoordenadasBase(base):
    for pos in bases:
        if pos[0] == base:
            return pos[1]
    return getwait()

def buscarPorNumero(numero):
    print "ATENCION : ",numero
 
    for ag in jugadores:
       
        if ag.turno == False: 
           
            if int(ag.numero) == int(numero):
                print "ENCONTRE EL NUMERO"
                return ag

    return ""





def mostrarTexto(score,xLabel,yLabel):
   global font 
   scoretext=font.render(str(score), 1,(255,255,255))
   screen.blit(scoretext, (xLabel,yLabel))

## -------------------- dibujar --------------------

def dibujar():
    global fondo,tux,screen,key,tux_pos_x,tux_pos_y,pelota,texto,anuncioEquipo1,anuncioEquipo2,font
    font=pygame.font.Font(None,30)
    

    while key:

        while keyDraw:
            time.sleep(1)
     
        
       
 
        # Redibujamos todos los elementos de la pantalla

        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        
        screen.blit(fondo, (0, 0))
        screen.blit(pelota.figura, (pelota.x, pelota.y))
        for jugador in jugadores:

            if jugador.movimiento:

                if jugador.direccion == "Derecha":
                    jugador.contador+=1
                    if jugador.contador > 8:
                        jugador.contador = 6
                if jugador.direccion == "Izquierda":
                    jugador.contador+=1
                    if jugador.contador > 5:
                        jugador.contador = 3
                if jugador.direccion == "Arriba":
                    jugador.contador+=1
                    if jugador.contador > 11:
                        jugador.contador = 9
                if jugador.direccion == "Abajo":
                    jugador.contador+=1
                    if jugador.contador > 2:
                        jugador.contador = 0

                                  
                screen.blit(jugador.fotogramas[jugador.contador],(jugador.x,jugador.y))
            else:
                if jugador.movimientoBalk:
                    if jugador.contador == 2:
                        jugador.movimientoBalk = False
                    screen.blit(jugador.fotogramas[0],(jugador.x,jugador.y))
                    time.sleep(1)
                    if jugador.contador == 0:
                        jugador.contador = 2
                    

                else: 
                    screen.blit(jugador.fotogramas[1],(jugador.x,jugador.y))

        # se muestran lo cambios en pantalla
        mostrarTexto(texto,500,50)
        mostrarTexto(anuncioEquipo1,50,50)
        mostrarTexto(anuncioEquipo2,840,50)
        pygame.display.flip()
 
 

        
## -------------------- getRol --------------------
def getRol():
    try:
        global roles
        rol = roles.pop()
        return rol
    except: 
        return "wait"
## -------------------- crearJugadores --------------------
def crearJugadores():
    Numerojugadores =  18
    contadorequipo1 =0 
    contadorequipo2 = 0
    for x in range(Numerojugadores):
        nuevojugador = Jugador()
        if x == 0:
            contadorequipo2+=1
            nuevojugador.rol = "Bateador"
            nuevojugador.bateador = True
            nuevojugador.equipo = 2
            nuevojugador.numero = contadorequipo2
            nuevojugador.enCampo = True
            nuevojugador.ultimo = True
            coords = getCoordenadasRol(nuevojugador.rol)
        else: 
            nuevojugador.rol =getRol()
            coords = getCoordenadasRol(nuevojugador.rol)
            if nuevojugador.rol == "wait":
                contadorequipo2+=1
                nuevojugador.numero = contadorequipo2
                nuevojugador.equipo = 2
            else:
                contadorequipo1+=1
                nuevojugador.numero = contadorequipo1
                nuevojugador.equipo = 1
                nuevojugador.enCampo = True
                nuevojugador.turno = True
    
        
        nuevojugador.x = coords[0]
        nuevojugador.y =coords[1]
        nuevojugador.crearFotogramas()
        jugadores.append(nuevojugador)
        print nuevojugador.rol," team : ",nuevojugador.equipo 
      
## -------------------- getJugador --------------------

def getJugador(rol):
    lock.acquire(1)
    for j in jugadores:
      #  print "I'm ",rol," Finding --- >",j.rol
        if j.rol == rol:
            tmp = j
            lock.release()
            return j
    lock.release()
    return ""
## -------------------- getJugadorMasCercaBalon --------------------
def getJugadorMasCercaBalon(xBalon,yBalon):
    valorMenor = ["",100000000]
    candidatos = (getJugador("Campo Corto"),getJugador("Catcher"),getJugador("Primera Base"),getJugador("Segunda Base"),getJugador("Tercera Base"),getJugador("Jardinero Izquierdo"),getJugador("Jardinero Central"),getJugador("Jardinero Derecho"))
    for candidato in candidatos:
        resultado = math.sqrt( (candidato.x - xBalon)**2 + (candidato.y - yBalon)**2 )
        if resultado < valorMenor[1]:
            valorMenor = [candidato,resultado]

    return valorMenor[0]


## -------------------- lectorPila --------------------
#Este metodo es el que se encarga de relizar todos los movimientos
def lectorPila():
    global automata,texto,jugadores
    key = True
    bandera = False
    while automata.estados.isEmpty() == False:
            for ag in jugadores:
                coordsPertenece = getCoordenadasRol(ag.rol)
                if not ag.rol == "wait" : 
                    if  coordsPertenece[0] == ag.x and coordsPertenece[1] == ag.y:
                        pass
                    else: 
                        if ag.rol == "Campo1" or ag.rol == "Campo2" or ag.rol == "Campo3" or ag.rol == "Campo4":
                            pass
                        else: 
                            threading.Thread(target = ag.moverse , args = (coordsPertenece[0],coordsPertenece[1],False) ).start()
            #La pila espera a que no existan mas de 3 hilos en ejeucion, en caso que si existan
            #espera hasta que estos hilos terminen de ejecutarse, para asi poder recorrer los siguientes estados
            while threading.activeCount() >3:
                  time.sleep(0.2)
                  print "waiting Stack ..."
            
             
            if bandera and not automata.estados.peek().escenario == "r":
                JCercano = getJugadorMasCercaBalon(pelota.x,pelota.y)
                JCercano.moverse(pelota.x,pelota.y,False)
                coords = getCoordenadasRol("Pitcher")
                pelota.moversePelota(coords[0],coords[1])
                coordsPertenece = getCoordenadasRol(JCercano.rol)
                JCercano.moverse(coordsPertenece[0],coordsPertenece[1],False)
                bandera = False
            if not automata.estados.peek().escenario == "r":
                time.sleep(0.1)
            #Obtengo el siguiente estado para reproducir
            estado = automata.estados.pop()
            print "recorriendo la pila",estado.escenario

            if estado.escenario == "b":
                texto = "BOLA"
                
                coords = getCoordenadasBase("Home")
                xtmp = coords[0] 
                ytmp = coords[1]
                xtmp = xtmp + random.randint(5,10)
                ytmp = ytmp + random.randint(5,10)
                ncords = [xtmp,ytmp]

                pelota.moversePelota(ncords[0],ncords[1])
                bandera = True

            if estado.escenario == "co":
                texto =  "CONTACTO PELOTA"
            
                
 
                ncords = BatearBalon(0)
                #Obtengo un el siguiente estado sin removerlo de la pila para su verificacion
                sigestado = automata.estados.peek()
                #En caso que el siguiente estado se trate de un out, un hilo se encarga de hacer los movimientos necesarios y la pelota siga su recorrido sin interupcion
                if automata.estados.peek().escenario == "o":
                    pelota.velocidad = 2
                else: 
                    pelota.velocidad = 5
                threading.Thread(target =pelota.moversePelota,args= (ncords[0],ncords[1])).start()
                if bool(random.getrandbits(1)):
                    opcionOut = 1
                else:
                    opcionOut = 2
                while automata.estados.peek().escenario == "o":
                    texto = "OUT"
                    print "Soy out "
                    escenarioOut = automata.estados.pop()
                    AgentepuestoOut = buscarPorNumero(escenarioOut.base)
                    print "Comprobar: ",AgentepuestoOut.rol
                    
                    cercano = getJugadorMasCercaBalon(ncords[0],ncords[1])
                    objetivo = getCoordenadasBase( getSiguienteBaseAir(AgentepuestoOut) )
                    coordsOut = getCoordenadasBase(objetivo)
                    agenteBase = getJugador(getSiguienteBaseAir(AgentepuestoOut))
                    agenteBase.velocidad = 3
                    cercano.velocidad = 3 
                    
                    #AccionOut(self,cercano,objetivo,agenteBase,pelota,AgentepuestoOut,jugadores)
                    AgentepuestoOut.velocidad = 30
                    threading.Thread(target = AgentepuestoOut.moverse, args = (coordsOut[0],coordsOut[1],False)).start()
                    threading.Thread(target = AgentepuestoOut.AccionOut,args = (cercano,objetivo,agenteBase,pelota,AgentepuestoOut,jugadores,opcionOut,ncords,False)).start()

                bandera = True
                if sigestado.escenario == "hi":
                    texto = "HIT"
                    print "Escenario HIT"
                    automata.estados.pop()
                    sigestado = automata.estados.peek()
                    if sigestado.escenario == "a":
                        movsA = []
                        while automata.estados.peek().escenario == "a":
                            e = automata.estados.pop()
                            movsA.append(e)
                            print "ESTADO : ",e.escenario," Base: ",e.base," Jugador: ",e.jugador
                        mov = Stack()
                        #agente = buscarPorNumero(guion.jugador)
                        for m in movsA:
                            mov.push(m)
                        mov.reverse()
                        threading.Thread(target = movimientoBases, args = (movsA,True) ).start()
                        intentoOut(mov,ncords[0],ncords[1],pelota,ncords)
                       

                   
           
                bandera = True

            if estado.escenario == "s":
                texto = "STRIKE"
                pelota.setCoord(getCoordenadasRol("Pitcher"))
                coords = getCoordenadasRol("Catcher")
                pelota.moversePelota(coords[0],coords[1])
                bandera = True
            if estado.escenario == "f":
                texto =  "FOUL"
                pelota.setCoord(getCoordenadasRol("Pitcher"))
                coords = getCoordenadasBase("Home")
                pelota.moversePelota(coords[0],coords[1])
                coordenadasFoul = getCoordenadasBase("Home")
                xtmp = coordenadasFoul[0]
                ytmp = coordenadasFoul[1]
                if bool(random.getrandbits(1)): 
                    xtmp = xtmp - random.randint(100,200)
                else:
                    xtmp = xtmp + random.randint(100,200)
                ytmp = ytmp - random.randint(1,30)
                nCoordsFoul = [xtmp,ytmp]
                pelota.moversePelota(nCoordsFoul[0],nCoordsFoul[1])
                bandera = True
            if estado.escenario == "p":
                texto="PONCHE"
                corredor = getJugador("Bateador")
                corredor.movimiento =   True
                nuevoBateador = corredor.getBateador(jugadores,corredor.equipo)
                coordsw = (446,610)
                nuevoBateador.rol = "Bateador"
                nuevoBateador.enCampo = True
                nuevoBateador.bateador = True
                nuevoBateador.ultimo = True
                corredor.rol = "wait"
                corredor.ultimo = False
                corredor.enCampo = False
                threading.Thread(target = nuevoBateador.moverse, args = (coordsw[0],coordsw[1],False)).start()
                gt = getwait()
                threading.Thread(target = corredor.moverse, args = (gt[0],gt[1],False)).start()   
                print "Nuevo bateador con el numero: ",nuevoBateador.numero
                while nuevoBateador.rol == "wait":
                    nuevoBateador.rol = "Bateador"
                    nuevoBateador.ultimo = True
                    print "Reasignando ..."
                while corredor.ultimo:
                    corredor.ultimo = False
                    corredor.rol = "wait"
               
            if estado.escenario == "ce":
                texto = "CAMBIO DE EQUIPOS"
                movimiento = Movimientos()
                movimiento.cambioEquipo(jugadores)
          
            if estado.escenario == "d":
                texto = "DOBLETE"
                ncords = BatearBalon(2)
                sigestado = automata.estados.peek()
                #pelota.moversePelota(ncords[0],ncords[1])
               
                if sigestado.escenario == "a":
                    movsA = []
                    while automata.estados.peek().escenario == "a":
                        e = automata.estados.pop()
                        movsA.append(e)
                 

                mov = Stack()
                for m in movsA:
                    mov.push(m)
                mov.reverse()
                threading.Thread(target = movimientoBases, args = (movsA,True) ).start()
                intentoOut(mov,ncords[0],ncords[1],pelota,ncords)
                bandera = True

            if estado.escenario == "w":
                texto = "WILD PITCH"
                pelota.setCoord(getCoordenadasRol("Pitcher"))
                pitcher = getJugador("Pitcher")
                irPelotaCoords = getCoordenadasBase("Home")
                xPelota = irPelotaCoords[0]
                yPelota = irPelotaCoords[1]
                pelota.velocidad = 4
                pelota.moversePelota(xPelota,yPelota)
                xPelota = xPelota + 30
                yPelota = yPelota + 20
                pelota.moversePelota(xPelota,yPelota)
                

                movsA = []
                while automata.estados.peek().escenario == "a":
                    e = automata.estados.pop()
                    movsA.append(e)
                time.sleep(3)
                movimientoBases(movsA,False)

            if estado.escenario == "r":
                texto = "ROBO DE BASE"
                movsA = []
                while automata.estados.peek().escenario == "a":
                    e = automata.estados.pop()
                    movsA.append(e)
                index = random.randint(0,(len(movsA) -1) )
                AgenteRobar = buscarPorNumero( movsA[index].jugador )
                print "pass ..."
                baseIrAR =  getSiguienteBaseAir(AgenteRobar)
                if baseIrAR == "Home":
                    baseIrAR = getCoordenadasBase("Tercera Base")
                else: 
                    baseIrAR = getCoordenadasBase(baseIrAR)


                
                threading.Thread(target = movimientoBases,args = (movsA,True)).start()
                xLanzamiento = baseIrAR[0] + 20
                yLanzamiento = baseIrAR[1] + 30
                pelota.velocidad = 10
                time.sleep(1)
                pelota.moversePelota(xLanzamiento,yLanzamiento)
                agenteCercano = getJugadorMasCercaBalon(xLanzamiento,yLanzamiento)
                agenteCercano.moverse(xLanzamiento,yLanzamiento,False)
                coords = getCoordenadasBase(agenteCercano.rol)
                xPB = coords[0]
                yPB = coords[1]
                agenteCercano.velocidad = 20
                agenteCercano.moverse(xPB,yPB,False)
                pelota.velocidad = 5
                bandera = True
                
            if estado.escenario == "dp":
                texto = "DOBLE PLAY"
                pelota.velocidad = 3
                ncords = BatearBalon(7)
                jugadoresAOut = []
                #pelota.moversePelota(ncords)
                threading.Thread(target  = pelota.moversePelota, args = (ncords[0],ncords[1])).start()
                while automata.estados.peek().escenario == "o":
                    texto = "OUT"
                    jugadoresAOut.append(automata.estados.pop())

                jugador1 = buscarPorNumero(jugadoresAOut[0].base)
                jugador2 = buscarPorNumero(jugadoresAOut[1].base)
                jugador1.velocidad = 13 
                jugador2.velocidad = 13
                baseJ1 = getSiguienteBaseAir(jugador1)
                baseJ2 = getSiguienteBaseAir(jugador2)
                coordsj1tmp = getCoordenadasBase(baseJ1)
                coordsj2tmp = getCoordenadasBase(baseJ2)
                
                  
                threading.Thread(target = jugador1.moverse, args = (coordsj1tmp[0],coordsj1tmp[1],False)).start()

                threading.Thread(target = jugador2.moverse, args = (coordsj2tmp[0],coordsj2tmp[1],False)).start()
              
                
                jugadorAlcanzar = getJugadorMasCercaBalon(ncords[0],ncords[1])
                jugadorAlcanzar.velocidad = 20
                
                threading.Thread(target = jugadorAlcanzar.moverse, args = (xtmp,ytmp,False)).start()
                
                while pelota.moviendose: 
                    time.sleep(0.5)
                
                cR = getCoordenadasRol(baseJ1)
               
                pelota.moversePelota(cR[0],cR[1])
                
                if baseJ1 == "Home":
                    baseJ1 == "Bateador"
                jugadorSiguiente  = getJugador(baseJ1)
                
                ObjetivoBase = getCoordenadasBase(jugadorSiguiente.rol)
                jugadorSiguiente.velocidad = 10
                jugadorSiguiente.moverseConPelota(ObjetivoBase[0],ObjetivoBase[1],pelota)
                coords = getCoordenadasRol(baseJ2)
                pelota.velocidad = 5
                pelota.moversePelota(coords[0],coords[1])
                jugadorSiguiente  = getJugador(baseJ2)
                ObjetivoBase = getCoordenadasBase(jugadorSiguiente.rol)
                jugadorSiguiente.moverseConPelota(ObjetivoBase[0],ObjetivoBase[1],pelota)
                jugador1.salirDelCampoOut(jugador1,jugadores)
                jugador2.salirDelCampoOut(jugador2,jugadores)
                bandera = True

            if estado.escenario == "h":
                texto = "HOMERUN"
                
                pelota.velocidad = 7
                ncords = BatearBalon(1)
                sigestado = automata.estados.peek()
                if sigestado.escenario == "a":
                    movsA = []
                    while automata.estados.peek().escenario == "a":
                        e = automata.estados.pop()
                        movsA.append(e)
                        print "ESTADO : ",e.escenario
                mov = Stack()
                for m in movsA:
                    mov.push(m)
                mov.reverse()
               
                threading.Thread(target = pelota.moversePelota, args = (ncords[0],ncords[1])).start()
                threading.Thread(target = movimientoBases, args = (movsA,True)).start()
                intentoOut(mov,ncords[0],ncords[1],pelota,ncords)
          
                        
                
                bandera = True
            if estado.escenario == "tb":
                texto = "BUNT"
                
                
                ncords = BatearBalon(5)
                
           
                threading.Thread(target = pelota.moversePelota, args = (ncords[0],ncords[1])).start()
              
                agenteCercano = getJugadorMasCercaBalon(ncords[0],ncords[1])
                sigestado = automata.estados.peek()
                if sigestado.escenario == "a":
                    movsA = []  
                    while automata.estados.peek().escenario == "a":
                        e = automata.estados.pop()
                        movsA.append(e)
                        print "ESTADO : ",e.escenario


                mov = Stack()
                for m in movsA:
                    mov.push(m)
                mov.reverse()
                threading.Thread(target=movimientoBases,args = (movsA,False)).start()
                intentoOut(mov,ncords[0],ncords[1],pelota,ncords)
           
                bandera = True   
                
            if estado.escenario == "t":
                texto = "TRIPLETE"
                
                
                ncords = BatearBalon(3)
                sigestado = automata.estados.peek()
              
                threading.Thread(target = pelota.moversePelota, args = (ncords[0],ncords[1])).start()
                if sigestado.escenario == "a":
                    movsA = []
                    while automata.estados.peek().escenario == "a":
                        e = automata.estados.pop()
                        movsA.append(e)
                        print "ESTADO : ",e.escenario

                    mov = Stack()
                    for m in movsA:
                        mov.push(m)
                    mov.reverse()
                    threading.Thread(target = movimientoBases, args = (movsA,True) ).start()
                    intentoOut(mov,ncords[0],ncords[1],pelota,ncords)

                bandera = True
            if estado.escenario == "bo":
                texto = "BALK"
                sigestado = automata.estados.peek()
                pitcher = getJugador("Pitcher")
                pitcher.contador = 0
                pitcher.movimientoBalk = True
                time.sleep(2.5)
                if sigestado.escenario == "a":
                    movsA = []
                    while automata.estados.peek().escenario == "a":
                        e = automata.estados.pop()
                        movsA.append(e)
                        print "ESTADO : ",e.escenario

                    movimientoBases(movsA,True)



            if estado.escenario == "bp":
                texto = "BASE POR BOLAS"
                coords = getCoordenadasBase("Home")
                xtmp = coords[0] 
                ytmp = coords[1]
                xtmp = xtmp + random.randint(5,10)
                ytmp = ytmp + random.randint(5,10)
                ncords = [xtmp,ytmp]

                pelota.moversePelota(ncords[0],ncords[1])
               
                
                sigestado = automata.estados.peek()
                if sigestado.escenario == "a":
                    movsA = []
                    while automata.estados.peek().escenario == "a":
                        e = automata.estados.pop()
                        movsA.append(e)
                        print "ESTADO : ",e.escenario

                    movimientoBases(movsA,False)
                bandera = True
            if estado.escenario == "bg":
                texto = "BASE POR GOLPE"
                coords = getCoordenadasBase("Home")
                pelota.moversePelota(coords[0],coords[1])
                home = getJugador("Bateador")
                xh = coords[0] + 10 
                yh = coords[1] - 3
                home.moverse(xh,yh,False)
                home.moverse(coords[0],coords[1],False)
                bandera = True
                sigestado = automata.estados.peek()
                if sigestado.escenario == "a":
                    movsA = []
                    while automata.estados.peek().escenario == "a":
                        e = automata.estados.pop()
                        movsA.append(e)
                        print "ESTADO : ",e.escenario

                    movimientoBases(movsA,False)

            if estado.escenario == "fs":
                pelota.velocidad = 15
                ncords = BatearBalon(6)
                sigestado = automata.estados.peek()
                #pelota.moversePelota(ncords[0],ncords[1])
               
                if sigestado.escenario == "a":
                    movsA = []
                    while automata.estados.peek().escenario == "a":
                        e = automata.estados.pop()
                        movsA.append(e)
                 

                mov = Stack()
                for m in movsA:
                    mov.push(m)
                mov.reverse()
                threading.Thread(target = movimientoBases, args = (movsA,True) ).start()
                intentoOut(mov,ncords[0],ncords[1],pelota,ncords)
                bandera = True
                 

            if estado.escenario == "o":
                texto = "Intento de Robo de Base - Out "
                
                jugadorOut = buscarPorNumero(estado.base)
                print "El jugador OUT ES: ",jugadorOut.rol
                baseObjetivo = getSiguienteBaseAir(jugadorOut)
                print "La base objetivo es: ",baseObjetivo
                coordenadasCorrer = getCoordenadasBase(baseObjetivo)
                jugadorOut.velocidad = 17
                pelota.velocidad = 7
                threading.Thread(target = jugadorOut.moverse, args= (coordenadasCorrer[0],coordenadasCorrer[1],False)).start()
                baseObjetivoArray = getCoordenadasRol(baseObjetivo)
                pelota.moversePelota(baseObjetivoArray[0],baseObjetivoArray[1])
                if baseObjetivo == "Home":
                    baseObjetivo = "Tercera Base"

                jugadorDefensiva = getJugador(baseObjetivo)
                jugadorDefensiva.velocidad = 7
                baseObjetivoArray = getCoordenadasBase(baseObjetivo)
                jugadorDefensiva.moverseConPelota(baseObjetivoArray[0],baseObjetivoArray[1],pelota)
                jugadorOut.movimiento = False
                time.sleep(1.5)
                
                if jugadorOut.rol == "Bateador":
                    print "SI FUE BATEADOR EN OUT SOLO"
                    jugadorOut.MovimientoOut(jugadores)
                else:
                    print "NO BATEADOR ..."
                    gw = getwait()
                    jugadorOut.rol = "wait"
                    jugadorOut.ultimo = False
                    while jugadorOut.rol == "Bateador":
                        jugadorOut.rol = "wait"
                        jugadorOut.ultimo = False

                    threading.Thread(target = jugadorOut.moverse, args = (gw[0],gw[1],False)).start() 





def BatearBalon(distancia):

    pelota.setCoord(getCoordenadasRol("Pitcher"))
    coords= getCoordenadasBase("Home") 
    pelota.moversePelota(coords[0],coords[1])
    coords = getCoordenadasRol("Pitcher")
    print "pase get getCoordenadasRol"
    xtmp = coords[0]
    ytmp = coords[1]
    if bool(random.getrandbits(1)): 
         xtmp = xtmp + random.randint(20,70)
    else:
        xtmp = xtmp - random.randint(20,70)
    
    if distancia == 0: 
        ytmp = ytmp - random.randint(70,140)
    if distancia == 1: 
        ytmp = ytmp - random.randint(100,180)
    if distancia == 2: 
        ytmp = ytmp - random.randint(100,170)
    if distancia == 3:
        ytmp = ytmp - random.randint(120,180)
    if distancia == 4: 
        ytmp = ytmp - random.randint(100,150)
    if distancia ==5: 
        ytmp = ytmp +  random.randint(50,100)
    if distancia == 6:
        ytmp = ytmp - random.randint(130,170)
    if distancia == 7:
        ytmp = ytmp - random.randint(100,120)
 
    ncords = (xtmp,ytmp)
    #Obtengo un el siguiente estado sin removerlo de la pila para su verificacion
    sigestado = automata.estados.peek()
    #En caso que el siguiente estado se trate de un out, un hilo se encarga de hacer los movimientos necesarios y la pelota siga su recorrido sin interupcion
    
    threading.Thread(target =pelota.moversePelota,args= (ncords[0],ncords[1])).start()
    return ncords



## -------------------- intentoOut --------------------

def intentoOut(pilaMovimientos,xtmp,ytmp,pelota,ncords):
    contador = 0
    while not pilaMovimientos.isEmpty():

                    estadoactual = pilaMovimientos.pop()
                    AgentepuestoOut = buscarPorNumero(estadoactual.jugador)
                    print "Agente puesto Out : ",AgentepuestoOut.rol
                    if not getSiguienteBaseAir(AgentepuestoOut) == "Home":
                        if contador == 0:
                            cercano = getJugadorMasCercaBalon(xtmp,ytmp)
                        else: 
                            cercano = getJugadorMasCercaBalon(pelota.objX,pelota.objY)
                            ncords = (pelota.objX,pelota.objY)
                        objetivo = getSiguienteBaseAir(AgentepuestoOut) 
                        print "Objetivo: ",objetivo
                        coordsOut = getCoordenadasBase(objetivo)
                        agenteBase = getJugador(objetivo)
                        agenteBase.velocidad = 10
                        cercano.velocidad = 10
                        #AccionOut(self,cercano,objetivo,agenteBase,pelota,AgentepuestoOut,jugadores)
                        AgentepuestoOut.velocidad = 15
                        #threading.Thread(target = AgentepuestoOut.moverse, args = (coordsOut[0],coordsOut[1],False)).start()
                            
                        AgentepuestoOut.AccionOut(cercano,coordsOut,agenteBase,pelota,AgentepuestoOut,jugadores,1,ncords,True)
                        contador+=1

## -------------------- getSiguienteBaseAir --------------------
def getSiguienteBaseAir(jugador):
    
    if jugador.rol == "Bateador":
        return "Primera Base"
    if jugador.rol == "Campo1":
        return "Segunda Base"
    if jugador.rol == "Campo2":
        return "Tercera Base"
    if jugador.rol == "Campo3":
        return "Home"
    if jugador.rol == "Campo4":
        return "Home"
    if jugador.rol == "wait":
        return "Home"

## -------------------- movimientoBases --------------------
def movimientoBases(movimientos,ganarCarrera):
    global puntajeEquipo1,puntajeEquipo2,anuncioEquipo1,anuncioEquipo2
    mov = Stack()
    for m in movimientos:
        mov.push(m)
    mov.reverse()
    fueBateador = False
    while not mov.isEmpty():
        guion = mov.pop()
        print "Jugador numero = ",guion.jugador," base = ",guion.base
        agente = buscarPorNumero(guion.jugador)
        if ganarCarrera:
            agente.velocidad = 7
        else: 
            agente.velocidad = 15
       # print "Agente obtenido ROL: ",agente.rol," con numero: ",agente.numero 
       # print "AGENTE = ",agente
        if int(guion.base) == 1: 
            fueBateador = True
            
               
            print "En teoria el ",agente.rol," se mueve a primera base"
            agente.movimiento = True
            tmpCoords = getCoordenadasBase("Primera Base")
            threading.Thread(target = agente.moverse, args  = (tmpCoords[0],tmpCoords[1],False)).start()
            agente.rol = "Campo1"
            agente.ultimo = False
        if int(guion.base) == 2: 
            agente.movimiento = True
            print "En teoria el ",agente.rol," con numero: ",agente.numero," se mueve a segunda base"
            tmpCoords = getCoordenadasBase("Segunda Base")
            threading.Thread(target = agente.moverse, args  = (tmpCoords[0],tmpCoords[1],False)).start()
            agente.rol = "Campo2"
       
        if int(guion.base) == 3: 
            print "En teoria el ",agente.rol," con numero: ",agente.numero,"se mueve a Tercera base"
            agente.movimiento = True
            agente.rol = "Campo3"
          
            tmpCoords = getCoordenadasBase("Tercera Base")
            threading.Thread(target = agente.moverse, args  = (tmpCoords[0],tmpCoords[1],False)).start()
        if int(guion.base) == 4: 
            print "En teoria el ",agente.rol," con numero: ",agente.numero,"se mueve a home"
            agente.movimiento = True
            agente.rol = "Campo4"
            tmpCoords = getCoordenadasBase("Home")
            if agente.equipo == 1: 
                puntajeEquipo1 = str(int(puntajeEquipo1) + 1)
                anuncioEquipo1 = "EQUIPO 1: "+puntajeEquipo1

            else: 
                puntajeEquipo2 = str(int(puntajeEquipo2) + 1)
                anuncioEquipo2 = "EQUIPO 2: "+puntajeEquipo2
            threading.Thread(target = agente.moverse, args  = (tmpCoords[0],tmpCoords[1],True)).start()

    if fueBateador:
        while verificarActivos():
            time.sleep(1)
            print "hilos activos ... ",threading.activeCount()
        bateadorNuevo = Jugador()
        batActual = getJugador("wait")
        nuevoBateador = bateadorNuevo.getBateador(jugadores,batActual.equipo)
        nuevoBateador.rol = "Bateador"
        nuevoBateador.ultimo = True
        nuevoBateador.bateador = True
        print "Nuevo bateador con el numero: ",nuevoBateador.numero
        while nuevoBateador.rol == "wait":
            nuevoBateador.rol = "Bateador"
            nuevoBateador.ultimo = True
            nuevoBateador.bateador = True
            print "Reasignando ..."
        print "Acabo de signar a: ",nuevoBateador.rol
        threading.Thread(target = nuevoBateador.moverse, args = (446,610,False) ).start()
        #nuevoBateador.moverse(446,610)

## -------------------- asignarPosicion --------------------
def asignarPosicion(jugador):
    if jugador.rol == "Primera Base":
        print ""

## -------------------- verificarActivos --------------------

def verificarActivos():
    for agente in jugadores:
        if agente.moviendose:
            return True
    if pelota.moviendose:
        return True
    return False

## -------------------- Metodo Principal --------------------
def main():
    global fondo,screen,pelota,key,tux_pos_y,tux_pos_x,automata
    pygame.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("SIMULADOR BEISBOL CINVESTAV")
    
    # cargamos el fondo y una imagen (se crea objetos "Surface")
    fondo = pygame.image.load("media/baseballmap.png").convert()
    icon = pygame.image.load("media/logo_cinves.png").convert_alpha()        
    pygame.display.set_icon(icon)
    # Se crean todos los jugadores
    crearJugadores()
    #Creo el objeto automata 
    automata = Automata()
    #Creo la pila del automata
    automata.crearPilaAutomata()
    #Invierto el orden de la pila 
    automata.estados.reverse()
    pelota = Pelota()

    #Creo e inicio un hilo que se encarga de dibujar y acualizar los personajes y el mapa
    threading.Thread(target = dibujar).start()
    #Creo e inicio un hilo el cual se encarga de hacer el recorrido de la pila
    threading.Thread(target  = lectorPila).start() 
  
    
    
   
    
    while True:

        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print "x = ",tux_pos_x,", y = ",tux_pos_y
            if event.type == pygame.QUIT:
                key = False
                sys.exit()
 

if __name__ == "__main__":
    main()