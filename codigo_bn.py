import numpy as np
from PIL import Image
import Lmedia
import arch_cbn as acbn
from bitarray import bits2bytes

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
	n = None

	def __init__(self,histograma,n):
		self.items = []
		self.n = n
		simbolo = 0

		for probabilidad in histograma:
			if probabilidad != 0:
				self.items.append(item(simbolo,probabilidad))
			simbolo += 1

		self.items.sort()

	def asigna_codigo(self):
		cont_cod = 0
		rep = 1
		nbits = self.n*rep
		lim = (2**nbits)-1
		for i in self.items:
			if cont_cod > lim:
				rep += 1
				nbits = self.n*rep
				lim = (2**nbits)-1
				cont_cod = 0

			i.codigo = genera_cadena01(cont_cod,nbits)
			cont_cod += 1

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
	C = 0

	for x in range(dim_x):
		for y in range(dim_y):
			cadena01 += inserta_C(tabla_codigos.busca_codigo_de(img_array[x,y]),C,tabla_codigos.n)
			if C == 0:
				C = 1
			else:
				C = 0

	return cadena01

def inserta_C(codigo,C,n):
	partes = []
	rep = len(codigo)/n
	pos = 0
	for i in range(rep):
		p = codigo[pos:pos+n]
		partes.append(p)
		pos = pos+n

	codigo = ""
	for p in partes:
		codigo += str(C)+p

	return codigo

def decodificar_img(dim_x,dim_y,tabla_codigos,cadena01,n):
	simbolos = []
	pos = 0
	n_elem = (dim_x*dim_y)
	C = 0
	tam = n+1
	max_tam = tabla_codigos[len(tabla_codigos)-1][1]

	for i in range(n_elem):
		if i != (n_elem-1):
			codigo = ""
			parte = cadena01[pos:pos+tam]
			while parte[0] == str(C):
				codigo += parte[1:]
				pos = pos + tam
				parte = cadena01[pos:pos+tam]

			if C == 0:
				C = 1
			else:
				C = 0

			simbolos.append(busca_simbolo_de_codigo(tabla_codigos,codigo))
		else:
			simbolos.append(tabla_codigos[len(tabla_codigos)/2][0])

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
img = Image.open("../f2_lenna.jpg")
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

print "\n N? :"
n = raw_input()

print "\n",img_np,"\n"
print "\nHistograma : ",h

tc = tabla_base(h,int(n))
tc.asigna_codigo()
imprime(tc.items)

dim = img_np.shape[0]*img_np.shape[1]
lm = Lmedia.calcula_L_media(tc.items,dim)
print "\nLMEDIA :",str(lm),"\n"
cadena01 = codificar_img(tc,img_np)
#print "Imagen codificada : ",cadena01

nom_arch = "arch_codigobn"
if acbn.crea_guarda_archivo(nom_arch,img_np,tc,cadena01):
	print "Archivo creado!, Leyendo..."
	md = acbn.abre_archivo(nom_arch)
	valores = decodificar_img(md[0],md[1],md[2],md[3],md[4])
	matriz = recupera_matriz(md[0],md[1],valores)
	Image.fromarray(np.asarray(matriz)).show()
'''
