import numpy as np
from PIL import Image
import struct

class item_tl():
	simbolo = None
	probabilidad = 0.0
	lim_inf = None
	lim_sup = None

	def __init__(self,s,p,li,ls):
		self.simbolo = s
		self.probabilidad = p
		self.lim_inf = li
		self.lim_sup = ls

def crea_guarda_archivo(nombre_archivo,imagen,tab_lim,numeros,tam_fragmento):
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
			archivo.write(chr(tam_fragmento))
			archivo.write(chr(len(tab_lim.items)-1))
			for item in tab_lim.items:
				archivo.write(chr(item.simbolo))
				archivo.write(convierte_a_bytes(item.lim_inf))
				archivo.write(convierte_a_bytes(item.lim_sup))

			archivo.write(convierte_a_bytes(float(len(numeros))))
			for n in numeros:
				archivo.write(convierte_a_bytes(n))

			archivo.seek(0)
			archivo.close()
		except:
			print "Error al escribir en "+nombre_archivo

	return archivo_abierto

def abre_archivo(nombre_archivo):
	meta_datos = []
	items = []
	numeros = []
	try:
		archivo = open(nombre_archivo,"rb")
		archivo_abierto = True
	except IOError:
		print 'No se pudo abrir: '+nombre_archivo+"!"

	if archivo_abierto == True:
		try:
			bx = convierte_a_float(archivo.read(4))
			by = convierte_a_float(archivo.read(4))
			tam_f = ord(archivo.read(1))
			n_items = ord(archivo.read(1))+1

			for i in range(n_items):
				simbolo = ord(archivo.read(1))
				linf = convierte_a_float(archivo.read(4))
				lsup = convierte_a_float(archivo.read(4))
				items.append(item_tl(simbolo,0.0,linf,lsup))

			n_numeros = convierte_a_float(archivo.read(4))

			for i in range(int(n_numeros)):
				numeros.append(convierte_a_float(archivo.read(4)))

			meta_datos.append(bx)
			meta_datos.append(by)
			meta_datos.append(tam_f)
			meta_datos.append(items)
			meta_datos.append(numeros)

			archivo.seek(0)
			archivo.close()
		except:
			print "Error al leer "+nombre_archivo

	return meta_datos

def convierte_a_float(bytes):
	tupla = struct.unpack('f',bytes)
	return (tupla[0])

def convierte_a_bytes(flotante):
	return (struct.pack('f',flotante))
