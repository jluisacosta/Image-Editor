import numpy as np
from PIL import Image
import Lmedia
import arch_hufft4 as ah

class item():
	simbolo = None
	probabilidad = 0.0
	codigo = None

	def __init__(self,sim,prob):
		self.simbolo = sim
		self.probabilidad = prob
		self.codigo = ""

	def __cmp__(self, otro) :
		if self.probabilidad > otro.probabilidad:
			resultado = -1
		elif self.probabilidad < otro.probabilidad:
			resultado = 1
		else :
			resultado = 0

		return resultado

class tabla_base():
	items = None
	nbloques = None

	def __init__(self,histograma,nbloques):
		self.items = []
		self.nbloques = nbloques
		simbolo = 0

		for probabilidad in histograma:
			if probabilidad != 0:
				self.items.append(item(simbolo,probabilidad))
			simbolo += 1

		self.items.sort()

	def asigna_codigo(self):
		if self.nbloques == (2**2):
			self.nbloques += 1
		if len(self.items)%self.nbloques != 0:
			nElementos = (len(self.items)/self.nbloques)+1
		else:
			nElementos = (len(self.items)/self.nbloques)

		#print "nElementos:",nElementos
		
		nbp = len(bin(nElementos-1)[2:])
		for i in range(nElementos):
			self.items[i].codigo = genera_cadena01(i,nbp)

		nb = len(bin(nElementos)[2:])
		cont_cod = 0
		cont_prefijo = 1
		for i in range(len(self.items)-nElementos):
			if cont_cod == nElementos:
				cont_cod = 0
				cont_prefijo += 1

			self.items[nElementos+i].codigo = self.genera_codigo(nbp,nElementos,cont_prefijo,nb,cont_cod)
			cont_cod += 1

	def genera_codigo(self,nbp,prefijo,cont_prefijo,nb,cont_cod):
		codigo = ""
		for i in range(cont_prefijo):
			codigo += genera_cadena01(prefijo,nbp)

		codigo += genera_cadena01(cont_cod,nb)
		return codigo

	def busca_codigo_de(self,simbolo):
		cod = ""
		for i in self.items:
			if i.simbolo == simbolo:
				cod = i.codigo
				break
		return cod


def imprime(tabla):
	if len(tabla)!=0:
		print "\nSimbolo   Probab    Codigo\n------------------------------------"
		for it in tabla:
			print "  ",it.simbolo,"       ",it.probabilidad,"     ",it.codigo
	else:
		print "tabla esta vacia!"


def genera_cadena01(entero,n):
	rep_bin = bin(int(entero))[2:]
	tam = len(rep_bin)
	if tam < n:
		n_ceros = n - tam
		for i in range(n_ceros):
			rep_bin = "0"+rep_bin

	return rep_bin

def codificar_img(tabla_codigos,img_array):
	dim_x = img_array.shape[0]
	dim_y = img_array.shape[1]
	cadena01 = ""

	for x in range(dim_x):
		for y in range(dim_y):
			cadena01 += tabla_codigos.busca_codigo_de(img_array[x,y])

	return cadena01

def decodificar_img(dim_x,dim_y,tabla_codigos,cadena01):
	simbolos = []
	tamanos = []
	pos = 0
	n_elem = (dim_x*dim_y)

	for item in tabla_codigos:
		if item[1] not in tamanos:
			tamanos.append(item[1])

	for i in range(n_elem):
		simbolo = -1
		tam = tabla_codigos[(len(tabla_codigos)-1)][1]
		while(simbolo < 0):
			if tam in tamanos:
				codigo = cadena01[pos:pos+tam]
				simbolo = busca_simbolo_de_codigo(tabla_codigos,codigo)
			tam -= 1
		simbolos.append(simbolo)
		pos += tam+1
	#print simbolos
	return simbolos


def busca_simbolo_de_codigo(tabla_codigos,codigo):
	simbolo = -1
	for i in tabla_codigos:
		if codigo == i[2]:
			simbolo = i[0]
			break

	return simbolo


def recupera_matriz(dim_x,dim_y,valores):
	matriz = np.zeros([dim_y,dim_x],dtype=np.uint8)
	i = 0
	for y in range(dim_y):
		for x in range(dim_x):
			matriz[y,x] =  valores[i]
			i+=1

	return matriz

'''Codigo Prueba'''
'''
img = Image.open("../cameraman.jpg")
h = img.histogram()

img = [[10,1,8,15,11,4,13,12],
	   [6,1,1,2,2,13,4,10],
	   [5,8,4,3,11,14,4,3],
	   [15,14,11,4,9,0,14,1],
	   [1,2,13,10,15,12,2,0],
	   [6,1,6,7,14,8,0,4],
	   [10,0,13,15,7,1,0,0],
	   [11,4,5,13,12,8,15,6]]

img_np = np.asarray(img)

#h = [6,7,4,2,7,2,4,2,4,1,4,4,3,5,4,5]
#h = [20,10,10,6,5,5,5,4,4,4,4,3,3,3,3,2,2,2,2,2,1]

print "\nn Bloques? :"
nbl = raw_input()

print "\n",img_np,"\n"
print "\nHistograma : ",h
tc = tabla_base(h,int(nbl))
tc.asigna_codigo()
imprime(tc.items)

dim = img_np.shape[0]*img_np.shape[1]
lm = Lmedia.calcula_L_media(tc.items,dim)
print "\nLMEDIA :",str(lm),"\n"

nom_arch = "arch_huff_binaryshift"
cadena01 = codificar_img(tc,img_np)
#print "Imagen codificada : ",cadena01

if ah.crea_guarda_archivo(nom_arch,img_np,tc,cadena01):
	print "Archivo creado!, Leyendo..."
	md = ah.abre_archivo(nom_arch)
	valores = decodificar_img(md[0],md[1],md[2],md[3])
	matriz = recupera_matriz(md[0],md[1],valores)
	Image.fromarray(np.asarray(matriz)).show()
'''




