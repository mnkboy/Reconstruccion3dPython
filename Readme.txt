%///Copyrightº Aviso Legal. Todos los derechos reservados.
%///Algoritmo de reconstruccion 3D hecho por y para fans. 
%///Distribuir bajo licencia GNU, para fines didacticos.
%///Detener su distribucion si se licencia en tu pais.
%///M.C.C. Javier Armando Jimenez Villafaña
%///20-06-2017
%///Universidad Autonoma de Yucatan
%///Programa de Maestria en Ciencias de la Computacion Generacion 2013-2015
%///Descripcion:
%///Este programa se encarga de encontrar correspondencias entre
%///un par de imagenes estereo, para posteriormente generar una 
%///nube de puntos que permita recrear una capa tridimensional

Algoritmo ejecutado en 
OS: Ubuntu 16.04
OpenCV 2.4.9
Python 2.7

Bibliotecas Adicionales:
NumPy(http://www.numpy.org/)
ScyPy(https://www.scipy.org/)
MatPlotLib(https://matplotlib.org/)

Requerimientos:
OpenCV 2.4.9 (Leer Tutorial) -> http://www.samontab.com/web/2014/06/installing-opencv-2-4-9-in-ubuntu-14-04-lts/ (Ultimo Acceso 20-06-2017)
Python 2.7

============ PARTE 1 ============ 
Instrucciones (Algoritmo Parte 1 Busqueda De Correspondencias Homograficas)
1.-Ejecutar el archivo main.py (Clase principal encargada de buscar las correspondencias)
2.-El archivo Generara 2 archivos .CSV (vectorPuntos1.csv y vectorPuntos2.csv)
3.-Adicionalmente generara 3 archivos de imagenes
	3.1.-harris_sad_11_11imagenHarris.jpg (Imagen sobresaturada de todas las posibles correspondencias encontradas)
	3.2.-harris_sad_11_11_Uno.jpg (Imagen con las esquinas o puntos d interes iniciales)
	3.3.-harris_sad_11_11_Dos.jpg (Imagen con las correspondencias de la imagen uno ubicadas en la imagen dos)
4.-Copiar los archivos .csv dentro de la carpeta Calculo de Matrices Para Reconstruccion Tridimensional (Parte 2)

============ PARTE 2 ============ 
Instrucciones Calculo de Matrices Para Reconstruccion Tridimensional (Parte 2)
1.- Ejecutar el archivo mainReconstruccion.py (Clase principal encargada de encontrar las matrices
		que se requieren para realizar una nube de puntos en 3 dimensiones)
2.-La ejecucion del programa generara 2 archivos .csv (nubeDePuntos3DPositiva.csv y nubeDePuntos3DNegativa.csv)
3.- Finalmente todas las nubes de puntos se almacenaran en el directorio NubesDePuntos
4.-Estas se pueden plotear en el programa MatLab utilizando el script Plot3DNubeDePuntos.m incluido en el directorio previamente citado

En el archivo ReporteReconstruccionTridimensional.pdf
se explica brevemente el sentido de este programa
y todos los pasos que conlleva realizar una reconstruccion tridimensional
a partir de 2 imagenes.
