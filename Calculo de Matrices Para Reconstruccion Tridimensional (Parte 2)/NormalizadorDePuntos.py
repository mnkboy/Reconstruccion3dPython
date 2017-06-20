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
		sumatoria = 0.0
		
		#Iniciamos un ciclo que calculara la distancia promedio que existe entre los puntos de nuestro vector
		for i in range(len(vectorPuntos)):
			#Realizamos la sumatoria de cada coordenada X elevada al cuadrado + la coordenada Y elevada al cuadrado 
			#y le sacamos la raiz cuadrada a esa suma
			sumatoria = sumatoria + sqrt(vectorPuntos[i,0]**2 + vectorPuntos[i,1]**2)
			#Ahora dividimos la sumatoria entre el numero de puntos que tiene nuestro vector, y esa sera nuestra distancia promedio
		distanciaPromedio = sumatoria/len(vectorPuntos)		
		
		#Escalamos la distancia promedio
		escala = float(sqrt(2)) / float(distanciaPromedio)
				
		#Creamos una matriz con los centroides 
		matrizCentroides = np.array( [(1,0, -centroideX),(0,1,-centroideY),(0,0,1)], dtype=float )
		
				
		#Ahora crearemos una matriz T parcial con nuestra escala
		Tparcial = np.array( [(escala,0, 0),(0,escala,0),(0,0,1)], dtype=float )
		
		#Nuestra matriz T final sera el producto punto entre nuestra matrizCentroide y nuestra matriz Tparcial						
		Tfinal = np.dot(Tparcial,matrizCentroides)
		
		#Crearemos un vector en donde almacenaremos nuestros puntos normalizados finales
		puntosFinalesParciales = np.zeros( (m,3) )
		
		#Copiamos nuestros puntos originales en la primera y segunda columnas
		puntosFinalesParciales[:,0] = vectorPuntosOriginal[:,0] 
		puntosFinalesParciales[:,1] = vectorPuntosOriginal[:,1] 
		#Y agregamos una columna de numeros 1 para normalizar nuestra matriz
		puntosFinalesParciales[:,2] = 1
		
		#Realizamos el producto punto entre nuestra matriz de puntos normalizada y nuestra matriz Tfinal Transpuesta
		puntosFinalesParciales = np.dot(puntosFinalesParciales, Tfinal.conj().T)
						
		#Creamos una matriz de m filas x 2 columnas para guardar nuestros puntos normalizados
		puntosFinales = np.zeros( (m,2) )
		
		#Guardamos nuestros puntos normalizados
		puntosFinales[:,0] = puntosFinalesParciales[:,0]
		puntosFinales[:,1] = puntosFinalesParciales[:,1]				
		
		
		#Devolvemos nuestro array de puntos finales
		return puntosFinales, Tfinal
