#Esta clase se encargara de crear las ventanas de calculo para las correspondencias
#y las ventanas de busqueda en nuestra imagen para mover nuestra ventana donde se encuentra nuestra esquina principal.

#Importamos las bibliotecas que nos serviran para realizar
#la tarea de obtener las esquinas 
import cv2   #Esta biblioteca es la relativa a opencv 2
import cv	  #Esta biblioteca es la relativa a opencv 
import numpy #Esta biblioteca es la relativa a calculos matematicos en python
import scipy #Esta biblioteca es la relativa a calculos cientifico matematico en python
import EjecutorDeMedidasDeCorrelacion #Esta biblioteca es la relativa a ejecutar calculos de correlacion entre un par ventanas de imagenes
from math import * #Esta biblioteca la usamos para el calculo del modulo, y tambien trae varias utilidades matematicas

class CreadorDeVentanas:
	
	#Esta funcion creara una ventana de NxN de la cual tomaremos los valores para realizar el SSD de una ventana de NxN de dos imagenes
	def creaMatrizNxN(self,puntox,puntoy, imagen, tamanoN):				
		#Esta variable almacenara las filas de nuestra matriz de NxN		
		vectorRenglon = []		
		#Esta variable almacenara todas las filas de nuestra matriz de NxN
		matrizNxNTotal = []
		
		#Validamos que el tamano de la matriz NxN sea impar, si no es impar entonces no se procede a extraer la matriz NxN
		if tamanoN % 2 == 0:
			print('El tamano de la ventana debe de ser impar')
			return 0
		#Si el rango de la matriz NxN es impar entonces procedemos a crearla
		else:
			rango = tamanoN // 2
			for i in range((-rango), (rango+1)):				
				#Limpiamos el renglon a cada nueva vuelta de X
				vectorRenglon = []
				for j in range((-rango), (rango+1)):
					#print(imagen[puntox+i,puntoy+j])
					#Metemos cada elemento en el renglon
					vectorRenglon.append(imagen[puntox+i,puntoy+j])
					#print(i,j)
				#Metemos cada renglon dentro de una matriz
				matrizNxNTotal.extend([vectorRenglon])
									
			#print('Muy bien, el tamano de la ventana es impar', rango)
			#print(vectorRenglon)
			#print(matrizNxNTotal)	
		#Devolvemos la matriz completa		
		return matrizNxNTotal

	#Esta funcion realizara el recorrido y la operacion SSD entre dos ventanas
	def realizaRecorridoDeLaVentana(self,puntox, puntoy, imagenUno, imagenDos, tamanoN, tamanoRecorrido, criterioDeCorrelacion):
		#Declaramos una variable que almacenara la sumatoria de la diferencia de cuadrados
		resultadoSumatoria = 0		
		#Declaramos un vector que almacenara la diferencia de la suma de cuadrados, y las coordenadas X e Y donde sucedio esa diferencia
		vectorSumatoriaDeLaMedidaDeCorrelacion = []					
		
		#Declaramos una variable que almacenara un valorsote para poder ir comparandolo y obtener el menor de ellos
		valorMinimo = 9999999
		
		#Declaramos un vector que almacenara el valor minimo y sus coordenadas del SSD que mas se parezca al punto que buscamos
		vectorValorMinimo = []
		#Guardamos las coordenadas originales en donde realizaremos el recorrido para el SSD
		puntoXOriginal = puntox
		puntoYOriginal = puntoy
		#Ahora simplemente creamos una matriz de NxN de nuestro punto original, esta matriz no la moveremos a ningun lado
		matrizImagenUno = self.creaMatrizNxN(puntoXOriginal, puntoYOriginal, imagenUno, tamanoN)
		
		#Creamos un objeto de la clase EjecutorDeMedidasDeCorrelacion para poder realizar los calculos de correlacion entre un par de ventanas de imagenes
		ejecutorDeMedidasDeCorrelacion = EjecutorDeMedidasDeCorrelacion.EjecutorDeMedidasDeCorrelacion()
		
		for i in range((-tamanoRecorrido), (tamanoRecorrido)): #En range se pone que comienza en -N, y termina en +N
			for j in range((-tamanoRecorrido), (tamanoRecorrido)): #En range se pone que comienza en -N, y termina +N
				#Aca sumamos el valor del incremento que controla el recorrido de nuestra matriz de NxN
				puntoX = puntoXOriginal+i
				puntoY = puntoYOriginal+j
				
				#Ahora simplemente creamos una matriz de NxN de nuestro punto original, esta matriz no la moveremos a ningun lado
				matrizImagenDos = self.creaMatrizNxN(puntoX, puntoY, imagenDos, tamanoN)
				
				#En este bloque solo vemos cuando convergen ambas coordenadas
				if puntoX == puntoXOriginal:
					if  puntoY == puntoYOriginal:
						#Ahora calculamos la medida de correlacion de las dos matrices
						if criterioDeCorrelacion == 'zncc':
							resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionZNCC(matrizImagenUno, matrizImagenDos, tamanoN)
						elif criterioDeCorrelacion == 'ncc':
							resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionNCC(matrizImagenUno, matrizImagenDos, tamanoN)					
						elif criterioDeCorrelacion == 'ssd':
							resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionSSD(matrizImagenUno, matrizImagenDos, tamanoN)							
						elif criterioDeCorrelacion == 'zsad':
							resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionZSAD(matrizImagenUno, matrizImagenDos, tamanoN)
						elif criterioDeCorrelacion == 'lsad':
							resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionLSAD(matrizImagenUno, matrizImagenDos, tamanoN)
						elif criterioDeCorrelacion == 'zssd':
							resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionZSSD(matrizImagenUno, matrizImagenDos, tamanoN)	
						elif criterioDeCorrelacion == 'lssd':
							resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionLSSD(matrizImagenUno, matrizImagenDos, tamanoN)	
						elif criterioDeCorrelacion == 'sad':
							resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionSAD(matrizImagenUno, matrizImagenDos, tamanoN)	
							
								
							
						#Guardamos el valor de la medida de correlacion, asi como sus coordenadas en un vector de 3 elementos
						vectorSumatoriaDeLaMedidaDeCorrelacion.extend([[resultadoSumatoria, puntoX,puntoY]])				
						#print("punto convergente",i,j,resultadoSumatoria)
						#print("En este momento coinciden los puntos", puntoX, puntoXOriginal, puntoY, puntoYOriginal)
						#Buscamos ahora el valor minimo de todos nuestros valores SSD calculados
						if valorMinimo > resultadoSumatoria:
							#Limpiamos el vector valor minimo
							vectorValorMinimo = []
							#reasignamos el valor minimo a la nueva sumatoria del SSD
							valorMinimo = resultadoSumatoria				
							#Guardamos en un vector el valor minimo del SSD de nuestra matriz actual, y sus coordenadas correspondientes
							vectorValorMinimo.extend([[valorMinimo,puntoX,puntoY]])
							print("En este momento la diferencia de cuadrados es minima", vectorValorMinimo)
				else:										
					#Ahora calculamos la medida de correlacion de las dos matrices
					if criterioDeCorrelacion == 'zncc':
						resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionZNCC(matrizImagenUno, matrizImagenDos, tamanoN)
					elif criterioDeCorrelacion == 'ncc':
						resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionNCC(matrizImagenUno, matrizImagenDos, tamanoN)					
					elif criterioDeCorrelacion == 'ssd':
						resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionSSD(matrizImagenUno, matrizImagenDos, tamanoN)
					elif criterioDeCorrelacion == 'zsad':
						resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionZSAD(matrizImagenUno, matrizImagenDos, tamanoN)
					elif criterioDeCorrelacion == 'lsad':
						resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionLSAD(matrizImagenUno, matrizImagenDos, tamanoN)
					elif criterioDeCorrelacion == 'zssd':
						resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionZSSD(matrizImagenUno, matrizImagenDos, tamanoN)	
					elif criterioDeCorrelacion == 'lssd':
						resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionLSSD(matrizImagenUno, matrizImagenDos, tamanoN)	
					elif criterioDeCorrelacion == 'sad':
						resultadoSumatoria = ejecutorDeMedidasDeCorrelacion.ejecutaMedidaDeCorrelacionSAD(matrizImagenUno, matrizImagenDos, tamanoN)	
					#Guardamos el valor de la medida de correlacion, asi como sus coordenadas en un vector de 3 elementos
					vectorSumatoriaDeLaMedidaDeCorrelacion.extend([[resultadoSumatoria, puntoX,puntoY]])				
					#print(i, j, resultadoSumatoria)
					#Buscamos ahora el valor minimo de todos nuestros valores SSD calculados
					if valorMinimo > resultadoSumatoria:
						#Limpiamos el vector valor minimo
						vectorValorMinimo = []
						#reasignamos el valor minimo a la nueva sumatoria del SSD
						valorMinimo = resultadoSumatoria				
						#Guardamos en un vector el valor minimo del SSD de nuestra matriz actual, y sus coordenadas correspondientes
						vectorValorMinimo.extend([[valorMinimo,puntoX,puntoY]])
					
		#######Devolvemos el valor de la funcion			
		return vectorSumatoriaDeLaMedidaDeCorrelacion, vectorValorMinimo
