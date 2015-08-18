import numpy as np
from PIL import Image

def primer_orden(img):
	h = Image.fromarray(img).histogram()
	dim = img.shape[0]*img.shape[1]
	sumatoria = 0.0
	sp = 0.0
	for i in h:
		p = float(float(i)/dim)
		sp+=p
		sumatoria += p*np.log2(p)

	sumatoria = abs(sumatoria)
	#print "\nSuma probabilidad:",sp
	return (sumatoria)

def segundo_orden(img):
	l2 = []
	lp = []
	lt = []

	l = img.flatten()
	n = len(l)
	for i in range(n):
		if (i+1) <= (n-1):
			item = [l[i],l[i+1]]
			if not item in l2:
				l2.append(item)
			lt.append(item)

	l2.append([l[-1],l[0]])
	lt.append([l[-1],l[0]])

	for i in l2:
		lp.append(lt.count(i))

	dim = float(len(lt))
	estimacion = (sumatoria2(lp,dim))/2
	#print "\nEstimacion de 2o orden : ",estimacion/2
	return estimacion

def sumatoria2(lp,dim):
	sumatoria = 0.0
	sp = 0.0
	for i in lp:
		p = float(float(i)/dim)
		sp += p
		sumatoria += p*np.log2(p)

	sumatoria *= -1
	#print "\nSuma probabilidad:",sp
	return (sumatoria)

'''
img = np.asarray(Image.open("cameraman.jpg"))
entropia = primer_orden(img)
so = segundo_orden(img)

print "Entropia : ",entropia," ESO : ",so
'''