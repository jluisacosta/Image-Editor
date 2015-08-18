import numpy as np
from PIL import Image

class item():
	x = None
	simbolo = None
	probabilidad = 0.0
	codigo = None

	def __init__(self,es_x,sim,prob):
		self.x = es_x
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
	orden_simbolos = None
	lista_tablas = None

	def __init__(self,histograma):
		self.items = []
		self.lista_tablas = []
		self.orden_simbolos = []
		simbolo = 0

		for probabilidad in histograma:
			if probabilidad != 0:
				self.items.append(item(False,simbolo,probabilidad))
			simbolo += 1

		self.items.sort()

	def generar_siguiente(self,tabla_padre,ntab):
		nueva = tabla_padre[:]
		ultimo_item = nueva.pop()
		penultimo_item = nueva.pop()
		nueva.append(item(True,ntab,(ultimo_item.probabilidad+penultimo_item.probabilidad)))
		nueva.sort()
		return nueva

	def selecciona_nuevo(self,tabla_hija):
		xnueva = 0
		item = None
		for i in tabla_hija:
			if i.x == True and i.simbolo > xnueva:
				xnueva = i.simbolo
				item = i

		return item

	def genera_codigo(self,tabla_padre,tabla_hija):
		item = self.selecciona_nuevo(tabla_hija)
		tabla_padre[-2].codigo = item.codigo + "0"
		tabla_padre[-1].codigo = item.codigo + "1"

	def asigna_codigo(self,tabla):
		tabla.lista_tablas[-1][-2].codigo = "0"
		tabla.lista_tablas[-1][-1].codigo = "1"
		ntablas = len(tabla.lista_tablas)
		#print "ntablas: ",ntablas
		for i in range(ntablas):
			if i == (ntablas-1):
				self.genera_codigo(tabla.items,tabla.lista_tablas[0])
			else:
				# print (-(i+2)),(-(i+1))
				self.genera_codigo(tabla.lista_tablas[-(i+2)],tabla.lista_tablas[-(i+1)])

		for i in tabla.items:
			tabla.orden_simbolos.append(i.simbolo)

	def busca_codigo_de(self,simbolo):
		return (self.items[self.orden_simbolos.index(simbolo)].codigo)

	def busca_codigo_de2(self,simbolo):
		cod = ""
		for i in self.items:
			if i.simbolo == simbolo:
				cod = i.codigo
				break
		return cod



def imprime(tabla):
	if len(tabla)!=0:
		print "\n  X    Simbolo   Probab    Codigo\n------------------------------------"
		for it in tabla:
			print it.x,"   ",it.simbolo,"    ",it.probabilidad,"   ",it.codigo
	else:
		print "tabla esta vacia!"

def genera_tabla_codigos(histograma):
	t = tabla_base(histograma)
	ntabs = (len(t.items)-2)
	tn = t.generar_siguiente(t.items,1)

	for i in range(ntabs):
		t.lista_tablas.append(tn)
		tn = t.generar_siguiente(tn,i+2)

	t.asigna_codigo(t)
	return t

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
	pos = 0
	n_elem = (dim_x*dim_y)
	for i in range(n_elem):
		simbolo = -1
		tam = tabla_codigos[0][1]
		while(simbolo < 0):
			codigo = cadena01[pos:pos+tam]
			simbolo = busca_simbolo_de_codigo(tabla_codigos,codigo)
			tam += 1
		simbolos.append(simbolo)
		pos += tam-1
	#print simbolos
	return simbolos


def busca_simbolo_de_codigo(tabla_codigos,codigo):
	simbolo = -1
	for i in tabla_codigos:
		if i[1] == len(codigo) and codigo == i[2]:
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


'''
img = Image.open("cameraman.jpg")
h = img.histogram()

img = [[10,1,8,15,11,4,13,12],
	   [6,1,1,2,2,13,4,10],
	   [5,8,4,3,11,14,4,3],
	   [15,14,11,4,9,0,14,1],
	   [1,2,13,10,15,12,2,0],
	   [6,1,6,7,14,8,0,4],
	   [10,0,13,15,7,1,0,0],
	   [11,4,5,13,12,8,15,6]]

h = [6,7,4,2,7,2,4,2,4,1,4,4,3,5,4,5]

img_np = np.asarray(img)
tc = genera_tabla_codigos(h)
cad = codificar_img(tc,img_np)
print img_np
imprime(tc.items)
print cad
'''