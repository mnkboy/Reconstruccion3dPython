#Crearemos una funcion encargada de normalizar los puntos que necesitamos
#Devuelve una linea  con direccion normalizada, esto significa que el producto punto con W= 1 de la distancia 

#importamos las bibliotecas que nos serviran para realizar
#la tarea de calcular el algoritmo de 8 puntos
import cv2   #Esta biblioteca es la relativa a opencv 2
import cv	  #Esta biblioteca es la relativa a opencv 
import numpy as np #Esta biblioteca es la relativa a calculos matematicos en python
import scipy #Esta biblioteca es la relativa a calculos cientifico matematico en python
from math import * #Esta biblioteca la usamos para el calculo del modulo, y tambien trae varias utilidades matematicas como por ejemplo el sqrt
import random #Esta biblioteca nos permitira generar numeros aleatorios para la posterior ordenacion de nuestro vector

class NormalizadorDeLineas:
	def normalizaLinea(self, vectorLinea):
		#Obtenemos las dimensiones de nuestro vector linea
		m, n = vectorLinea.shape	
		
		lineaParcial = np.zeros((3,n))
		for i in range(n):
			lineaParcial[0,i] = sqrt( vectorLinea[0,i]**2 + vectorLinea[1,i]**2 )
		#for i in range(n):
		#	print(i,".- ",lineaParcial[0,i])
		
		#Triplicamos la fila 0 en las filas 1 y 2
		lineaParcial[1,:] = lineaParcial[0,:]
		lineaParcial[2,:] = lineaParcial[0,:]
		#for i in range(n):
		#	print(i," ", lineaParcial[0,i], " ", lineaParcial[1,i]," ", lineaParcial[2,i])
		#print(lineaParcial.shape)
		
		lineaNormalizada = vectorLinea / lineaParcial
		
		#for i in range(200):
		#	print(i," ", lineaNormalizada[0,i], " ", lineaNormalizada[1,i]," ", lineaNormalizada[2,i])
		#print(lineaNormalizada.shape)

		return lineaNormalizada
