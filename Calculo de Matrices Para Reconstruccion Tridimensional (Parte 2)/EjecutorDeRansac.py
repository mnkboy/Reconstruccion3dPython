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

import EjecutorDeAlgoritmoDe8Puntos #Biblioteca encargada de realizar el calculo del algoritmo de 8 puntos
import NormalizadorDeLineas #Biblioteca encargada de realizar la normalizacion de la linea de puntos

class EjecutorDeRansac:

	def ejecutaRansac(self, vectorPuntosUno, vectorPuntosDos):			
		#Convertimos los vectores a arreglos de punto flotante
		vectorPuntosUno = np.array(vectorPuntosUno, dtype=float)
		vectorPuntosDos = np.array(vectorPuntosDos, dtype=float)
		
		#Creamos un objeto de tipo EjecutorDeAlgoritmoDe8Puntos para resolver el algoritmo de 8 puntos
		objEjecutorDeAlgoritmoDe8Puntos = EjecutorDeAlgoritmoDe8Puntos.EjecutorDeAlgoritmoDe8Puntos()
				
		#Creamos un objeto de la clase NormalizadorDeLineas para poder normalizar la multiplicacion de los (vectoresPunto .* F)
		objNormalizadorDeLineas = NormalizadorDeLineas.NormalizadorDeLineas();
		
		# Umbral de distancia de los pixeles inliers
		umbralDistanciaPixeles = 1.5
		# Probabilidad de que sea outlayer
		e = .60
		#Probabilidad de que de los resultados obtenidos estan realmente bien clasificados
		p = .99
		#Subconjunto de puntos que voy a tomar
		s = 8
		#Criterio de paro adaptativo N
		N = np.float32(log(1 - p))/np.float32(log(1 - (1 - e)**s))
		#Contador de muestras tomadas
		contadorDeMuestrasTomadas = 0
		#El mejor error lo situamos en infinito
		mejorErrorDeInliers = np.inf
		#Cantidad maxima de inliers
		cantidadMaximaDeInliers = 0
		#MejorF ahosta ahora
		mejorF = []		
		#Obtenemos los tamanos de los vectores de correspondencias
		m, n = vectorPuntosUno.shape	

		######### Aca comienza propiamente el algoritmo de optimizacion de RANSAC #########
		while (contadorDeMuestrasTomadas < N):
			#############Esta parte es para revolver las muestras ########################
			#Declaramos un vector de muestras aleatorias donde generaremos "m" numeros aleatorios para desordenar a nuestras correspondencias
			indicesAleatorios =  np.random.rand(m,1)
			
			#Creamos un vector de "m" filas por 2 columnas, en el que guardaremos los indices aleatorios, y los indices del 0 al "m"
			vectorMuestrasAleatoriasDos = np.zeros((m, 2))		
			
			#Guardamos nuestros indices aleatorios en nuestro vector de muestras
			vectorMuestrasAleatoriasDos[0:(m),0] = indicesAleatorios[0:(m),0]
					
			#Guardamos los numeros de forma consecutiva de 0 hasta m 
			vectorMuestrasAleatoriasDos[0:m,1] = range(0,m)
			
			#Ahora ordenamos de manera ascendente nuestros indices aleatorios, OJO esto nos devuelve el vector en forma de lista
			vectorMuestrasAleatoriasDos = sorted(vectorMuestrasAleatoriasDos, key=lambda valorDeOrdenamiento: valorDeOrdenamiento[0], reverse=False)
			
			#Reconvertimos nuestro vector a forma de array de nuevo
			vectorMuestrasAleatoriasDos = np.array(vectorMuestrasAleatoriasDos, dtype=float)
			
			#Tomamos las 8 primeras muestras de nuestro vector de muestras		
			vector8Muestras = vectorMuestrasAleatoriasDos[0:8,1]
			
			#############Fin de la parte para revolver las muestras #######################
			###############################################################################
			
			###############################################################################
			######## EN ESTA PARTE CALCULAMOS UNA F CON LOS 8 PUNTOS ALEATORIOS ###########
			
			#Creamos dos vectores que almacenaran los indices que indicaran que fila tomaremos para las muestras aleatorias
			muestrasVectorUno = np.zeros((len(vector8Muestras), 2))		
			muestrasVectorDos = np.zeros((len(vector8Muestras), 2))		
			
			#Incrementamos el contador del ciclo por cada iteracion de ransac
			contadorDeMuestrasTomadas = contadorDeMuestrasTomadas+1
			
			#Ahora guardamos las coordenadas "x" e "y" de las correspondencias
			#en los vectores de puntos 1 y 2, con los indices de nuestro vector 
			#aleatorio de muestras
			for i in range(len(vector8Muestras)):
				muestrasVectorUno[i,:] = vectorPuntosUno[vector8Muestras[i],0:2] 
				muestrasVectorDos[i,:] = vectorPuntosDos[vector8Muestras[i],0:2]
			
			#Calculamos una F parcial con el algoritmo de 8 puntos
			FDenormalizada, FNormalizada, Tuno, Tdos = objEjecutorDeAlgoritmoDe8Puntos.ejecutaAlgoritmoDe8Puntos(muestrasVectorUno, muestrasVectorDos)
			
			##### FIN DE LA PARTE DONDE  CALCULAMOS UNA F CON LOS 8 PUNTOS ALEATORIOS #####
			###############################################################################
			
			
			###############################################################################################
			############## EN ESTA PARTE CALCULAMOS LAS DISTANCIAS DE LA LINEA HACIA LOS PUNTOS ###########
			
			#Ahora realizamos un producto punto entre la matriz F y el vector de puntos
			#Este producto nos dara una linea previa para evaluar nuestros inliers
			LineaUnoPrevia =  np.dot(FDenormalizada,vectorPuntosUno.conj().T) 
			LineaDosPrevia =  np.dot(FDenormalizada.conj().T,vectorPuntosDos.conj().T) 
			
			#Normalizamos nuestra linea previa para dejar unicamente 2 filas por m columnas
			LineaUno = objNormalizadorDeLineas.normalizaLinea(LineaUnoPrevia)
			LineaDos = objNormalizadorDeLineas.normalizaLinea(LineaDosPrevia)
			
			#Ahora calculamos las distancias entre nuestras correspondencias y la linea normalizada
			distanciaUno = np.abs(np.dot(vectorPuntosDos, LineaUno))
			distanciaUno = np.array(distanciaUno.diagonal(), dtype=float)			
			
			distanciaDos = np.abs(np.dot(vectorPuntosUno, LineaDos))
			distanciaDos = np.array(distanciaDos.diagonal(), dtype=float)
			
			#Declaramos un vector de inliers que almacenara a todas las correspondencias, que sean menores
			#Al umbral de distancia
			vectorInliers = []
			
			#Iniciamos un ciclo de comprobacion que almacenara los pares de correspondencias en las que 
			#Ambos pares de correspondencias sean menores al umbral
			for i in range(len(distanciaUno)):				
				if(distanciaUno[i] < umbralDistanciaPixeles and distanciaDos[i] < umbralDistanciaPixeles):
					vectorInliers.extend([[distanciaUno[i], distanciaDos[i],i]])				
			#Reconvertimos la lista de inliers a vector de tipo array flotante
			vectorInliers = np.array(vectorInliers, dtype=float)
			
			########## FIN DE LA PARTE PARA CALCULAR LAS DISTANCIAS DE LA LINEA HACIA LOS PUNTOS ##########
			###############################################################################################
			
			###############################################################################################
			######### CALCULAMOS EL ERROR EN BASE AL NUMERO DE INLIERS OBTENIDOS CON LA F ACTUAL ##########
			
			errorDeInliers = 0.0
			#Verificamos que existan puntos que sean menores al umbral, osea que sean inliers
			if( len(vectorInliers) > 0):
				for i in range(len(vectorInliers)):
					#Tomamos la posicion donde se encuentras las coordenadas en nuestros vectores de puntos
					posicion = vectorInliers[i,2]
					#Iniciamos la sumatoria de los valores de las distancias al cuadrado 
					#De las distancia uno y distancia dos
					errorDeInliers = errorDeInliers + ((distanciaUno[posicion])**2 + (distanciaDos[posicion])**2)
				#Y dividimos esa sumatoria, entre la cantidad de inliers que obtuvimos con nuestra matriz F
				errorDeInliers = errorDeInliers / len(vectorInliers)
			else:
				#Si no hay inliers, entonces el error es infinito
				errorDeInliers = np.inf
			
			#Si encontramos un conjunto de 8 correspondencias que maximicen los inliers, entonces actualizamos los parametros
			if (len(vectorInliers) > cantidadMaximaDeInliers or (len(vectorInliers) == cantidadMaximaDeInliers and errorDeInliers < mejorErrorDeInliers)):				
				#Mantenemos los mejores parametros encontrados hasta ahora que maximicen el numero de inliers
				cantidadMaximaDeInliers = len(vectorInliers)
				mejorErrorDeInliers = errorDeInliers
				mejorF = FDenormalizada
				mejoresInliers = vectorInliers	
							
			# Actualizamos adaptativamente el criterio de paro N
			porcentajeDeInliers = np.float32(len(vectorInliers)) / np.float32(m)
			#"e" es el porcentaje de error con la actual cantidad de inliers
			e = 1.0 - porcentajeDeInliers			
			
			#Si el error "e" es mayor a cero, entonces actualizamos el valor de N
			if (e > 0):
				N = np.float32(log(1 - p))/np.float32(log(1 - (1 - e)**s))
			#Si el error es negativo, entonces tenemos un error absoluto
			else:
				N = 1		
			#Imprimimos los parametros de manera detallada cada 10 ciclos
			if((contadorDeMuestrasTomadas % 10) == 0):
				print("iteracion numero: ", contadorDeMuestrasTomadas, "Cantidad inliers / Tamano de coorrespondencias: ", cantidadMaximaDeInliers,"/", m, "Error de la muestra: ", mejorErrorDeInliers, "Criterio N: ", N )			
			#Imprimimos los parametros de manera rapida en cada iteracion
			print("it: ", contadorDeMuestrasTomadas, "inliers: ", cantidadMaximaDeInliers,"/", m, "Error: ", mejorErrorDeInliers, "N: ", N )
			
		#Al final imprimimos los parametros de manera detallada
		print("iteracion numero: ", contadorDeMuestrasTomadas, "Cantidad inliers / Tamano de coorrespondencias: ", cantidadMaximaDeInliers,"/", m, "Error de la muestra: ", mejorErrorDeInliers, "Criterio N: ", N )				
		
		###### FIN DEL CALCUL0 DEL ERROR EN BASE AL NUMERO DE INLIERS OBTENIDOS CON LA F ACTUAL #######
		###############################################################################################
		
		return FDenormalizada, vector8Muestras, vectorInliers
