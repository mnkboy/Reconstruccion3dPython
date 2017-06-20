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
import csv, operator#Esta biblioteca nos permitira leer desde un archivo CSV los puntos homograficos previamente calculados

import NormalizadorDePuntos #Biblioteca encargada de normalizar los puntos
import EjecutorDeAlgoritmoDe8Puntos #Biblioteca encargada de realizar el calculo del algoritmo de 8 puntos
import EjecutorDeAlgoritmoDe8PuntosVersion2 #Biblioteca encargada de realizar el calculo del algoritmo de 8 puntos
import NormalizadorDePuntosVersion2 #Biblioteca encargada de realizar la normalizacion de puntos segun estefano calamar 
import EjecutorDeRansac #Biblioteca encargada de realizar el calculo del algoritmo de Ransac
import EjecutorDeRansacVersion2 #Biblioteca encargada de realizar el calculo del algoritmo de Ransac de acuerdo al libro de zizerman
import CalculadorDeMatrices #Biblioteca encargada de realizar el calculo de la matriz esencial, fundamental, Rt entre otras
import LlenadorDeNubesDePuntos #Biblioteca encargada de llenar una nube de puntos a partir de todos los parametros calculados
import ManejadorDeArchivos #Biblioteca encargada de realizar el manejo de archivos para guardar en un archivo de texto nuestra nube de puntos

import math #Biblioteca encargada de los metodos matematicos basicos

#Creamos los objetos de las clases que utilizaremos en nuestro programa
objNormalizadorDePuntos = NormalizadorDePuntos.NormalizadorDePuntos()
objNormalizadorDePuntosVersionDos =  NormalizadorDePuntosVersion2.NormalizadorDePuntos()
objEjecutorDeAlgoritmoDe8Puntos = EjecutorDeAlgoritmoDe8Puntos.EjecutorDeAlgoritmoDe8Puntos()
objEjecutorDeAlgoritmoDe8PuntosVersionDos = EjecutorDeAlgoritmoDe8PuntosVersion2.EjecutorDeAlgoritmoDe8Puntos()
objEjecutorDeRansac = EjecutorDeRansac.EjecutorDeRansac()
objEjecutorDeRansacVersionDos = EjecutorDeRansacVersion2.EjecutorDeRansac()
objCalculadorDeMatrices = CalculadorDeMatrices.CalculadorDeMatrices()
objLlenadorDeNubesDePuntos = LlenadorDeNubesDePuntos.LlenadorDeNubesDePuntos()
objManejadorDeArchivos = ManejadorDeArchivos.ManejadorDeArchivos()

#Declaramos dos vectores en donde almacenaremos nuestros puntos leidos de nuestros CSV's
vectorPuntos1 = []
vectorPuntos2 = []

#Leemos el vector de puntos Uno
with open('vectorPuntos1.csv') as csvMatrizPuntos:
    vectorPuntosUno = csv.reader(csvMatrizPuntos)
    for reg in vectorPuntosUno:        
        vectorPuntos1.append([int(reg[0]),int(reg[1]),int(reg[2])])#Guardamos cada punto en nuestro vector

#Leemos el vector de puntos Dos
with open('vectorPuntos2.csv') as csvMatrizPuntos:
    vectorPuntosDos = csv.reader(csvMatrizPuntos)
    for reg in vectorPuntosDos:        
        vectorPuntos2.append([int(reg[0]),int(reg[1]),int(reg[2])])#Guardamos cada punto en nuestro vector

#Convertimos nuestras listas objetos de tipo Array
vectorPuntosUno = np.array(vectorPuntos1, dtype=int)
vectorPuntosDos = np.array(vectorPuntos2, dtype=int)


#parametros matriz K
ejeFocalX = 1636.54393 
ejeFocalY = 1637.23683 
puntoCentralX = 249.71486 
puntoCentralY = 251.944067


#Calculamos nuestra matriz fundamental
#FDenormalizada, vector8Muestras, vectorInliers = objEjecutorDeRansacVersionDos.ejecutaRansac(vectorPuntosUno, vectorPuntosDos)
FDenormalizada, vector8Muestras, vectorInliers = objEjecutorDeRansac.ejecutaRansac(vectorPuntosUno, vectorPuntosDos)

#Calculamos nuestra matriz de la camara K
matrizCamaraK = objCalculadorDeMatrices.calculaMatrizK(ejeFocalX, ejeFocalY, puntoCentralX, puntoCentralY)

#Calculamos nuestra matriz Esencial
matrizEsencial = objCalculadorDeMatrices.calculaMatrizEsencial(FDenormalizada, matrizCamaraK)

#Calculamos la matriz de Rotacion R
matrizDeRotacionR, matrizDeRotacionRNegativo = objCalculadorDeMatrices.calculaMatrizDeRotacionR(matrizEsencial)

#Calculamos la matriz de traslacion T
matrizTGorrito, matrizTGorritoNegativa = objCalculadorDeMatrices.calculaMatrizDeTraslacionT(matrizEsencial)

#Calculamos los vectores T positivos y T negativo
vectorT = objCalculadorDeMatrices.calculaVectorT(matrizTGorrito)

#Calculamos los vectores T positivos y T negativo
vectorTNegativo = objCalculadorDeMatrices.calculaVectorT(matrizTGorritoNegativa)

#Calculamos la matriz inversa de K
matrizInversaDeCamaraK = objCalculadorDeMatrices.calculaMatrizInversaCamaraK(matrizCamaraK)

#Calculamos la matriz RT Positiva para la solucion 1(P0_1)
matrizRT_P0 = objCalculadorDeMatrices.calculaMatrizRT(matrizDeRotacionR, vectorT)

#Calculamos la matriz RT Negativa para la solucion 2(P0_2)
matrizRT_P0_Negativa = objCalculadorDeMatrices.calculaMatrizRT(matrizDeRotacionRNegativo, vectorTNegativo)

#Calculamos la matriz canonica RT (P1)
matrizCanonicaRT_P1 = objCalculadorDeMatrices.calculaMatrizCanonicaRT()

#Calculamos nuestra matriz fundamental, normalizando cada una de las componentes
#entre la componente inferior derecha.
FDenormalizada = FDenormalizada / FDenormalizada[2,2]

#imprimimos la matriz fundamental
print("FDenormalizada")
print(FDenormalizada)



#imprimimos las matrices, que seran los parametros de nuestra reconstruccion 3D
print("matrizCamaraK")
print(matrizCamaraK)

print("Matriz de Esencial E")
print(matrizEsencial)

print("Matriz de rotacion R")
print(matrizDeRotacionR)

print("Matriz de rotacion R Negativo")
print(matrizDeRotacionRNegativo)

print("Matriz matrizTGorrito")
print(matrizTGorrito)


print("Matriz de traslacion T")
print(vectorT)

print("Matriz de traslacion T Negativo")
print(vectorTNegativo)

print("Matriz inversa de camara K")
print(matrizInversaDeCamaraK)

print("Matriz RT P0_1")
print(matrizRT_P0)

print("Matriz RT Negativa P0_2 ")
print(matrizRT_P0_Negativa)

print("Matriz Canonica RT P1")
print(matrizCanonicaRT_P1)

#########SOLUCION POSITIVA##############
#Calculamos la solucion positiva
nubeDePuntos3D = objLlenadorDeNubesDePuntos.llenaNubeDePuntos(vectorPuntosUno,vectorPuntosDos, matrizInversaDeCamaraK, matrizRT_P0, matrizCanonicaRT_P1)
#Salvamos la solucion en un archivo .csv
np.savetxt("nubeDePuntos3DPositiva.csv", nubeDePuntos3D, delimiter=",")

#Exportamos la solucion Positiva
directorio = "NubesDePuntos"
nombreDelArchivo = "ArchivoDeNubeDePuntosPositiva"
fechaDeCreacion = datetime.datetime.now()
modoDeApertura = "a+"
#Enviamos la nube de puntos y los parametros al manejador de archivos
objManejadorDeArchivos.manejaArchivo(directorio, nombreDelArchivo, fechaDeCreacion, nubeDePuntos3D, modoDeApertura)
#Imprimimos la fecha y la hora de creacion del archivo
##################################################

#########SOLUCION NEGATIVA##############
nubeDePuntos3DNegativa = objLlenadorDeNubesDePuntos.llenaNubeDePuntos(vectorPuntosUno,vectorPuntosDos, matrizInversaDeCamaraK, matrizRT_P0_Negativa, matrizCanonicaRT_P1)
#Salvamos la solucion en un archivo .csv
np.savetxt("nubeDePuntos3DNegativa.csv", nubeDePuntos3DNegativa, delimiter=",")

#Exportamos la solucion Negativa
directorio = "NubesDePuntos"
nombreDelArchivo = "ArchivoDeNubeDePuntosNegativa"
fechaDeCreacion = datetime.datetime.now()
modoDeApertura = "a+"
#Enviamos la nube de puntos y los parametros al manejador de archivos
objManejadorDeArchivos.manejaArchivo(directorio, nombreDelArchivo, fechaDeCreacion, nubeDePuntos3DNegativa, modoDeApertura)
#Imprimimos la fecha y la hora de creacion del archivo
print ("Fecha y hora = %s" % fechaDeCreacion)
##################################################


#Comprobamos la restriccion epipolar
for i in range(10):
	x1 = vectorPuntosUno[i,:]
	x2 = vectorPuntosDos[i,:]
	print( math.sqrt( (np.dot(x2, np.dot(FDenormalizada, x1.conj().T)) )**2 ) )

