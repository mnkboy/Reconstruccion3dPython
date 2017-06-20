#Esta clase se encargara de realizar el manejo de archivos para guardar y/o exportar nuestra nube de puntos
#Esta clase recibe como parametros:
#1.- Un directorio
#2.- Un nombre de archivo
#3.- Una fecha de creacion
#4.- El contenido del archivo
#5.- Un modo de apertura

class ManejadorDeArchivos:	
	
	def manejaArchivo(self, directorio, nombreArchivo, fechaDeCreacion, contenidoDelArchivo, modoDeApertura ):
		#Ubicamos la ruta del archivo
		rutaCompleta = directorio + "/" + nombreArchivo + "_" + str(fechaDeCreacion) + ".txt"
		
		# Abrimos el archivo nombreArchivo.txt
		fo = open(rutaCompleta, modoDeApertura)
		print("Manejador de archivos")
		for i in range(len(contenidoDelArchivo)):
			#print(contenidoDelArchivo[i])		
			#Escribimos el archivo
			concatenada = " "+str(contenidoDelArchivo[i]).strip( '[' ']' );
			fo.write(concatenada+"\n");
		
		print( "Nombre del archivo : ", fo.name)
		print( "Cerrado o no : ", fo.closed)
		print( "Modo de apertura : ", fo.mode)
		
		# Cerramos el archivo nombreArchivo.txt
		fo.close()
