#En este programa calcularemos las esquinas en una imagen 1, asi como sus correspondencias en una imagen 2
#importamos las bibliotecas que nos serviran para realizar
#la tarea de obtener las esquinas 
import cv2   #Esta biblioteca es la relativa a opencv 2
import cv	  #Esta biblioteca es la relativa a opencv 
import numpy as np #Esta biblioteca es la relativa a calculos matematicos en python
import scipy #Esta biblioteca es la relativa a calculos cientifico matematico en python
import datetime #Esta biblioteca nos permitira obtener el tiempo y la fecha de nuestra computadora 
from matplotlib import pyplot as plt #Esta biblioteca es la relativa a graficacion, un poco mejor que una ventana normal, pero no es la gran cosa

import DetectorDeEsquinasDeHarris #Esta biblioteca es la encargada de realizar la deteccion de esquinas
import CortadorDeMosaicos #Esta clase se encargara de recortar la imagen en mosaicos en los cuales despues ubicaremos las esquinas 
import ReductorDeNumeroDeEsquinas#Esta clase se encargara de filtrar unicamente las coordenadas de los puntos que esten dentro del mosaico actual
import CreadorDeVentanas #Esta biblioteca es la encargada de realizar el calculo y creacion de las ventanas para ubicar los puntos correspondencia

###########En esta seccion declararemos los objetos que necesitaremos para realizar la reconstruccion 3D###########
#creamos un objeto de tipo detector de esquinas
objDetectorDeEsquinasDeHarris = DetectorDeEsquinasDeHarris.DetectorDeEsquinasDeHarris()

#Creamos un objeto de la clase cortador de mosaicos para delimitar las coordenadas inciales y finales de nuestro mosaico actual
objCortadorDeMosaicos = CortadorDeMosaicos.CortadorDeMosaicos();

#Declaramos un objeto de la clase ReductorDeNumeroDeEsquinas para poder reducir el numero de esquinas que existe en un mosaico
objReductorDeNumeroDeEsquinas = ReductorDeNumeroDeEsquinas.ReductorDeNumeroDeEsquinas()

#Creamos un objeto de tipo creador de ventanas para poder utilizar las funciones de creacion de ventanas
objCreadorDeVentanas = CreadorDeVentanas.CreadorDeVentanas()
###################################################################################################################

############### Paso 1.- Leemos imagen Uno e imagen Dos ###############
#Declaramos un par de variables que almacenaran los nombres de las imagenes uno e imagen dos
nombreImagenUno = 'Craneo1.pgm'
nombreImagenDos = 'Craneo2.pgm'

#Leemos la primera imagen imagen que nos servira para calcular las esquinas
imcolorUno = cv.LoadImage(nombreImagenUno)

#Leemos la segunda imagen que nos servira para calcular las esquinas
imcolorDos = cv.LoadImage(nombreImagenDos)
########################################################################



############### Paso 2.- Convertimos la imagen uno e imagen dos a escala de grices ###############
#Convertimos la imagen uno a escala de grices
imagenUno = cv.LoadImage(nombreImagenUno,cv.CV_LOAD_IMAGE_GRAYSCALE)

#Convertimos la imagen dos a escala de grices
imagenDos = cv.LoadImage(nombreImagenDos,cv.CV_LOAD_IMAGE_GRAYSCALE)
##################################################################################################



############### Paso 3.- Calculamos las esquinas de la imagen Uno ###############
#Declaramos un umbral hessiano que determinara que pixel es una esquina, y que pixel no es esquina
umbralHessiano = 0.000000001

#Llamamos a la funcion encargada de realizar la deteccion de esquinas de harris
#El mapa de coordenadas de esquinas devuelve un vector de N renglones x 3 columnas
#Columna 1 = Valor de esquinidad
#Columna 2 = Coordenada X
#Columna 3 = Cordenada Y
#Recibimos una imagen, y un numpyArray
(imagenHarris, mapaDeCoordenadasEsquinas) =	objDetectorDeEsquinasDeHarris.detectaEsquinas(imagenUno,imcolorUno, umbralHessiano)
#(imagenHarrisDos, mapaDeCoordenadasEsquinasDos) = detectorDeEsquinasDeHarris.detectaEsquinas(imagenDos,imcolorDos, umbralHessiano)

print("Este es el alto de la imagen: ", imagenHarris.height)   #Alto
print("Este es el ancho de la imagen: ", imagenHarris.width)    #Ancho

m, n = mapaDeCoordenadasEsquinas.shape
##################################################################################################
								###########REDUCCION DE ESQUINAS##############
#Paso 4.- dividimos la imagen en mosaicos, y guardamos las coordenadas de inicio en X,y Y 
#y las coordenadas de fin en X y Y de cada mosaico

incrementoVerticalX = 48 #Incremento en X formato "GuardaYAccede"
incrementoHorizontalY = 64 #Incremento en Y formato "GuardayAccede"

#Recibimimos un vector que tiene el numero de mosaicos asi como sus coordenadas inciales y finales de cada mosaico
#Tambien recibimos una matriz simulando nuestra matriz hessiana
vectorCoordenadasDeLosMosaicos = objCortadorDeMosaicos.cortaMosaicoDeNxN(imagenUno, incrementoVerticalX, incrementoHorizontalY)

##################################################################################################
#Declaramos una distancia minima en pixeles que habra entre esquina y esquina dentro de nuestro mosaico
criterioDistanciaPixeles = 10

#Declaramos un vector que almacenara un vectorMosaicoActual hasta cubrir el numero de mosaicos totales en el que fue dividido la imagen
vectorPuntosADibujarTotales = []

#Paso 5.- En este paso guardaremos todas las coordenadas que se encuentran dentro de cada mosaico
#Guardamos las coordenadas iniciales y finales de cada mosaico
for i in range(len(vectorCoordenadasDeLosMosaicos)):
	
	coordenadaInicialX = vectorCoordenadasDeLosMosaicos[i,1]
	coordenadaInicialY = vectorCoordenadasDeLosMosaicos[i,2]
	coordenadaFinalX = vectorCoordenadasDeLosMosaicos[i,3]
	coordenadaFinalY = vectorCoordenadasDeLosMosaicos[i,4]
	
	#Guardamos las coordenadas que se encuentran dentro del mosaico actual
	vectorMosaicoActual = objReductorDeNumeroDeEsquinas.ubicaLasCoordenadasDelMosaico(mapaDeCoordenadasEsquinas, coordenadaInicialX, coordenadaInicialY, coordenadaFinalX, coordenadaFinalY)

#Paso 6.- En este paso reduciremos el numero de esquinas por mosaico, limitandolo a un maximo de 5 esquinas
#por mosaico, a un distancia mayor de 10 pixeles entre esquina y esquina	

	#Verificamos que dentro de nuestro mosaico actual exista al menos una esquina para que no se vaya vacio al ciclo de comprobacion
	if len(vectorMosaicoActual)	> 0:
		vectorPuntosADibujar = objReductorDeNumeroDeEsquinas.reduceEsquinas(vectorMosaicoActual, criterioDistanciaPixeles)
		print("Vamos en la ventana numero:", i)
		#Metemos en un vector las coordendas del mosaico actual, uno por cada vuelta.
		for w in range(len(vectorPuntosADibujar)):			
			vectorPuntosADibujarTotales.extend([[vectorPuntosADibujar[w][0], vectorPuntosADibujar[w][1], vectorPuntosADibujar[w][2]]])
		#Imprimimos los puntos que existen dentro del mosaico actual
		print("vectorMosaicoActual")
		print(vectorMosaicoActual)
		print("vectorPuntosADibujar")
		print(vectorPuntosADibujar)
		
#Devolvemos como parametros una arreglo matricial tipo numpyArray
#En el cual estaran todos los puntos que cumplen la regla de los 10 pixeles de distancia
#Y no mas de 5 esquinas en un mosaico
vectorPuntosADibujarTotales = np.array(vectorPuntosADibujarTotales, dtype=float)

print("vectorPuntosADibujarTotales")
print(vectorPuntosADibujarTotales)
##################################################################################################

############### Paso 7.- Declaramos todas las variables que vamos a utilizar en nuestra tarea de reconstruccion 3D ####################
#Declaramos una variable que almacenara el tamano de la ventana
tamanoVentana = 11#Este tamano es el tamano N de la ventana NxN

#Declaramos una variable que almacenara el tamano de la ventana que vamos a recorrer
tamanoRecorrido = 11#Este tamano es el el tamano del recorrido de MxM

#Declaramos una variable que sera el rango dentro del cual se calculara nuestra ventana, es decir valores negativos, cero, valores positivos
rango = tamanoVentana // 2

#Declaramos una matriz que almacenara a nuestra ventana de NxN
matrizNxN = []

#Declaramos un par de vectores que almacenaran los puntos que vayamos a necesitar para calcular la matriz fundamental
vectorPuntos1 = []
vectorPuntos2 = []

vectorPuntosUNO = []
vectorPuntosDOS = []

#Volvemos a cargar nuevamente las imagenes limpias
imcolorPruebaUno = cv.LoadImage(nombreImagenUno)
imcolorPruebaDos = cv.LoadImage(nombreImagenDos)

#Establecemos una variable que almacenara el criterio de correlacion, los criterios pueden ser
#1.- ssd, 2.- ncc, 3.- zncc, 4.- lsad, 5.- zsad
#6.- lssd, 7.- zssd, 8.- sad  <--- buena   
#N.- otros... que se vayan agregando
criterioDeCorrelacion = 'sad'
###############################################################################################################################

############### Paso 8.- Comprobamos que la ventana no se salga de sus limites ###############
#Aca recorremos todas las coordenadas donde se supone hay correspondencias
for i in range(len(vectorPuntosADibujarTotales)):	
	#En esta parte metemos un par de coordenadas X e Y para poder crear una matriz, o realizar un recorrido
	puntoX = int(vectorPuntosADibujarTotales[i,1])#Este punto se mueve verticalmente de arriba hacia abajo, y controla el desplazamiento en filas
	puntoY = int(vectorPuntosADibujarTotales[i,2])#Este punto se mueve horizontalmente de izquierda a derecha, y controla el desplazamiento en columnas	

	#En esta parte verificamos que cada punto X e Y que vayamos a calcular en la ventana no se salga de los limites de la imagen
	if imagenUno.height	 <= puntoX + (tamanoVentana + tamanoRecorrido):
		#print("El valor de la ventana se excede de las dimensiones X osea alto de la imagen")
		continue
	elif imagenUno.width <= puntoY + (tamanoVentana + tamanoRecorrido):
		#print("El valor de la ventana se excede de las dimensiones Y osea ancho de la imagen")
		continue
	elif puntoX - (tamanoVentana + tamanoRecorrido) < 0:
		#print("El valor de la ventana es menor de las dimensiones X osea alto de la imagen")
		continue
	elif puntoY - (tamanoVentana + tamanoRecorrido) < 0:	
		#print("El valor de la ventana es menor de las dimensiones Y osea ancho de la imagen")
		continue
	else:	
############### Paso 9.- Creamos una ventana de NxN para cada coordenada X e Y donde exista una esquina en la imagenUno ###############	
		#Si no se sale de sus limites entonces procedemos a crear su ventana
		(matrizCriterioCorrelacion, vectorValorMinmo) = objCreadorDeVentanas.realizaRecorridoDeLaVentana(puntoX,puntoY,imagenUno, imagenDos, tamanoVentana, tamanoRecorrido, criterioDeCorrelacion)		
		
		#Pintamos los circulos en la imagen 1
		cv.Circle(imcolorPruebaUno,(puntoY,puntoX),3,cv.RGB(155, 0, 25))#<---Pintamos los circulos en formato "Despliega" (Y,X)
		#Pintamos los circulos en la imagen 2
		cv.Circle(imcolorPruebaDos,(vectorValorMinmo[0][2],vectorValorMinmo[0][1]),3,cv.RGB(155, 0, 25))#<---Pintamos los circulos en formato "Despliega" (Y,X)
		#Pintamos una linea en la imagen 2 para observar el corrimiento
		cv.Line(imcolorPruebaDos, (puntoY, puntoX), (vectorValorMinmo[0][2], vectorValorMinmo[0][1]), cv.RGB(25, 25, 112), thickness=1, lineType=8, shift=0)#<---Pintamos las lineas en formato "Despliega" (Y,X)
		
############### Paso 10.- Metemos en un par de vectores los puntos correspondientes para poder calcular la matriz fundamental ###############			
		vectorPuntos1.append([puntoX,puntoY,1]) #---> Agregamos el 1 para normalizar la matriz de "m" filas  x 3 columnas, Guardamos las coordenadas en formato "GuardaYAccede" (X,Y)
		vectorPuntos2.append([vectorValorMinmo[0][1],vectorValorMinmo[0][2],1]) #---> Agregamos el 1 para normalizar la matriz de "m" filas  x 3 columnas,  Guardamos las coordenadas en formato "GuardaYAccede" (X,Y)
		
		vectorPuntosUNO.append([puntoX,puntoY]) #---> Agregamos el 1 para normalizar la matriz de "m" filas  x 3 columnas, Guardamos las coordenadas en formato "GuardaYAccede" (X,Y) 
		vectorPuntosDOS.append([vectorValorMinmo[0][1],vectorValorMinmo[0][2]]) #---> Agregamos el 1 para normalizar la matriz de "m" filas  x 3 columnas, Guardamos las coordenadas en formato "GuardaYAccede" (X,Y)

##############Paso 11.-Convertimos los vectores que son listas a tipo array##############

vectorPuntos1 = np.array(vectorPuntos1, dtype=int)
vectorPuntos2 = np.array(vectorPuntos2, dtype=int)	 

#~ vectorPuntosUNO = np.float32(vectorPuntosUNO)
#~ vectorPuntosDOS = np.float32(vectorPuntosDOS)

#Salvamos la solucion en un archivo .csv
np.savetxt("vectorPuntos1.csv", vectorPuntos1, delimiter=",",  fmt="%u")
np.savetxt("vectorPuntos2.csv", vectorPuntos2, delimiter=",",  fmt="%u")

print("Imprimimos el vector de puntos 1")
for i in range(len(vectorPuntos1)):	
	print(vectorPuntos1[i,:])
print("len(vectorPuntos1)")	
print(len(vectorPuntos1))
#########################################################################################		

############### Paso N.- Mostramos la imagen ###############
#Creamos una ventana que desplegara la imagen con las esquinas halladas en la imagen uno
cv.NamedWindow('Imagen Uno', cv.CV_WINDOW_AUTOSIZE)
#Mostramos la imagen uno
cv.ShowImage('Imagen Uno', imcolorPruebaUno) 
#Creamos una ventana que desplegara la imagen con las esquinas halladas en la imagen uno
cv.NamedWindow('Imagen Dos', cv.CV_WINDOW_AUTOSIZE)
#Mostramos la imagen uno
cv.ShowImage('Imagen Dos', imcolorPruebaDos) 

#Guardamos la imagen con las esquinas halladas en la imagen uno
cv.SaveImage('harris_'+criterioDeCorrelacion+'_'+str(tamanoVentana)+'_'+str(tamanoRecorrido)+'_Uno.jpg', imcolorPruebaUno)
#Guardamos la imagen con las esquinas halladas en la imagen dos
cv.SaveImage('harris_'+criterioDeCorrelacion+'_'+str(tamanoVentana)+'_'+str(tamanoRecorrido)+'_Dos.jpg', imcolorPruebaDos)
#Guardamos la imagen con las esquinas halladas en la imagen dos
cv.SaveImage('harris_'+criterioDeCorrelacion+'_'+str(tamanoVentana)+'_'+str(tamanoRecorrido)+'imagenHarris.jpg', imagenHarris)


#Esperamos a que el usuario presione una tecla
cv.WaitKey()


##################################################################################################



