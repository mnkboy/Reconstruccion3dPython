#Crearemos una funcion encargada de normalizar los puntos que necesitamos 
#Devuelve una transformacion de un vector columna para normalizar los puntos dentro de este vector

#importamos las bibliotecas que nos serviran para realizar
#la tarea de calcular el algoritmo de 8 puntos
import cv2   #Esta biblioteca es la relativa a opencv 2
import cv	  #Esta biblioteca es la relativa a opencv 
import numpy as np #Esta biblioteca es la relativa a calculos matematicos en python
import scipy #Esta biblioteca es la relativa a calculos cientifico matematico en python
import random #Esta biblioteca nos permitira generar numeros aleatorios para la posterior ordenacion de nuestro vector
import datetime #Esta biblioteca nos permitira obtener el tiempo y la fecha de nuestra computadora 
import math #Biblioteca encargada de los metodos matematicos basicos


import CalculadorDeMatrices #Biblioteca encargada de realizar el calculo de la matriz esencial, fundamental, Rt entre otras
import EjecutorDeRansacVersion2 #Biblioteca encargada de realizar el calculo del algoritmo de Ransac de acuerdo al libro de zizerman

#Declaramos todos nuestros objetos que usaremos para el calculo de nuestra reconstruccion
objCalculadorDeMatrices = CalculadorDeMatrices.CalculadorDeMatrices()

objEjecutorDeRansacVersionDos = EjecutorDeRansacVersion2.EjecutorDeRansac()

#Declaramos los parametros de nuestra matriz K
ejeFocalX = 1636.54393 
ejeFocalY = 1637.23683 
puntoCentralX = 249.71486 
puntoCentralY = 251.944067

#Creamos una matriz K
matrizCamaraK = objCalculadorDeMatrices.calculaMatrizK(ejeFocalX, ejeFocalY, puntoCentralX, puntoCentralY)

#Calculamos la matriz inversa de K
matrizInversaDeCamaraK = objCalculadorDeMatrices.calculaMatrizInversaCamaraK(matrizCamaraK)

#generar numeros aleatorios
#rangoX  -2 +2
#rangoY -1.5 + 1.5
#rangoZ 1.5 5.0
#Declaramos las dimensiones de la matriz de coordenadas homogeneas aleatorias
m = 4
n = 200

#Declaramos un vector que almacenara a nuestras coordenadas homogeneas de 1x4
matrizPuntosArtificiales = np.zeros((m, n), dtype=float )


#Iniciamos un ciclo para generar 500 coordenadas homogeneas
for i in range(n):
	x =  random.uniform(-2, 2)
	y =  random.uniform(-1.5, 1.5)
	z =  random.uniform(1.5, 5)
	
	matrizPuntosArtificiales[0,i] = x
	matrizPuntosArtificiales[1,i] = y
	matrizPuntosArtificiales[2,i] = z
	matrizPuntosArtificiales[3,i] = 1
	
#Imprimimos las componentes	
#print("matrizPuntosArtificiales[i]")
#for i in range(m):
	#print(matrizPuntosArtificiales[i])
	


#Creamos un vector T
vectorT = np.array([0,.15,0], dtype=float )

#Imprimimos T
print("matrizT")
print(vectorT[0],vectorT[1],vectorT[2])

#Convertimos los grados a radianes
teta = float(15) * float((3.1416/180))

#Creamos una matriz R 
matrizR = np.array([[1,0,0],[0,math.cos(teta),-math.sin(teta)],[0, math.sin(teta),math.cos(teta)]], dtype=float )

#Imprimimos R
print("matrizR")
print(matrizR)


#Vamos a convertir nuestro vectorT en una matriz T gorrito
matrizTGorrito = np.array([[0,-vectorT[2],vectorT[1]],[vectorT[2],0,-vectorT[0]],[-vectorT[1],vectorT[0],0]], dtype=float )

print("matrizTGorrito")
print(matrizTGorrito)

#Calculamos P0
matrizP0 = objCalculadorDeMatrices.calculaMatrizRT(matrizR, vectorT)

#Imprimimos P0
print("matrizP0")
print(matrizP0)

#Calculamos P1, matriz canonica
matrizP1 = objCalculadorDeMatrices.calculaMatrizCanonicaRT()

#Imprimimos P1
print("matrizP1")
print(matrizP1)

############Realizamos el calculo de los puntos para P0################
#Multiplicamos P0 por la matriz de n puntos artificiales
vectorResultante = np.dot(matrizP0, matrizPuntosArtificiales)

#Tomamos la tercera fila de vector resultante y la guardamos en un vector, para usala como el divisor
filaDivisoriaVectorResultante = vectorResultante[2,:]

#Dividimos al vector Resultante entre la fila divisoria 
vectorResultante[:,:] = vectorResultante[:,:] / filaDivisoriaVectorResultante

###################Fin del calculo de los puntos para P0###############

############Realizamos el calculo de los puntos para P1################
#Multiplicamos P0 por la matriz de 500 vectores
vectorResultanteP1 = np.dot(matrizP1, matrizPuntosArtificiales)

#Tomamos la tercera fila de vector resultante y la guardamos en un vector, para usala como el divisor
filaDivisoriaVectorResultante = vectorResultanteP1[2,:]

#Dividimos al vector Resultante entre la fila divisoria 
vectorResultanteP1[:,:] = vectorResultanteP1[:,:] / filaDivisoriaVectorResultante

###################Fin del calculo de los puntos para P1################
filas = n
columnas = 3

#Creamos un vector para guardar nuestros puntos para la imagen 1
vectorPuntosUno = np.zeros((filas, columnas), dtype=float )		

#Creamos un vector para guardar nuestros puntos para la imagen 2
vectorPuntosDos = np.zeros((filas, columnas), dtype=float )		


for i in range(n):
	#print(i, "X = ", vectorResultante[0,i], "Y = ",vectorResultante[1,i], "Z = ",vectorResultante[2,i])
	vectorPuntosUno[i,:] = vectorResultante[0,i], vectorResultante[1,i], vectorResultante[2,i]
	#print(vectorPuntosUno[i])


for i in range(n):
	#print(i, "X = ", vectorResultanteP1[0,i], "Y = ",vectorResultanteP1[1,i], "Z = ",vectorResultanteP1[2,i])
	vectorPuntosDos[i,:] = vectorResultanteP1[0,i], vectorResultanteP1[1,i], vectorResultanteP1[2,i]
	#print(vectorPuntosDos[i])
	

#Se premultiplica por la matriz K para convertir los puntos mapeados en pixeles en puntos ideales mapeados a metros
#Multiplicamos todos los puntos artificiales por K inversa antes de entrar

vectorPuntosUno = np.dot(vectorPuntosUno,matrizInversaDeCamaraK.conj().T)
#for i in range(n):
#	vectorPuntosUno[i,:] = np.dot(matrizInversaDeCamaraK, vectorPuntosUno[i,:])
	
#Multiplicamos todos los puntos artificiales por K inversa antes de entrar

vectorPuntosDos = np.dot(vectorPuntosDos, matrizInversaDeCamaraK.conj().T)
#for i in range(n):
#	vectorPuntosDos[i,:] = np.dot(matrizInversaDeCamaraK, vectorPuntosDos[i,:])


#Calculamos la matriz fundamental, y la fundamental, se vuelve ahora nuestra matriz esencial
#Por la premultiplicacion, y el sistema se convierte en un sistema ideal
FDenormalizada, vector8Muestras, vectorInliers = objEjecutorDeRansacVersionDos.ejecutaRansac(vectorPuntosUno, vectorPuntosDos)
print("Matriz FDenormalizada")
print(FDenormalizada)

FDenormalizadaDividida = FDenormalizada/FDenormalizada[2,2]

print("Matriz FDenormalizada")
print(FDenormalizadaDividida)

print("np.linalg.det(FDenormalizadaDividida)")
print(np.linalg.det(FDenormalizadaDividida))

#Realizamos una descomposicion en valores singulares de nuestra matrizEsencial
U,D,V = np.linalg.svd(FDenormalizadaDividida)				

print("U")
print(U)
print("D")
print(D)
print("V")
print(V)

print(np.linalg.det(U))

#Calculamos la matriz de Rotacion R
matrizDeRotacionR, matrizDeRotacionRNegativo = objCalculadorDeMatrices.calculaMatrizDeRotacionR(FDenormalizadaDividida)
print("matrizDeRotacionR")
print(matrizDeRotacionR)

print("matrizDeRotacionRNegativo")
print(matrizDeRotacionRNegativo)

#Calculamos la matriz de traslacion T
matrizTGorrito, matrizTGorritoNegativa = objCalculadorDeMatrices.calculaMatrizDeTraslacionT(FDenormalizadaDividida)
print("matrizTGorrito")
print(matrizTGorrito)

print("matrizTGorritoNegativa")
print(matrizTGorritoNegativa)

#Calculamos los vectores T positivos y T negativo
vectorT = objCalculadorDeMatrices.calculaVectorT(matrizTGorrito)

print("vectorT")
print(vectorT)

print("Comprobando la restriccion epipolar")
for i in range(10):
	print(np.dot(vectorPuntosDos[i,:].conj().T, np.dot(FDenormalizadaDividida, vectorPuntosUno[i,:])))

E = np.dot(matrizTGorrito, matrizR)

print("E")
print(E)


