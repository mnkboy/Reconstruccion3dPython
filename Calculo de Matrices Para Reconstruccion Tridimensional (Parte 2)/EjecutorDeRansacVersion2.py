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

import EjecutorDeAlgoritmoDe8PuntosVersion2 #Biblioteca encargada de realizar el calculo del algoritmo de 8 puntos de acuerdo al libro de stefano calamar
import NormalizadorDePuntosVersion2 #Biblioteca encargada de realizar la normalizacion de puntos segun stefano calamar 

class EjecutorDeRansac:

	def ejecutaRansac(self, vectorPuntosUno, vectorPuntosDos):
		
		#Creamos un objeto de tipo EjecutorDeAlgoritmoDe8Puntos para resolver el algoritmo de 8 puntos
		objEjecutorDeAlgoritmoDe8PuntosVersionDos = EjecutorDeAlgoritmoDe8PuntosVersion2.EjecutorDeAlgoritmoDe8Puntos()						
		#Creamos un objeto de tipo normalizador de puntos para normalizar nuestros puntos de acuerdo al libro de stefano calamar
		objNormalizadorDePuntosVersionDos = NormalizadorDePuntosVersion2.NormalizadorDePuntos();
									
		#Convertimos los vectores a arreglos de punto flotante
		vectorPuntosUno = np.array(vectorPuntosUno, dtype=float)
		vectorPuntosDos = np.array(vectorPuntosDos, dtype=float)
		
		#Normalizamos los puntos del vector uno, y obtenemos su matriz de escalamiento T
		vectorPuntosUnoNormalizados, Tuno = objNormalizadorDePuntosVersionDos.normalizaPuntos(vectorPuntosUno)
		
		#Normalizamos los puntos del vector dos, y obtenemos su matriz de escalamiento T
		vectorPuntosDosNormalizados, Tdos = objNormalizadorDePuntosVersionDos.normalizaPuntos(vectorPuntosDos)
		
		#Declaramos un umbral para decidir que es inlier y que no lo es.
		umbral = 0.001				
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
			############# ESTA PARTE ES PARA REVOLVER LAS MUESTRAS ########################
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
			
			############# FIN DE LA PARTE ES PARA REVOLVER LAS MUESTRAS ###################
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
				muestrasVectorUno[i,:] = vectorPuntosUnoNormalizados[vector8Muestras[i],0:2]
				muestrasVectorDos[i,:] = vectorPuntosDosNormalizados[vector8Muestras[i],0:2]
			
			#Calculamos una F parcial con el algoritmo de 8 puntos
			FDenormalizada, FNormalizada = objEjecutorDeAlgoritmoDe8PuntosVersionDos.ejecutaAlgoritmoDe8Puntos(muestrasVectorUno, muestrasVectorDos, Tuno, Tdos)
			
			##### FIN DE LA PARTE DONDE  CALCULAMOS UNA F CON LOS 8 PUNTOS ALEATORIOS #####
			###############################################################################
			
			
			###############################################################################################
			############## EN ESTA PARTE CALCULAMOS LAS DISTANCIAS DE LA LINEA HACIA LOS PUNTOS ###########
			m, n = vectorPuntosUnoNormalizados.shape
			
			#Transponemos al vector de puntos uno a una matriz de 3 filas x m columnas
			vectorPuntosUnoNormalizadosTranspuestos = np.zeros( (3,m) )					
			vectorPuntosUnoNormalizadosTranspuestos = vectorPuntosUnoNormalizados.conj().T
			
			
			#Transponemos al vector de puntos dos a una matriz de 3 filas x m columnas
			vectorPuntosDosNormalizadosTranspuestos = np.zeros( (3,m) )					
			vectorPuntosDosNormalizadosTranspuestos = vectorPuntosDosNormalizados.conj().T
			
			
			x2tFx1 = np.zeros( (1,m) )					
			
			#x2tFx1[1,1] = np.dot(vectorPuntosDosNormalizadosTranspuestos[:,1].conj().T, np.dot(FNormalizada, vectorPuntosUnoNormalizadosTranspuestos[:,1]))
			
			#x2tFx1[1,1] = np.dot(vectorPuntosDosNormalizadosTranspuestos[:,1].conj().T, np.dot(FNormalizada, vectorPuntosUnoNormalizadosTranspuestos[:,1]))
						
			for i in range(m):
				x2tFx1[0,i] = np.dot(np.dot(vectorPuntosDosNormalizadosTranspuestos[:,i].conj().T, FNormalizada), vectorPuntosUnoNormalizadosTranspuestos[:,i])											
				#print(np.dot(np.dot(vectorPuntosUnoNormalizadosTranspuestos[:,i].conj().T, FNormalizada), vectorPuntosDosNormalizadosTranspuestos[:,i]))
			#x2tFx1 = zeros(1,length(x1));
			#for n = 1:length(x1)
			#x2tFx1(n) = x2(:,n)'*F{k}*x1(:,n);
			#end
			Fx1 = np.dot(FNormalizada, vectorPuntosUnoNormalizadosTranspuestos)
			Ftx2 = np.dot(FNormalizada.conj().T, vectorPuntosDosNormalizadosTranspuestos)
			#Fx1 = F{k}*x1;
			#Ftx2 = F{k}'*x2;     			
			
			#####################################################################################
			########### EN ESTE BLOQUE EVALUAREMOS LAS DISTANCIAS PARA DETERMINAR INLIERS #######
			#ELEVAMOS AL CUADRADO EL NUMERADOR
			
			#Declaramos un vector de inliers que almacenara a todas las correspondencias, que sean menores
			#Al umbral de distancia
			vectorInliers = []
			
			#Declaramos un vector que almacenara las coordenadas que son inliers para poder recalular la F 
			#Solo con coordenadas que sean inliers
			puntosUnoInliers = []
			puntosDosInliers = []
			
			#Iniciamos un ciclo de comprobacion que almacenara los pares de correspondencias en las que 
			#Ambos pares de correspondencias sean menores al umbral			
			for i in range(m):
				distancia = (x2tFx1[0,i]**2)/( (Fx1[0,i]**2 + Fx1[1,i]**2) + (Ftx2[0,i]**2+Ftx2[1,i]**2) )				
				#Si la distancia es menor al umbra, entonces tenemos un inlier
				if( distancia < umbral ):					
					#Guardamos la fila que es inlier junto con su error
					vectorInliers.extend([[i, distancia]])									
					#Guardamos las coordenadas de los puntos que son inliers
					puntosUnoInliers.extend([[vectorPuntosUno[i,0], vectorPuntosUno[i,1], 1]])				
					puntosDosInliers.extend([[vectorPuntosDos[i,0], vectorPuntosDos[i,1], 1]])				
						
			#Reconvertimos la lista de inliers a vector de tipo array flotante
			vectorInliers = np.array(vectorInliers, dtype=float)
			puntosUnoInliers = np.array(puntosUnoInliers, dtype=float)
			puntosDosInliers = np.array(puntosDosInliers, dtype=float)
			
			###############################################################################################
			######### CALCULAMOS EL ERROR EN BASE AL NUMERO DE INLIERS OBTENIDOS CON LA F ACTUAL ##########
			
			errorDeInliers = 0.0
			#Verificamos que existan puntos que sean menores al umbral, osea que sean inliers
			if( len(vectorInliers) > 0):
				for i in range(len(vectorInliers)):
					#Tomamos la posicion donde se encuentras las coordenadas en nuestros vectores de puntos
					posicion = vectorInliers[i,0]
					#Iniciamos la sumatoria de los valores de las distancias al cuadrado 
					#De las distancia uno y distancia dos
					errorDeInliers = errorDeInliers + ((vectorInliers[i,1])**2)
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
			if (e > 0 and e < 1):
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
		
		
		###############################################################################################
		############ VOLVEMOS A CALCULAR NUESTRA F AHORA SOLO CON NUESTROS PUNTOS INLIERS #############
		
		#Normalizamos los puntos del vector uno, y obtenemos su matriz de escalamiento T
		#puntosUnoInliersNormalizados, Tuno = objNormalizadorDePuntosVersionDos.normalizaPuntos(puntosUnoInliers)
		
		#Normalizamos los puntos del vector dos, y obtenemos su matriz de escalamiento T
		#puntosDosInliersNormalizados, Tdos = objNormalizadorDePuntosVersionDos.normalizaPuntos(puntosDosInliers)
		
		#Calculamos una F parcial con el algoritmo de 8 puntos
		#FDenormalizada, FNormalizada = objEjecutorDeAlgoritmoDe8PuntosVersionDos.ejecutaAlgoritmoDe8Puntos(puntosUnoInliersNormalizados, puntosDosInliersNormalizados, Tuno, Tdos)
		
		###############################################################################################
		###############################################################################################
		
		return FDenormalizada, vector8Muestras, vectorInliers
				
			
