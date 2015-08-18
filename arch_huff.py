import numpy as np
from PIL import Image
import struct
from bitarray import bitarray, bits2bytes
import huffman
import Lmedia

def crea_guarda_archivo_huffman(nombre_archivo,imagen,tabla_codigos,cadena01):
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

def abre_huffman(nombre_archivo):
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
			meta_datos.append(bx)
			meta_datos.append(by)
			#print "X: ",bx," Y: ",by," Entradas: ",be,"\n"
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
				#print simbolo," ",tam_codigo," ",codigo

			meta_datos.append(items)

			bit_array = bitarray(endian='big')
			bit_array.frombytes(archivo.read())
			cadena01 = bit_array.to01()

			meta_datos.append(cadena01)

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

'''Codigo de prueba'''
'''
img = [[10,1,8,15,11,4,13,12],
	   [6,1,1,2,2,13,4,10],
	   [5,8,4,3,11,14,4,3],
	   [15,14,11,4,9,0,14,1],
	   [1,2,13,10,15,12,2,0],
	   [6,1,6,7,14,8,0,4],
	   [10,0,13,15,7,1,0,0],
	   [11,4,5,13,12,8,15,6]]

h = [6,7,4,2,7,2,4,2,4,1,4,4,3,5,4,5]


img = Image.open("../cameraman.jpg")
h = img.histogram()

img_np = np.asarray(img)

nom_arch = "arch_huffman"
tabla_codigos = huffman.genera_tabla_codigos(h)
lm = Lmedia.calcula_L_media(tabla_codigos.items,(img_np.shape[0]*img_np.shape[1]))
print "\nLmedia : ",lm
#huffman.imprime(tabla_codigos.items)
cadena01 = huffman.codificar_img(tabla_codigos,img_np)

if crea_guarda_archivo_huffman(nom_arch,img_np,tabla_codigos,cadena01):
	print "Archivo creado!, Leyendo..."
	md = abre_huffman(nom_arch)
	valores = huffman.decodificar_img(md[0],md[1],md[2],md[3])
	matriz = huffman.recupera_matriz(md[0],md[1],valores)
	Image.fromarray(np.asarray(matriz)).show()

'''






