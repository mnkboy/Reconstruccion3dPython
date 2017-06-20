#Crearemos una funcion encargada de normalizar los puntos que necesitamos
#Devuelve una transformacion de un vector columna para normalizar los puntos dentro de este vector

#importamos las bibliotecas que nos serviran para realizar
#la tarea de calcular el algoritmo de 8 puntos
import cv2   #Esta biblioteca es la relativa a opencv 2
import cv	  #Esta biblioteca es la relativa a opencv 
import numpy as np #Esta biblioteca es la relativa a calculos matematicos en python
import scipy #Esta biblioteca es la relativa a calculos cientifico matematico en python
from math import * #Esta biblioteca la usamos para el calculo del modulo, y tambien trae varias utilidades matematicas como por ejemplo el sqrt
import random #Esta biblioteca nos permitira generar numeros aleatorios para la posterior ordenacion de nuestro vector

class NormalizadorDePuntos:

	def normalizaPuntos(self, vectorPuntos):	
		#Convertimos el vector de 8 puntos que recibimos en un objeto de tipo Array
		vectorPuntosOriginal = np.array(vectorPuntos, dtype=float)
		vectorPuntos = np.array(vectorPuntos, dtype=float)
		
		#Calculamos el centroide para las coordenadas X
		centroideX = float(sum(vectorPuntos[:,0]))/float(len(vectorPuntos))
		#Calculamos el centroide para las coordenadas Y
		centroideY = float(sum(vectorPuntos[:,1]))/float(len(vectorPuntos))
		
		m, n = vectorPuntosOriginal.shape
		#Creamos un vector de 8 filas y 1 columna para replicar el valor del centroideX 
		columnaCentroideX = np.zeros( (m,1) )		
		columnaCentroideX[:,0] = centroideX
		
		#Creamos un vector de 8 filas y 1 columna para replicar el valor del centroideY				
		columnaCentroideY = np.zeros( (m,1) )						
		columnaCentroideY[:,0] = centroideY
		
		#Ahora restamos el valor de los centroides a cada una de las coordenadas de nuestro vector de 8 puntos
		columnaCentroideX = vectorPuntos[:,0] - columnaCentroideX[:,0]				
		columnaCentroideY = vectorPuntos[:,1] - columnaCentroideY[:,0]		
		
		#Colocamos los nuevos valores en sus respectivas posiciones		
		vectorPuntos[:,0] = columnaCentroideX
		vectorPuntos[:,1] = columnaCentroideY
		
		#Declaramos una variable que almacenara la sumatoria de la distancia promedio que existe entre los puntos
		sumatoriaX = 0.0
		sumatoriaY = 0.0
		
		desvEstandarX = 0.0
		desvEstandarY = 0.0
		
		#Iniciamos un ciclo que calculara la desviacion estandar para X y para Y
		for i in range(len(vectorPuntos)):
			#Realizamos la sumatoria de cada coordenada X a la que le restamos el centroide de X
			sumatoriaX = sumatoriaX + vectorPuntos[i,0]**2
			sumatoriaY = sumatoriaY + vectorPuntos[i,1]**2
			
		desvEstandarX = sqrt(sumatoriaX/m)
		desvEstandarY = sqrt(sumatoriaY/m)
		
		matrizH = np.array([[1/desvEstandarX,0,-centroideX/desvEstandarX],[0,1/desvEstandarY,-centroideY/desvEstandarY],[0,0,1]], dtype=float )
		
		#Crearemos un vector en donde almacenaremos nuestros puntos normalizados finales
		puntosFinalesParciales = np.zeros( (m,3) )
		
		#Copiamos nuestros puntos originales en la primera y segunda columnas
		puntosFinalesParciales[:,0] = vectorPuntosOriginal[:,0] 
		puntosFinalesParciales[:,1] = vectorPuntosOriginal[:,1] 
		#Y agregamos una columna de numeros 1 para normalizar nuestra matriz
		puntosFinalesParciales[:,2] = 1
		
		#Normalizamos los puntos originales, multiplicandolos por la matriz H
		puntosFinalesParciales = np.dot(matrizH, puntosFinalesParciales.conj().T)
		
		#Transponemos los puntos para que nos quede en forma (8,3)
		puntosFinalesParciales = puntosFinalesParciales.conj().T
		
		#Creamos una matriz de m filas x 2 columnas para guardar nuestros puntos normalizados
		puntosFinales = np.zeros( (m,3) )
					
		#Guardamos nuestros puntos normalizados
		puntosFinales[:,0] = puntosFinalesParciales[:,0]
		puntosFinales[:,1] = puntosFinalesParciales[:,1]
		puntosFinales[:,2] = 1	
			
		#Devolvemos nuestro array de puntos finales
		return puntosFinales, matrizH
