import numpy as np
from PIL import Image
import struct
from bitarray import bitarray, bits2bytes

class item():
	inicial = None
	tam = None
	conteo = None

	def __init__(self,ini,tam,contp):
		self.inicial = ini
		self.tam = tam
		self.conteo = contp

def crea_guarda_archivo(nombre_archivo,imagen,items):
	dim_x = imagen.shape[1]
	dim_y = imagen.shape[0]
	archivo_abierto = False

	try:
		archivo = open(nombre_archivo,"w")
		archivo_abierto = True
	except IOError:
		print 'No se pudo crear: '+nombre_archivo+"!"

	if archivo_abierto == True:
		try:
			archivo.write(convierte_a_bytes(dim_x))
			archivo.write(convierte_a_bytes(dim_y))
			for item in items:
				archivo.write(chr(item.inicial))
				archivo.write(convierte_a_bytes(item.tam))
				for i in range(item.tam):
					archivo.write(convierte_a_bytes(item.conteo[i]))

			archivo.seek(0)
			archivo.close()
		except:
			print "Error al escribir en "+nombre_archivo

	return archivo_abierto 

def abre_archivo(nombre_archivo):
	meta_datos = []
	items = []
	try:
		archivo = open(nombre_archivo,"rb")
		archivo_abierto = True
	except IOError:
		print 'No se pudo abrir: '+nombre_archivo+"!"

	if archivo_abierto == True:
		try:
			bx = convierte_a_int(archivo.read(4))
			by = convierte_a_int(archivo.read(4))
			for i in range(8):
				ini = ord(archivo.read(1))
				tam = convierte_a_int(archivo.read(4))
				contp = []
				for i in range(tam):
					contp.append(convierte_a_int(archivo.read(4)))
				items.append(item(ini,tam,contp))

			meta_datos.append(bx)
			meta_datos.append(by)
			meta_datos.append(items)

			archivo.seek(0)
			archivo.close()
		except:
			print "Error al leer "+nombre_archivo

	return meta_datos

def convierte_a_int(bytes):
	tupla = struct.unpack('i',bytes)
	return (tupla[0])

def convierte_a_bytes(entero):
	return (struct.pack('i',entero))

