import numpy as np
from PIL import Image
import struct
from bitarray import bitarray, bits2bytes

def crea_guarda_archivo(nombre_archivo,imagen,tabla_codigos,cadena01):
	dim_x = imagen.shape[1]
	dim_y = imagen.shape[0]
	archivo_abierto = False
	n_entradas = len(tabla_codigos.items)

	try:
		archivo = open(nombre_archivo,"w")
		archivo_abierto = True
	except IOError:
		print 'No se pudo crear: '+nombre_archivo+"!"

	if archivo_abierto == True:
		try:
			archivo.write(convierte_a_bytes(dim_x))
			archivo.write(convierte_a_bytes(dim_y))
			archivo.write(convierte_a_bytes(n_entradas))
			archivo.write(chr(tabla_codigos.n))
			for i in tabla_codigos.items:
				bit_array = bitarray(i.codigo,endian='big')
				tam_codigo = len(i.codigo)
				archivo.write(chr(i.simbolo))
				archivo.write(chr(tam_codigo))
				archivo.write(bit_array.tobytes())

			bit_array = bitarray(cadena01,endian='big')
			archivo.write(bit_array.tobytes())

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
			be = convierte_a_int(archivo.read(4))
			bn = ord(archivo.read(1))
			meta_datos.append(bx)
			meta_datos.append(by)

			for i in range(be):
				item = []
				simbolo = ord(archivo.read(1))
				tam_codigo = ord(archivo.read(1))
				bit_array = bitarray(endian='big')
				bit_array.frombytes(archivo.read(bits2bytes(tam_codigo)))
				codigo = bit_array.to01()[:tam_codigo]
				item.append(simbolo)
				item.append(tam_codigo)
				item.append(codigo)
				items.append(item)

			meta_datos.append(items)

			bit_array = bitarray(endian='big')
			bit_array.frombytes(archivo.read())
			cadena01 = bit_array.to01()

			meta_datos.append(cadena01)
			meta_datos.append(bn)

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

