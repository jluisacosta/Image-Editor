import numpy as np
from PIL import Image
from bitarray import bitarray

def igs(img,n):
	dim_x = img.shape[0]
	dim_y = img.shape[1]
	suma = 0
	resultado = np.zeros([dim_x,dim_y],dtype=np.uint8)
	mascara = ((2**n)-1)<<(8-n)
	mb = bin(mascara)

	for x in range(dim_x):
		for y in range(dim_y):
			valor = img[x,y]
			if valor >= mascara: #si los bits mas significativos son unos
				suma = valor
			else:
				suma = valor + (suma&((2**n)-1))
			resultado[x,y] = (suma&mascara)>>(8-n)

	return resultado


def normaliza_a(L,n,r):
	raux = r/float((2**n)-1)
	normalizada = (raux*(L-1)).astype(np.uint8)
	return normalizada

def genera_cadena01(entero,n):
	rep_bin = bin(int(entero))[2:]
	tam = len(rep_bin)
	if tam < n:
		n_ceros = n - tam
		for i in range(n_ceros):
			rep_bin = "0"+rep_bin

	return rep_bin

def genera_cadena01_matriz(r,n):
	cad =""
	dim_x = r.shape[0]
	dim_y = r.shape[1]

	for x in range(dim_x):
		for y in range(dim_y):
			cad += genera_cadena01(r[x,y],n)

	#print (dim_x*dim_y*n), len(cad)
	bit_array = bitarray(cad,endian='big')

	return (bit_array.tobytes())

def recupera_bytes(cadena_bytes,n):
	list_ba = []
	bit_array = bitarray(endian='big')
	bit_array.frombytes(cadena_bytes)
	cadena01 = bit_array.to01()
	num_elem = (len(cadena01)/n)
	n_ceros = 8-n

	for i in range(num_elem):
		sub_ba = bit_array[(n*i):(n*i)+n]

		for j in range(n_ceros):
			sub_ba.insert(0,False)

		list_ba.append(sub_ba.tobytes())

	return list_ba

def transforma_bytesavalores(lista_bytes):
	valores = []
	for byte in lista_bytes:
		valor = ord(str(byte))
		valores.append(valor)

	return valores

def recupera_matriz(dim_x,dim_y,valores):
	matriz = np.zeros([dim_y,dim_x],dtype=np.uint8)
	i = 0
	for y in range(dim_y):
		for x in range(dim_x):
			matriz[y,x] =  valores[i]
			i+=1

	return matriz
