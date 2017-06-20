#Sehicieron correcciones al codigo el dia 14/11/2014
#Se corrigio el formato de guardado en el vector, y se devuelve 
#En forma de numpyArray.
#Esta clase se encargara de calcular para cada pixel
#dependiendo del umbral hessiano si se trata de una esquina
#si es mayor al umbral, de otro modo, si es menor
#al umbral, entonces no es esquina

#Importamos las bibliotecas que nos serviran para realizar
#la tarea de obtener las esquinas 
import cv2   #Esta biblioteca es la relativa a opencv 2
import cv	  #Esta biblioteca es la relativa a opencv 
import numpy as np #Esta biblioteca es la relativa a calculos matematicos en python
import scipy #Esta biblioteca es la relativa a calculos cientifico matematico en python

class DetectorDeEsquinasDeHarris:

	def detectaEsquinas(self, image, imcolor, umbralHessiano):
		#Trazamos el mapa de esquinas 
		mapaDeEsquinas = cv.CreateMat(image.height, image.width, cv.CV_32FC1)

		#Implementamos la deteccion de esquinas con el 
		#algoritmo de harris hecho con python.
		cv.CornerHarris(image,mapaDeEsquinas,3)
		
		#Declaramos un vector que almacenara las coordenadas de las esquinas
		mapaDeCoordenadasEsquinas = []

		#Recorremos en forma "Despliega"
		for x in range(0, image.height): #alto
			for y in range(0, image.width): #ancho				
				#Recorremos en forma "Despliega"
				harris = cv.Get2D(mapaDeEsquinas, x, y) # Pedimos los valores X e Y 			
				#Verificamos si el punto en la posicion x e y son esquina dependiendo del umbral hessiano
				if harris[0] > umbralHessiano:
					#Si son mayor al umbral hessiano, entonces dibujamos un circulo al rededor 
					#del punto que es una esquina en la imagen a color original.
					cv.Circle(imcolor,(y,x),3,cv.RGB(155, 0, 25))#<---Pintamos los circulos en formato "Despliega"										
					#Guardamos en una lista cada una de las coordenadas donde los puntos son esquina					
					#Las guardamos en formato "GuardaYAccede"
					mapaDeCoordenadasEsquinas.extend([[harris[0],x,y]])
			
		#Devolvemos como parametros una arreglo matricial tipo numpyArray
		#en la cual estan contenidos la imagen con circulos dibujados donde
		#estan las esquinas, y un vector en donde se encuentran las coordenadas
		#donde estan las esquinas.
		mapaDeCoordenadasEsquinas = np.array(mapaDeCoordenadasEsquinas, dtype=float)
		
		return imcolor, mapaDeCoordenadasEsquinas
