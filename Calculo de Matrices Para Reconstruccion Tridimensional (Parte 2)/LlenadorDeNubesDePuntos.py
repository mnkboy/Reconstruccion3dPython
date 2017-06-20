#Esta clase se encargara de realizar el llenado de la nube de puntos

#Importamos las bibliotecas que nos serviran para realizar
#la tarea de obtener las esquinas 
import cv2   #Esta biblioteca es la relativa a opencv 2
import cv	  #Esta biblioteca es la relativa a opencv 
import numpy as np #Esta biblioteca es la relativa a calculos matematicos en python
import scipy #Esta biblioteca es la relativa a calculos cientifico matematico en python
from math import * #Esta biblioteca la usamos para el calculo del modulo, y tambien trae varias utilidades matematicas
import TrianguladorLinear #Esta biblioteca se encargara de realizar la triangulacion linear de nuestros puntos en 3D

class LlenadorDeNubesDePuntos:
	
	#Esta funcion creara una ventana de NxN de la cual tomaremos los valores para realizar el SSD de una ventana de NxN de dos imagenes
	def llenaNubeDePuntos(self,vectorPuntosUno,vectorPuntosDos, matrizInversaDeCamaraK, matrizRT_P0, matrizCanonicaRT_P1):				
		#Creamos un objeto de tipo trianguladorLinear para poder calcular nuestras coordenadas 3D
		objTrianguladorLinear = TrianguladorLinear.TrianguladorLinear()
		
		#Declaramos una nube de puntos en donde guardaremos todas nuestras coordenadas 3D
		nubeDePuntos3D =  np.zeros((len(vectorPuntosUno), 3), dtype=float )	
		
		print("Vamos a imprimir unos puntos normalizados")
		for i in range(len(vectorPuntosUno)):
			#Realizamos el proceso para puntoUno
			puntoUno = vectorPuntosUno[i,:]
			#print("punto uno normal")
			#print(puntoUno)
			#Multiplicamos nuestro punto homogeneizado, por la inversa de la matriz K (osea K^-1)
			#Para convertir la medida en pixeles del mundo digital de nuestro punto uno, a metros
			#Que seria la medida en el mundo real.
			puntoUnoPorKinv = np.dot(matrizInversaDeCamaraK, puntoUno)
			#print("punto uno inverso")
			#print(puntoUnoPorKinv)
			
			#Realizamos el proceso para puntoDos
			puntoDos = vectorPuntosDos[i,:]
			#print("punto dos normal")
			#print(puntoDos)
			puntoDosPorKinv = np.dot(matrizInversaDeCamaraK, puntoDos)
			#print("punto dos inverso")
			#print(puntoDosPorKinv)
			
			coordenadaX3D = objTrianguladorLinear.calculaTriangulacionLinear(puntoUnoPorKinv, puntoDosPorKinv, matrizRT_P0, matrizCanonicaRT_P1)			
			
			nubeDePuntos3D[i,0] = coordenadaX3D[1][0] #x
			nubeDePuntos3D[i,1] = coordenadaX3D[1][1] #y
			nubeDePuntos3D[i,2] = coordenadaX3D[1][2] #z
			
		return nubeDePuntos3D
