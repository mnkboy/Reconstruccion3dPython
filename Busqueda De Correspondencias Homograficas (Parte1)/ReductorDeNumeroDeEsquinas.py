#Crearemos una clase que se encargara de aplicar los pasos finales
#de la reduccion del numero de esquinas en una imagen

#importamos las bibliotecas que nos serviran para realizar
#la tarea de obtener las esquinas 
import cv2   #Esta biblioteca es la relativa a opencv 2
import cv	  #Esta biblioteca es la relativa a opencv 
import numpy as np #Esta biblioteca es la relativa a calculos matematicos en python
import scipy #Esta biblioteca es la relativa a calculos cientifico matematico en python
import EjecutorDeMedidasDeCorrelacion # Esta biblioteca incluye varios metodos de medidas de correlacion entre un par de imagenes estereo
import CortadorDeMosaicos
from matplotlib import pyplot as plt

class ReductorDeNumeroDeEsquinas:
	
	def ubicaLasCoordenadasDelMosaico(self, mapaDeCoordenadasEsquinas, coorXinicial, coorYinicial, coorXfinal, coorYfinal):
		#Declaramos un vector que almacenara unicamente a las coordenadas que pertenecen al mosaico actual
		vectorMosaicoActual = []
		#Iniciamos un ciclo que filtrara los puntos que se encuentren dentro del mosaico que estamos trabajando actualmente
		for i in range(len(mapaDeCoordenadasEsquinas)):
			if mapaDeCoordenadasEsquinas[i,1] >= coorXinicial and mapaDeCoordenadasEsquinas[i,1] <= coorXfinal:		
				if mapaDeCoordenadasEsquinas[i,2] >= coorYinicial and mapaDeCoordenadasEsquinas[i,2] <= coorYfinal:		
					vectorMosaicoActual.extend([[ mapaDeCoordenadasEsquinas[i,0], mapaDeCoordenadasEsquinas[i,1], mapaDeCoordenadasEsquinas[i,2] ]])
				
		
		vectorMosaicoActual = sorted(vectorMosaicoActual, key=lambda valorEsquinidad: valorEsquinidad[0], reverse = True)
		
		#Devolvemos como parametros una arreglo matricial tipo numpyArray
		#En el cual almacenamos las esquinas que se encuentran dentro del mosaico actual
		vectorMosaicoActual = np.array(vectorMosaicoActual, dtype=float)
		
		return vectorMosaicoActual
	
	def reduceEsquinas(self, vectorMosaicoActual, criterioDistanciaPixeles):
		#Declaramos una variable que sera la que indique si la esquina cumple con las caracteristicas para ser insertado o no
		banderaDeInsercion = 0
		#Declaramos un contador que indicara el numero de esquinas aniadidos y no sobre pasarnos del limite
		contador = 1
		#Declaramos un contador de esquinas que sera el que nos indique la cantidad maxima de esquinas que insertaremos para dibujar por mosaico
		numeroDeEsquinasADibujar = 5
		#Declaramos un vector que almacenara el valor hessiano, y las coordenadas X e Y de nuestras esquinas
		vectorPuntosADibujar = []
		#Creamos un objeto de la clase EjecutorDeMedidasDeCorrelacion para poder calcular la distancia euclidiana entre las coordenadas de dos esquinas
		objEjecutorDeMedidasDeCorrelacion = EjecutorDeMedidasDeCorrelacion.EjecutorDeMedidasDeCorrelacion()

		vectorMosaicoActual = sorted(vectorMosaicoActual, key=lambda Hessiano: Hessiano[0], reverse = True)
		vectorPuntosADibujar.extend([[ vectorMosaicoActual[0][0], vectorMosaicoActual[0][1], vectorMosaicoActual[0][2] ]])

		#Iniciamos un ciclo que recorrera las N esquinas de nuestro mosaico actual
		for i in range(1,len(vectorMosaicoActual),1):
			#En cada vuelta completa de nuestro vector puntos a dibujar, reiniciamos el criterio de insercion
			banderaDeInsercion = 0
			#Iniciamos un ciclo que recorrera las N esquinas insertadas que cumplieron el criterio de insercion
			for j in range(len(vectorPuntosADibujar)):
				#Estas variables son para las coordenadas del mosaico actual
				coorXinicial = vectorMosaicoActual[i][1]
				coorYinicial = vectorMosaicoActual[i][2]

				#Estas variables son para el vector que se crea dinamicamente de las esquinas a dibujar
				coorXfinal = vectorPuntosADibujar[j][1]
				coorYfinal = vectorPuntosADibujar[j][2]
				
				#Calculamos la distancia euclidiana entre ambos puntos
				distancia = objEjecutorDeMedidasDeCorrelacion.ejecutaCalculoDeDistanciaEuclidiana(coorXinicial, coorYinicial, coorXfinal, coorYfinal)
				
				#Verificamos que el punto que se comprueba cumpla y su distancia sea mayor al criterio de distancia en pixeles
				if distancia <= criterioDistanciaPixeles:
					#print("La distancia es menor al criterio: ", distancia)
					banderaDeInsercion = 1		
			
			#Si la bandera de insercion no cambio, entonces la esquina cumple los criterios de insercion en cuanto a distancia
			if banderaDeInsercion == 0:
				#Si la cantidad de puntos ya se lleno, entonces detenemos el ciclo de global de comprobacion e insercion
				if contador == numeroDeEsquinasADibujar:
					break
				else:
					#Si la cantidad de puntos a dibujar todavia no se llena, entonces insertamos la nueva esquina			
					vectorPuntosADibujar.extend([[ vectorMosaicoActual[i][0], vectorMosaicoActual[i][1], vectorMosaicoActual[i][2] ]])
					contador = contador +1 
					
		#Devolvemos como parametros una arreglo matricial tipo numpyArray
		#En este arreglo van todas las esquinas que cumplen con el criterio de insercion
		vectorPuntosADibujar = np.array(vectorPuntosADibujar, dtype=float)
					
		return vectorPuntosADibujar
