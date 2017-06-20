#Crearemos una clase encargada de calcular varias matrices, por ejemplo la escencial, la matrizR y la matrizT
#Esta clase recibira como parametros una MatrizFundamental, un foco_x, un foco_y,
#y un par de puntos centrales punto_c_x y punto_c_y
import cv2   #Esta biblioteca es la relativa a opencv 2
import cv	  #Esta biblioteca es la relativa a opencv 
import numpy as np #Esta biblioteca es la relativa a calculos matematicos en python
import scipy #Esta biblioteca es la relativa a calculos cientifico matematico en python
from math import * #Esta biblioteca la usamos para el calculo del modulo, y tambien trae varias utilidades matematicas como por ejemplo el sqrt
import random #Esta biblioteca nos permitira generar numeros aleatorios para la posterior ordenacion de nuestro vector

class CalculadorDeMatrices:
		
	def calculaMatrizK(self, focoX, focoY, puntoC_X, puntoC_Y):		
		#En esta parte creamos una matrizK escencial de la siguiente forma:		
		#[focoX	0	puntoC_X]
		#[0	focoY	puntoC_Y]
		#[0		0		1	]
		
		matrizCamaraK = np.zeros((3, 3), dtype=float )		
				
		matrizCamaraK[0,0] = focoX
		matrizCamaraK[0,2] = puntoC_X
		matrizCamaraK[1,1] = focoY
		matrizCamaraK[1,2] = puntoC_Y
		matrizCamaraK[2,2] = 1.0
		
		return matrizCamaraK
	
	def calculaMatrizEsencial(self, matrizFundamental, matrizCamaraK):		
		#Calculamos la matriz esencial
		matrizEsencial = np.dot( matrizCamaraK.conj().T, np.dot( matrizFundamental, matrizCamaraK ) )
			
		return matrizEsencial

	#Esta funcion se encargara de calcular la matriz de rotacion R a partir de la matriz Escencial
	def calculaMatrizDeRotacionR(self, matrizEsencial):
		#Realizamos una descomposicion en valores singulares de nuestra matrizEsencial
		U,D,V = np.linalg.svd(matrizEsencial, full_matrices=True)				
		
		
		#Calculamos Rz( +(Pi/2) ) positiva
		RZpositiva = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
		
		RzdotVt = np.dot(RZpositiva.conj().T, V)		
		
		UdotRzdotVt = np.dot(U, RzdotVt)		
		
		#Guardamos la matrizR positiva
		matrizR = UdotRzdotVt;
		
		#Calculamos Rz( -(Pi/2) ) negativa
		RZnegativa = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]], dtype=float)
					
		RzNegdotVt = np.dot(RZnegativa.conj().T, V)		
		
		UdotRzNegdotVt = np.dot(U, RzNegdotVt)
		
		#Guardamos la matrizR negativa
		matrizRNegativa = UdotRzNegdotVt
		
		return matrizR, matrizRNegativa
			
		
	#Esta funcion se encargara de calcular la matriz de traslacion T gorrito de 3x3 a partir de la matriz Escencial
	def calculaMatrizDeTraslacionT(self, matrizEsencial):		
		
		#Calculamos Rz( +(Pi/2) ) positiva
		RZpositiva = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
		
		#Realizamos una descomposicion en valores singulares de nuestra matrizEsencial
		U,D,V = np.linalg.svd(matrizEsencial)				
		
		#Calculamos la matriz de los eigenvalores de la matriz escencial
		#Para colocarlos en forma de matriz de 3x3
		SigmaD = np.diag(D)
		
		#Hacemos el producto punto de la matriz SigmaD por la matriz U transpuesta
		SigmaDdotUt = np.dot(SigmaD, U.conj().T)
		
		
		
		#Hacemos el producto de Rz positiva por SigmaDotUt
		RzDotSigmaDdotUt = np.dot(RZpositiva, SigmaDdotUt)
		
		
		
		#Hacemos el producto de U por RzDotSigmaDdotUt
		UdotRzDotSigmaDdotUt = np.dot(U, RzDotSigmaDdotUt)
		
		
		#Guardamos nuestra matriz T gorrito positiva
		MatrizTGorritoPositiva = UdotRzDotSigmaDdotUt
		
		#Calculamos Rz( -(Pi/2) ) negativa
		RZnegativa = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]], dtype=float)
		
		#Comenzamos con los calculos para nuestra MatrizTGorritoNegativa
		
		#Hacemos el producto punto de la matriz SigmaD por la matriz U transpuesta
		SigmaDdotUt = np.dot(SigmaD, U.conj().T)
		
				
		#Hacemos el producto de Rz negativa por SigmaDotUt
		RzNegDotSigmaDdotUt = np.dot(RZnegativa, SigmaDdotUt)
		
				
		#Hacemos el producto de U por RzNegDotSigmaDdotUt
		UdotRzNegDotSigmaDdotUt = np.dot(U, RzNegDotSigmaDdotUt)
				
		
		#Guardamos nuestra matriz T gorrito negativa
		MatrizTGorritoNegativa = UdotRzNegDotSigmaDdotUt
		
		return MatrizTGorritoPositiva, MatrizTGorritoNegativa
		
	
	#Esta funcion se encargara de calcular el vectorT que es nuestro vector de traslacion
	def calculaVectorT(self, matrizTGorrito):
		#El vector T tiene la siguiente forma:
		#	 [T1]
		#T = [T2]
		#	 [T3]
		#
		vectorT = np.zeros((3), dtype=float )
		
		vectorT[0] = matrizTGorrito[2,1]
		vectorT[1] = matrizTGorrito[0,2]
		vectorT[2] = matrizTGorrito[1,0]
		
		return vectorT
		
	#Esta funcion se encarga de calcular la matriz inversa de K de la camara
	def calculaMatrizInversaCamaraK(self, matrizCamaraK):
			
		matrizInversaCamaraK = np.linalg.inv(matrizCamaraK)
		
		return matrizInversaCamaraK
		
	#Esta funcion se encarga de calcular la matriz RT (Matriz P1)
	def calculaMatrizRT(self, matrizR, vectorT):
	
		matrizRT = np.zeros((3, 4), dtype=float )
		
		matrizRT[:,0:3] = matrizR
		
		matrizRT[:,3] = vectorT
				
		return matrizRT
		
	#Esta funcion se encarga de calcular la matriz RT (Matriz P0)
	def calculaMatrizCanonicaRT(self):		
		
		#Esta matriz canonica tiene la siguiente forma:
		#[1	 0	0	0]
		#[0	 1	0	0]
		#[0	 0	1	0]	
		
		matrizCanonicaRT = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0]], dtype=float )
		
		return matrizCanonicaRT
