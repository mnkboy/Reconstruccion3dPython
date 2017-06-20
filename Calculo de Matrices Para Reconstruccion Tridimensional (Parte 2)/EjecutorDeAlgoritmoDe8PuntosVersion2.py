#Crearemos una funcion encargada de realizar el calculo del 
#algoritmo de 8 puntos para obtener una matriz F que nos sirva para 
#eliminar outlayers con ransac

#importamos las bibliotecas que nos serviran para realizar
#la tarea de calcular el algoritmo de 8 puntos
import cv2   #Esta biblioteca es la relativa a opencv 2
import cv	  #Esta biblioteca es la relativa a opencv 
import numpy as np #Esta biblioteca es la relativa a calculos matematicos en python
import scipy #Esta biblioteca es la relativa a calculos cientifico matematico en python
from math import * #Esta biblioteca la usamos para el calculo del modulo, y tambien trae varias utilidades matematicas como por ejemplo el sqrt
import random #Esta biblioteca nos permitira generar numeros aleatorios para la posterior ordenacion de nuestro vector
import NormalizadorDePuntos #Esta biblioteca nos permitira normalizar los puntos que deseamos utilizar para nuestro algoritmo de 8 puntos

class EjecutorDeAlgoritmoDe8Puntos:

	def ejecutaAlgoritmoDe8Puntos(self, vectorPuntosUno,vectorPuntosDos, Tuno, Tdos):	
		
		#Creamos un objeto de tipo normalizador de puntos para normalizar los puntos entrantes
		#objNormalizadorDePuntos = NormalizadorDePuntos.NormalizadorDePuntos()
		#Primero normalizamos los puntos ambas imagenes con la clase normalizador de puntos
		#vectorPuntosNormalizadosUno, Tuno = objNormalizadorDePuntos.normalizaPuntos(vectorPuntosUno)
		#vectorPuntosNormalizadosDos, Tdos = objNormalizadorDePuntos.normalizaPuntos(vectorPuntosDos)
		
		vectorPuntosNormalizadosUno = vectorPuntosUno
		vectorPuntosNormalizadosDos = vectorPuntosDos
		
		#Separamos las coordenadas de los puntos en un par de columnas de coordenadas en coordenadas X e Y
		coordenadasX = vectorPuntosNormalizadosUno[:,0]
		coordenadasY = vectorPuntosNormalizadosUno[:,1]
		
		#Ahora separamos las coordenadas de la segunda imagen
		coordenadasXPrimas = vectorPuntosNormalizadosDos[:,0]
		coordenadasYPrimas = vectorPuntosNormalizadosDos[:,1]
				
		#Creamos una matriz de 8 filas x 9 columnas para guardar nuestros puntos normalizados
		matrizA = np.zeros( (8,9) )		
		
		#Realizamos un producto punto de matrices, y agregamos una ultima columna de unos, para normalizar la matriz A
		#A = [ xp.*x xp.*y xp yp.*x yp.*y yp x y ones(8,1)];
		matrizA[:,0] = coordenadasXPrimas * coordenadasX
		matrizA[:,1] = coordenadasXPrimas * coordenadasY
		matrizA[:,2] = coordenadasXPrimas
		matrizA[:,3] = coordenadasYPrimas * coordenadasX
		matrizA[:,4] = coordenadasYPrimas * coordenadasY
		matrizA[:,5] = coordenadasYPrimas
		matrizA[:,6] = coordenadasX
		matrizA[:,7] = coordenadasY
		matrizA[:,8] = 1
		
		#Realizamos una descomposicion de valores singulares de la matrizA 
		U,D,V = np.linalg.svd(matrizA)
		
		#Transponemos la matriz V
		V = V.conj().T
		
		#Ahora guardamos unicamente la ultima columna de 9x1 de nuestra matriz V 
		fParcial = V[:,8]
		
		#Transponemos esa ultima columna para de jarla en forma de fila de 1x9
		fParcial = fParcial.conj().T
		
		#Ahora colocamos los elementos de nuestra fParcial en forma de una matriz de 3x3
		Ffinal = np.zeros( (3,3) )
		Ffinal[0,0:3] = fParcial[0:3]
		Ffinal[1,0:3] = fParcial[3:6]
		Ffinal[2,0:3] = fParcial[6:9]
				
		#Y realizamos una descomposicion en valores singulares de esta Ffinal
		U,D,V = np.linalg.svd(Ffinal)
		V = V.conj().T
				
		#Utilizamos la matriz diagonal que obtuvimos de la descomposicion de valores singulares
		D = np.diag((D))
		#Hacemos el ultimo elemento de la fila, y de la columna igual a cero
		D[2,2] = 0		
		#Dividimos todos los valores de la matriz entre el primer elemento de la matriz
		D = D / D[0,0]
			
		#Realizamos un producto punto entre la transpuesta de la matriz V, y la matriz D, 
		#El resultado de ese producto, volvemos a realizar otro producto punto por la matriz U
		#Este producto de productos puntos nos da una matriz F en escala normalizada
		FNormalizada = np.dot( U, np.dot( D, V.conj().T ) )

		#Denormalizamos la matriz final, realizando un producto punto entre la FNormalizada y la matriz T de los puntos de la imagen uno
		#Y despues al resultado de ese producto, lo multiplicamos producto punto por la matriz T transpuesta de los puntos de la imagen dos
		FDenormalizada = np.dot( Tdos.conj().T, np.dot( FNormalizada, Tuno ) )

		return FDenormalizada, FNormalizada
