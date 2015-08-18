
def calcula_L_media(tabla,dimension):
	sumatoria = 0.0
	for item in tabla:
		sumatoria += (float(item.probabilidad)/float(dimension))*len(item.codigo)
	return sumatoria