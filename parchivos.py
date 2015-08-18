import numpy as np
from PIL import Image
import struct
from bitarray import bitarray
import igs

def crea_guarda_archivo_igs(nombre_archivo,imagen,n_profundidad):
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
			archivo.write(convierte_a_bytes(n_profundidad))

			archivo.write(igs.genera_cadena01_matriz(imagen,n_profundidad))
			archivo.seek(0)
			archivo.close()
		except:
			print "Error al escribir en "+nombre_archivo

	return archivo_abierto

def abre_igs(nombre_archivo):
	meta_datos = []
	xyn = []
	cadena01 = None

	try:
		archivo = open(nombre_archivo,"rb")
		archivo_abierto = True
	except IOError:
		print 'No se pudo abrir: '+nombre_archivo+"!"

	if archivo_abierto == True:
		try:
			bx = archivo.read(4)
			by = archivo.read(4)
			bn = archivo.read(4)
			xyn.append(convierte_a_int(bx))
			xyn.append(convierte_a_int(by))
			xyn.append(convierte_a_int(bn))
			tam_cad = (xyn[0]*xyn[1]*xyn[2])
			cadena_bytes = archivo.read(tam_cad)
			archivo.seek(0)
			archivo.close()
		except:
			print "Error al leer "+nombre_archivo

	if not len(xyn)==0 and cadena_bytes != None:
		meta_datos.append(xyn)
		meta_datos.append(cadena_bytes)

	return meta_datos


def convierte_a_int(bytes):
	tupla = struct.unpack('i',bytes)
	return (tupla[0])

def convierte_a_bytes(entero):
	return (struct.pack('i',entero))


'''Codigo de prueba'''
'''
img = Image.open("../cameraman.jpg")
n_prueba = 4

img_x = igs.igs(np.asarray(img),n_prueba)
print "Matriz generada por IGS: \n",img_x

if crea_guarda_archivo_igs("nuevo_archivo",img_x,n_prueba):
	print "Archivo creado!"

	md = abre_igs("nuevo_archivo")
	print "Archivo leido!, recuperando bytes..."

	lista_bytes = igs.recupera_bytes(md[1],md[0][2])
	print "Bytes recuperados, transformando a valores originales..."

	valores = igs.transforma_bytesavalores(lista_bytes)
	print "Valores transformados, construyendo matriz leida..."

	m = igs.recupera_matriz(md[0][0],md[0][1],valores)
	print "Matriz leida de archivo: \n",m

	r_normalizada = igs.normaliza_a(256,n_prueba,m)
	img_norm = Image.fromarray(r_normalizada)
	img_norm.show()
	img.show()
'''

