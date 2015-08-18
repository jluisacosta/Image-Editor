import numpy as np
from PIL import Image
import arch_ca as aca

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

	def __cmp__(self, otro) :
		if self.probabilidad > otro.probabilidad:
			resultado = -1
		elif self.probabilidad < otro.probabilidad:
			resultado = 1
		else :
			resultado = 0

		return resultado

class item_cod():
	simbolo = None
	iinf = None
	isup = None

	def __init__(self,s,iinf,isup):
		self.simbolo = s
		self.iinf = iinf
		self.isup = isup

	def __cmp__(self, otro) :
		if self.probabilidad > otro.probabilidad:
			resultado = -1
		elif self.probabilidad < otro.probabilidad:
			resultado = 1
		else :
			resultado = 0

		return resultado

class tabla_limites():
	items = None

	def __init__(self,histograma,n):
		self.items = []
		simbolo = 0

		for probabilidad in histograma:
			if probabilidad != 0:
				self.items.append(item_tl(simbolo,float(probabilidad/n),0,0))
			simbolo += 1

		self.items.sort()
		self.items[0].lim_inf = 0
		self.items[0].lim_sup = self.items[0].probabilidad

		for i in range(len(self.items)-1):
			ant = self.items[i]
			item = self.items[i+1]
			item.lim_inf = ant.lim_sup
			item.lim_sup = item.lim_inf + item.probabilidad

	def dame_item(self,simbolo):
		item_buscado = None
		for item in self.items:
			if item.simbolo == simbolo:
				item_buscado = item
				break
		return item_buscado

	def imprimete(self):
		if len(self.items)!=0:
			print "\n  Simbolo   Probab    Lim_inf    Lim_sup\n------------------------------------------"
			for it in self.items:
				print "  ",it.simbolo,"     ",it.probabilidad,"     ",it.lim_inf,"    ",it.lim_sup
		else:
			print "tabla esta vacia!"

	def prueba(self):
		iisups = []
		band = False
		for i in self.items:
			iisups.append(i.lim_sup)

		for iisup in iisups:
			c = iisups.count(iisup)
			if c > 1:
				band = True
				break

		if band == True:
			print "SI HAY REPETIDOS!!!"
		else:
			print "No hay repetidos!!"

class tabla_codificacion():
	items = None
	promedio = None

	def __init__(self,tab_lim,fragmento):
		self.items = []
		self.promedio = 0.0
		iinf = 0.0
		isup = 1.0

		self.items.append(item_cod(-1,iinf,isup))

		for simbolo in fragmento:
			itemtl = tab_lim.dame_item(simbolo)
			ant = self.items[-1]
			longi = float(ant.isup-ant.iinf)
			iinf = float(ant.iinf+((longi)*itemtl.lim_inf))
			isup = float(ant.iinf+((longi)*itemtl.lim_sup))
			self.items.append(item_cod(simbolo,iinf,isup))

		self.promedio = float((self.items[-1].iinf+self.items[-1].isup)/2)

	def imprimete(self):
		if len(self.items)!=0:
			print "\n  Simbolo   i inf    i sup\n------------------------------------"
			for it in self.items:
				print "  ",it.simbolo,"     ",it.iinf,"     ",it.isup
		else:
			print "tabla esta vacia!"

def codifica_img(tab_lim,img_flatten,tam_fragmento):
	numeros = []
	pos = 0
	fragmento = img_flatten[pos:pos+tam_fragmento]
	while len(fragmento) > 0:
		t = tabla_codificacion(tab_lim,fragmento)
		numeros.append(t.promedio)
		pos = pos + tam_fragmento
		fragmento = img_flatten[pos:pos+tam_fragmento]

	return numeros

def decodificacion(dim_x,dim_y,tam_fragmento,tab_lim,numeros):
	n_elementos = int(dim_x*dim_y)
	cont = 0
	img = []

	for codigo in numeros:
		for i in range(tam_fragmento):
			if cont < n_elementos:
				item = dame_item_de(tab_lim,codigo)
				img.append(item.simbolo)
				codigo = float((codigo-item.lim_inf)/(item.lim_sup-item.lim_inf))
				cont += 1
			else:
				break

	matriz = np.asarray(img).reshape(dim_y,dim_x)
	return matriz

def dame_item_de(tab_lim,codigo):
	it = None
	for item in tab_lim:
		if item.lim_inf<=codigo and codigo<=item.lim_sup:
			it = item
			break
	return it


'''Codigo prueba'''
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

h = [6,7,4,2,7,2,4,2,4,1,4,4,3,5,4,5]

tam_fragmento = 5
img_array = np.asarray(img)
#print img_array
img_f = img_array.flatten()
tablalim = tabla_limites(h,float(len(img_f)))
#tablalim.imprimete()
nums = codifica_img(tablalim,img_f,tam_fragmento)

nom_arch = "archivo_ca"
if aca.crea_guarda_archivo(nom_arch,img_array,tablalim,nums,tam_fragmento):
	print "Archivo creado!, Leyendo...\n"
	md = aca.abre_archivo(nom_arch)
	matriz = decodificacion(md[0],md[1],md[2],md[3],md[4])
	Image.fromarray(matriz.astype(np.uint8)).show()
'''








