#Esta clase se encargara de realizar el llenado de la nube de puntos

#Importamos las bibliotecas que nos serviran para realizar
#la tarea de obtener las esquinas 
import cv2   #Esta biblioteca es la relativa a opencv 2
import cv	  #Esta biblioteca es la relativa a opencv 
import numpy as np #Esta biblioteca es la relativa a calculos matematicos en python
import scipy #Esta biblioteca es la relativa a calculos cientifico matematico en python
from math import * #Esta biblioteca la usamos para el calculo del modulo, y tambien trae varias utilidades matematicas

class TrianguladorLinear:
	#Este metodo recibe como parametros a un puntoUnoPorKInv, puntoDosPorKInv, MatrizRT_P0, y MatrizRT_P1
	def calculaTriangulacionLinear(self, u, u1, P0, P1):
				
		#Construimos nuestra matriz A
		matrizA = np.zeros((4, 3), dtype=float )
		
						#u.x*P(2,0)-P(0,0)
		matrizA[0,0] = u[0]*P0[2,0]-P0[0,0]
						#u.x*P(2,1)-P(0,1)
		matrizA[0,1] = u[0]*P0[2,1]-P0[0,1]
						#u.x*P(2,2)-P(0,2)
		matrizA[0,2] = u[0]*P0[2,2]-P0[0,2]
		
						#u.y*P(2,0)-P(1,0)
		matrizA[1,0] = u[1]*P0[2,0]-P0[1,0]
						#u.y*P(2,1)-P(1,1)
		matrizA[1,1] = u[1]*P0[2,1]-P0[1,1]
						#u.y*P(2,2)-P(1,2)
		matrizA[1,2] = u[1]*P0[2,2]-P0[1,2]
		
						#u1.x*P1(2,0)-P1(0,0)
		matrizA[2,0] = u[0]*P1[2,0]-P1[0,0]
						#u1.x*P1(2,1)-P1(0,1)
		matrizA[2,1] = u[0]*P1[2,1]-P1[0,1]
						#u1.x*P1(2,2)-P1(0,2)
		matrizA[2,2] = u[0]*P1[2,2]-P1[0,2]
						
						#u1.y*P1(2,0)-P1(1,0)
		matrizA[3,0] = u[1]*P1[2,0]-P1[1,0]
						#u1.y*P1(2,1)-P1(1,1)
		matrizA[3,1] = u[1]*P1[2,1]-P1[1,1]
						#u1.y*P1(2,2)-P1(1,2)
		matrizA[3,2] = u[1]*P1[2,2]-P1[1,2]
		
		#Construimos nuestro vector B
		vectorB = np.zeros((4, 1), dtype=float )		
						#-(u.x*P(2,3)-P(0,3))
		vectorB[0,0] = -(u[0]*P0[2,3]-P0[0,3])
						#-(u.y*P(2,3)-P(1,3)),
		vectorB[1,0] = -(u[1]*P0[2,3]-P0[1,3])
						#-(u1.x*P1(2,3)-P1(0,3)),
		vectorB[2,0] = -(u[0]*P1[2,3]-P1[1,3])
						#-(u1.y*P1(2,3)-P1(1,3))
		vectorB[3,0] = -(u[1]*P1[2,3]-P1[1,3])
		
		#Resolvemos la incognita que seria nuestro punto tridimensional X		
		#cv.Solve(matrizA,vectorB,X,DECOMP_SVD)
		
		X = np.zeros((1, 3), dtype=float )	
		#matrizA = cv.fromarray(matrizA) 
		#vectorB = cv.fromarray(vectorB)
		#X = cv.fromarray(X)	 
		
		X = cv2.solve(matrizA, vectorB, X, 1)
		
		return X
