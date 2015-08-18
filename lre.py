import numpy as np
from PIL import Image
import arch_lre as al
from bitarray import bitarray

class item():
	inicial = None
	tam = None
	conteo = None

	def __init__(self,ini,tam,contp):
		self.inicial = ini
		self.tam = tam
		self.conteo = contp

def dame_planos(img_array):
	planos = []
	for i in range(8):
		plano = img_array
		plano = plano & pow(2,i)
		plano = plano >> i
		planos.append(plano.flatten())

	planos.reverse()
	return planos

def genera_conteo_de(plano):
	contadores = []
	valor = plano[0]
	cont = 0
	for i in plano:
		if i == valor:
			cont += 1
		else:
			contadores.append(cont)
			cont = 1
			valor = i

	contadores.append(cont)
	return contadores

def genera_items(planos):
	items = []
	for plano in planos:
		cont = genera_conteo_de(plano)
		tam = len(cont)
		items.append(item(plano[0],tam,cont))

	return items

def transforma_conteo(inicial,conteo):
	lista01 = []
	valor = inicial
	for i in conteo:
		for j in range(i):
			lista01.append(valor)

		if valor == 0:
			valor = 1
		else:
			valor = 0

	return lista01

def decodificacion(dim_x,dim_y,items):
	matrices = []
	for item in items:
		m = transforma_conteo(item.inicial,item.conteo)
		matrices.append(np.asarray(m).reshape(dim_y,dim_x))

	matriz_img = combina_matrices(dim_x,dim_y,matrices)
	return matriz_img

def combina_matrices(dim_x,dim_y,matrices):
	matriz = np.zeros([dim_y,dim_x],dtype=np.uint8)
	for y in range(dim_y):
		for x in range(dim_x):
			cadena01 = ""
			for m in matrices:
				cadena01 += str(m[y,x])
			bit_array = bitarray(cadena01,endian='big')
			matriz[y,x] = ord(str(bit_array.tobytes()))

	return matriz

'''Codigo prueba'''
'''
img = [[10,1,8,15,11,4,13,12],
	   [6,1,1,2,2,13,4,10],
	   [5,8,4,3,11,14,4,3],
	   [15,14,11,4,9,0,14,1],
	   [1,2,13,10,15,12,2,0],
	   [6,1,6,7,14,8,0,4],
	   [10,0,13,15,7,1,0,0],
	   [11,4,5,13,12,8,15,6]]

img_array = np.asarray(img)

img_array = np.asarray(Image.open("../cameraman.jpg"))

planos = dame_planos(img_array)
items = genera_items(planos)

nom_arch = "archivo_lre"
if al.crea_guarda_archivo(nom_arch,img_array,items):
	print "Archivo creado!, Leyendo...\n"
	md = al.abre_archivo(nom_arch)
	matriz_img = decodificacion(md[0],md[1],md[2])
	Image.fromarray(matriz_img).show()
'''







