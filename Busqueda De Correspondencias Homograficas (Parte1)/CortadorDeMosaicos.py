#Esta clase se encargara de crear las ventanas de calculo para las correspondencias
#y las ventanas de busqueda en nuestra imagen para mover nuestra ventana donde se encuentra nuestra esquina principal.

#Importamos las bibliotecas que nos serviran para realizar
#la tarea de obtener las esquinas 
import cv2   #Esta biblioteca es la relativa a opencv 2
import cv	  #Esta biblioteca es la relativa a opencv 
import numpy as np #Esta biblioteca es la relativa a calculos matematicos en python
import scipy #Esta biblioteca es la relativa a calculos cientifico matematico en python
from math import * #Esta biblioteca la usamos para el calculo del modulo, y tambien trae varias utilidades matematicas
import random #Esta biblioteca nos permitira generar numeros aleatorios para la posterior ordenacion de nuestro vector

class CortadorDeMosaicos:

	def cortaMosaicoDeNxN(self, imagen, incrementoVerticalX, incrementoHorizontalY):
		#Declaramos un par de variables que almacenaran el ALTO y el ANCHO de la imagen que vamos a dividir en mosaicos
		verticalX  = imagen.height# Alto (X)
		horizontalY = imagen.width # Ancho (Y)
		
		#Declaramos un contador que almacenara el numero de ventanas en las que se dividio la imagen
		contadorDeVentanas = 0
		
		#Declaramos un vector que almacenara el numero de ventana asi como sus coordenadas iniciales y finales
		#Este vector tendra los siguientes datos
		#1.-Numero Ventana
		#2.- Posicion Inicial Horizontal
		#3.- Posicion Inicial Vertical
		#4.- Posicion Final Horizontal
		#5.- Posicion Final Vertical
		vectorCoordenadasDelMosaico = []
		
		#Comenzamos a recorrer nuestra imagen, con incrementos en X Alto
		for i in range(incrementoVerticalX, verticalX+1, incrementoVerticalX):
			#Comenzamos a recorrer nuestra imagen con incrementos en Y Ancho
			for j in range(incrementoHorizontalY, horizontalY+1, incrementoHorizontalY):
				
				#Guardamos coordenadas iniciales y finales en X de nuestro mosaico
				coordenadaInicialX = i - incrementoVerticalX
				coordenadaFinalX = i
				#Guardamos coordenadas iniciales y finales en Y de nuestro mosaico
				coordenadaInicialY = j - incrementoHorizontalY
				coordenadaFinalY = j
				
				#Incrementamos el numero de ventanas encontradas en 1
				contadorDeVentanas = contadorDeVentanas +1
				
				#Anadimos las coordenadas iniciales y finales del mosaico al vector que contendra a todas
				#Las coordenadas que delimitan los limites de los mosaicos
				vectorCoordenadasDelMosaico.extend([[contadorDeVentanas, coordenadaInicialX, coordenadaInicialY, (coordenadaFinalX-1), (coordenadaFinalY-1)]])		
				
		#Devolvemos como parametros una arreglo matricial tipo numpyArray
		#En el cual estan contenidos las coordenadas inciales y finales de nuestro mosaico				
		vectorCoordenadasDelMosaico = np.array(vectorCoordenadasDelMosaico, dtype=float)
				
		return vectorCoordenadasDelMosaico
