#Esta clase se encargara de crear las ventanas de calculo para las correspondencias
#y las ventanas de busqueda en nuestra imagen para mover nuestra ventana donde se encuentra nuestra esquina principal.

#Importamos las bibliotecas que nos serviran para realizar
#la tarea de obtener las esquinas 
import cv2   #Esta biblioteca es la relativa a opencv 2
import cv	  #Esta biblioteca es la relativa a opencv 
import numpy #Esta biblioteca es la relativa a calculos matematicos en python
import scipy #Esta biblioteca es la relativa a calculos cientifico matematico en python
from math import * #Esta biblioteca la usamos para el calculo del modulo, y tambien trae varias utilidades matematicas

class EjecutorDeMedidasDeCorrelacion:
	
	
	#Esta funcion realizara la operacion de calculo de correlacion SAD (Sum of Absolute Differences)
	def ejecutaMedidaDeCorrelacionSAD(self, matrizImagenUno, matrizImagenDos, tamanoN ):				
		#Declaramos una variable que almacenara la sumatoria de la diferencia de cuadrados entre ambas matrices
		resultadoSumatoria = 0.0
		#Declaramos una variable que indicara el divisor por el cual se multiplicara la sumatoria SSD		
		divisor = tamanoN ** 2
		#Realizamos la sumatoria de la diferencia de cuadrados entre ambas matrices
		for i in range(0, tamanoN):
			for j in range(0, tamanoN):				
				resultadoSumatoria = (resultadoSumatoria + abs(matrizImagenUno[i][j] - matrizImagenDos[i][j]))
				#print(i)
		#######Devolvemos el valor de la funcion						
		return resultadoSumatoria/(divisor)
	
	#Esta funcion realizara la operacion de calculo de correlacion de Diferencia de Minimos Cuadrados (SSD Sum of Squared Differences)
	def ejecutaMedidaDeCorrelacionSSD(self, matrizImagenUno, matrizImagenDos, tamanoN ):				
		#Declaramos una variable que almacenara la sumatoria de la diferencia de cuadrados entre ambas matrices
		resultadoSumatoria = 0.0
		#Declaramos una variable que indicara el divisor por el cual se multiplicara la sumatoria SSD		
		divisor = tamanoN ** 2
		#Realizamos la sumatoria de la diferencia de cuadrados entre ambas matrices
		for i in range(0, tamanoN):
			for j in range(0, tamanoN):				
				resultadoSumatoria = (resultadoSumatoria + (matrizImagenUno[i][j] - matrizImagenDos[i][j])**2)
				#print(i)
		#######Devolvemos el valor de la funcion						
		return resultadoSumatoria/(divisor)
		
	#Esta funcion realizar la operacion de calculo de corelacion ZSSD (Zero-mean Sum of Squared Differences )
	def ejecutaMedidaDeCorrelacionZSSD(self, matrizImagenUno, matrizImagenDos, tamanoN ):				
		#Declaramos una variable que almacenara el promedio de la sumatoria de los valores de la ventana de NxN
		promedioImagenUno = self.ejecutaCalculoDelPromedio(matrizImagenUno, tamanoN)
		promedioImagenDos = self.ejecutaCalculoDelPromedio(matrizImagenDos, tamanoN)
		#Declaramos una variable que almacenara la sumatoria de la diferencia de cuadrados entre ambas matrices
		resultadoSumatoria = 0.0
		#Declaramos una variable que indicara el divisor por el cual se dividira la sumatoria de la medida de correlacion
		divisor = tamanoN ** 2
		#Realizamos la sumatoria de la diferencia de cuadrados entre ambas matrices
		for i in range(0, tamanoN):
			for j in range(0, tamanoN):				
				resultadoSumatoria = (resultadoSumatoria + ((matrizImagenUno[i][j] - promedioImagenUno) + (matrizImagenDos[i][j] -promedioImagenDos ) )**2 )
				#print(i)
		#######Devolvemos el valor de la funcion						
		return resultadoSumatoria/(divisor)
		
			
	#Esta funcion realizar la operacion de calculo de corelacion ZSAD (Zero-mean Sum of Absolute Differences )
	def ejecutaMedidaDeCorrelacionZSAD(self, matrizImagenUno, matrizImagenDos, tamanoN ):				
		#Declaramos una variable que almacenara el promedio de la sumatoria de los valores de la ventana de NxN
		promedioImagenUno = self.ejecutaCalculoDelPromedio(matrizImagenUno, tamanoN)
		promedioImagenDos = self.ejecutaCalculoDelPromedio(matrizImagenDos, tamanoN)
		#Declaramos una variable que almacenara la sumatoria de la diferencia de cuadrados entre ambas matrices
		resultadoSumatoria = 0.0
		#Declaramos una variable que indicara el divisor por el cual se dividira la sumatoria de la medida de correlacion
		divisor = tamanoN ** 2
		#Realizamos la sumatoria de la diferencia de cuadrados entre ambas matrices
		for i in range(0, tamanoN):
			for j in range(0, tamanoN):				
				resultadoSumatoria = (resultadoSumatoria + abs((matrizImagenUno[i][j] - promedioImagenUno) + (matrizImagenDos[i][j] -promedioImagenDos ) ) )
				#print(i)
		#######Devolvemos el valor de la funcion						
		return resultadoSumatoria/divisor
	
	#Esta funcion realizar la operacion de calculo de corelacion LSAD (Locally scaled Sum of Absolute Differences)
	def ejecutaMedidaDeCorrelacionLSAD(self, matrizImagenUno, matrizImagenDos, tamanoN ):				
		#Declaramos una variable que almacenara el promedio de la sumatoria de los valores de la ventana de NxN
		promedioImagenUno = self.ejecutaCalculoDelPromedio(matrizImagenUno, tamanoN)
		promedioImagenDos = self.ejecutaCalculoDelPromedio(matrizImagenDos, tamanoN)
		#Declaramos una variable que almacenara la sumatoria de la diferencia de cuadrados entre ambas matrices
		resultadoSumatoria = 0.0
		#Declaramos una variable que indicara el divisor por el cual se multiplicara la sumatoria SSD		
		divisor = tamanoN ** 2		
		#Declaramos una variable que almacenara la fraccion multiplicadora
		fraccionMultiplicadora = 0.0
		
		#Establecemos los parametros de la fraccion multiplicadora
		#verificamos que no se divida entre cero
		if promedioImagenDos == 0.0:
			fraccionMultiplicadora = 0.0
		else:
			fraccionMultiplicadora = promedioImagenUno/promedioImagenDos		
		#Realizamos la sumatoria de la diferencia de la suma absoluta de diferencias
		for i in range(0, tamanoN):
			for j in range(0, tamanoN):						
				#Calculamos la sumatoria para el metodo		
				resultadoSumatoria = ( resultadoSumatoria + abs( matrizImagenUno[i][j] - (fraccionMultiplicadora * matrizImagenDos[i][j]) ) )
				#print(i)
		#######Devolvemos el valor de la funcion						
		return resultadoSumatoria/divisor
		
		
	#Esta funcion realizar la operacion de calculo de corelacion LSSD (Locally scaled Sum of Squared Differences)
	def ejecutaMedidaDeCorrelacionLSSD(self, matrizImagenUno, matrizImagenDos, tamanoN ):				
		#Declaramos una variable que almacenara el promedio de la sumatoria de los valores de la ventana de NxN
		promedioImagenUno = self.ejecutaCalculoDelPromedio(matrizImagenUno, tamanoN)
		promedioImagenDos = self.ejecutaCalculoDelPromedio(matrizImagenDos, tamanoN)
		#Declaramos una variable que almacenara la sumatoria de la diferencia de cuadrados entre ambas matrices
		resultadoSumatoria = 0.0
		#Declaramos una variable que indicara el divisor por el cual se multiplicara la sumatoria SSD		
		divisor = tamanoN ** 2		
		#Declaramos una variable que almacenara la fraccion multiplicadora
		fraccionMultiplicadora = 0.0
		
		#Establecemos los parametros de la fraccion multiplicadora
		#verificamos que no se divida entre cero
		if promedioImagenDos == 0.0:
			fraccionMultiplicadora = 0.0
		else:
			fraccionMultiplicadora = promedioImagenUno/promedioImagenDos		
		#Realizamos la sumatoria de la diferencia de la suma absoluta de diferencias
		for i in range(0, tamanoN):
			for j in range(0, tamanoN):						
				#Calculamos la sumatoria para el metodo		
				resultadoSumatoria = ( resultadoSumatoria + ( matrizImagenUno[i][j] - (fraccionMultiplicadora * matrizImagenDos[i][j]) )**2 )
				#print(i)
		#######Devolvemos el valor de la funcion						
		return resultadoSumatoria/divisor
	
	
	
	#Esta funcion realizara la operacion de calculo de correlacion de NCC (Normalized Cross Correlation)
	def ejecutaMedidaDeCorrelacionNCC(self, matrizImagenUno, matrizImagenDos, tamanoN):		
		#Declaramos una variable que almacenara la sumatoria del numerador de la matriz
		numerador = 0.0
		
		#Declaramos una variable que almacenara la sumatoria del denominador de la matriz
		denominador = 0.0
				
		#Declaramos una variable que almacenara el resultado final de la medida de correlacion NCC
		resultadoNCC = 0.0
		
		#Realizamos la sumatoria de la resta del cada elemento menos el valor promedio de la ventana
		for i in range(0, tamanoN):
			for j in range(0, tamanoN):								
				numerador = numerador + ( matrizImagenUno[i][j] * matrizImagenDos[i][j] )
				denominador = denominador + ( (matrizImagenUno[i][j])**2  * (matrizImagenDos[i][j])**2  )
		
		#Comprobamos que no se divida entre cero
		if denominador == 0.0:
			#Si se divide entre cero, devolvemos cero como resultado, lo cual es el mejor valor que podemos obtener
			return 0
		#Si no es cero, procedemos con la division del numerador entre el denominador
		else:
			resultadoNCC = numerador / sqrt(denominador)
		return resultadoNCC
	
	#Esta funcion realizara la operacion de calculo de correlacion de ZNCC (Zero-mean Normalized Cross Correlation)
	def ejecutaMedidaDeCorrelacionZNCC(self, matrizImagenUno, matrizImagenDos, tamanoN):		
		#desviacionEstandarMatrizUno = self.ejecutaCalculoDeLaDesviacionEstandar(matrizImagenUno, tamanoN)
		#desviacionEstandarMatrizDos = self.ejecutaCalculoDeLaDesviacionEstandar(matrizImagenDos, tamanoN)
		promedioImagenUno = self.ejecutaCalculoDelPromedio(matrizImagenUno, tamanoN)
		promedioImagenDos = self.ejecutaCalculoDelPromedio(matrizImagenDos, tamanoN)

		#Declaramos una variable que almacenara la sumatoria del numerador de la matriz
		numerador = 0.0

		#Declaramos una variable que almacenara la sumatoria del denominador de la matriz
		denominador = 0.0
		
		#Declaramos una variable que almacenara el resultado final de la medida de correlacion ZNCC
		resultadoZNCC = 0.0
		#Realizamos la sumatoria de la resta del cada elemento menos el valor promedio de la ventana
		for i in range(0, tamanoN):
			for j in range(0, tamanoN):				
				numerador = numerador + ( (matrizImagenUno[i][j] - promedioImagenUno) * (matrizImagenDos[i][j] - promedioImagenDos) )
				denominador = denominador + ( ((matrizImagenUno[i][j] - promedioImagenUno)**2) * ((matrizImagenDos[i][j] - promedioImagenDos)**2) )
		
		#Comprobamos que no se divida entre cero
		if denominador == 0.0:
			#Si se divide entre cero, devolvemos cero como resultado, lo cual es el mejor valor que podemos obtener
			return 0
		#Si no es cero, procedemos con la division del numerador entre el denominador
		else:
			resultadoZNCC = numerador / sqrt(denominador)
		return resultadoZNCC
	
	#Esta funcion se encargara de calcular la desviacion estandar de los elementos de una matriz de NxN
	def ejecutaCalculoDeLaDesviacionEstandar(self,matrizImagen, tamanoN):
		#Declaramos una variable que almacenara la sumatoria de los elementos de la matriz
		resultadoSumatoria = 0.0
		#Declaramos una variable que indicara el divisor por el cual se dividira la sumatoria del valor de cada elemento de la ventana menos el valor promedio 
		divisor = tamanoN ** 2
		#Calculamos el valor promedio de los valores de la ventana de NxN
		valorPromedio = self.ejecutaCalculoDelPromedio(matrizImagen, tamanoN)
		#Realizamos la sumatoria de la resta del cada elemento menos el valor promedio de la ventana
		for i in range(0, tamanoN):
			for j in range(0, tamanoN):				
				resultadoSumatoria = resultadoSumatoria + (matrizImagen[i][j] - valorPromedio)**2
		#Realizamos el calculo de la desviacion estandar
		desviacionEstandar = sqrt(resultadoSumatoria/divisor)
		#######Devolvemos el valor de la funcion						
		return desviacionEstandar
	
	#Esta funcion se encarga de sacar el valor promedio de una ventana de NxN, el resultado es un valor escalar
	def ejecutaCalculoDelPromedio(self,matrizImagen, tamanoN):
		#Declaramos una variable que almacenara la sumatoria de los elementos de la matriz
		resultadoSumatoria = 0.0
		#Declaramos una variable que indicara el divisor por el cual se dividira la sumatoria
		divisor = tamanoN ** 2
		#Realizamos la sumatoria de los valores de la ventana de NxN
		for i in range(0, tamanoN):
			for j in range(0, tamanoN):				
				resultadoSumatoria = (resultadoSumatoria + (matrizImagen[i][j]))				
		#Dividimos la sumatoria entre el numero de elementos
		promedio = resultadoSumatoria / divisor
		#######Devolvemos el valor promedio
		return promedio		
	
	#Esta funcion s eencargara de calcular la distancia euclidiana entre un par de coordenadas X e Y
	def ejecutaCalculoDeDistanciaEuclidiana(self, puntoXUno, puntoYUno, puntoXDos, puntoYDos):		
		#Declaramos una variable que almacenara la distancia euclidiana entre ambos puntos
		distanciaEuclidiana = 0.0
		
		#Realizamos el calculo de la distancia euclidiana
		distanciaEuclidiana = sqrt((puntoXUno - puntoXDos)**2 + (puntoYUno - puntoYDos)**2)
						
		return distanciaEuclidiana
		
