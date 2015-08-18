try:  
    import gtk.glade
except:  
    print("GTK No Disponible")
    sys.exit(1)

import numpy
from PIL import Image, ImageFilter

class Diferencial():

	dialogo = None
	entrada = None
	check = None
	aplicacion = None

	def __init__(self,aplicacion):
	    wTree = gtk.glade.XML("pdi.glade","dialogo_dif")
	    self.dialogo = wTree.get_widget("dialogo_dif")
	    self.entrada = wTree.get_widget("dif_entry")
	    self.check = wTree.get_widget("dif_predeterminado")
	    self.aplicacion = aplicacion
	    dic = {
	            "on_aceptar5_clicked": self.aplica_mascara,
	        	"on_cancelar5_clicked": self.desaparece_dialogo,
	          }
	    wTree.signal_autoconnect(dic)

	def abre_dialogo(self):
	    if  self.aplicacion.imagen != None:
	        self.dialogo.show()

	def aplica_mascara(self,widget):
	    try:
	        band = self.check.get_active()
	        diferencial = int(self.entrada.get_text())
	        self.aplicacion.imagen = self.filtro_diferencial(self.aplicacion.imagen,diferencial,band)
	        self.aplicacion.dibujar_img(self.aplicacion.imagen)
	    except ValueError(" error"):
	        print "Error en la entrada!"

	    self.desaparece_dialogo(widget)
	    self.aplicacion.actualiza_historial()

	def desaparece_dialogo(self,widget):
	    self.dialogo.destroy()

	def filtro_diferencial(self,r,diferencial,band):
	    img = Image.fromarray(r)
	    img1 = img.filter(ImageFilter.Kernel((3,3),[-1,-2,-1,0,0,0,1,2,1],1))
	    img2 = img.filter(ImageFilter.Kernel((3,3),[-1,0,1,-2,0,2,-1,0,1],1))
	    dif = numpy.array(img1, dtype=numpy.int16)+numpy.array(img2, dtype=numpy.int16)
	    temp1 = ((dif>diferencial).astype(numpy.uint8))
	    temp2 = ((dif<=diferencial).astype(numpy.uint8))
	    if band == True:
	        s = (temp1*255)+(temp2*0)
	    else:
	        s = (temp1*255)+(temp2*img)

	    return s

class Espacial():

	dialogo = None
	aplicacion = None
	menu = None

	def __init__(self,aplicacion):
		wTree = gtk.glade.XML("pdi.glade","matriz_selecc")
		self.dialogo = wTree.get_widget("matriz_selecc")
		self.aplicacion = aplicacion
		dic = {
		        "on_b3x3_clicked": self.aplica_filtro3x3,
		    	"on_b5X5_clicked": self.aplica_filtro5x5,
		      }
		wTree.signal_autoconnect(dic)

	def abre_dialogo(self,widget):
		if  self.aplicacion.imagen != None:
			self.menu = widget
	        self.dialogo.show()

	def desaparece_dialogo(self):
	    self.dialogo.destroy()
	
	def aplica_filtro3x3(self,widget):
		self.procesa_imagen(3)

	def aplica_filtro5x5(self,widget):
		self.procesa_imagen(5)

	def procesa_imagen(self,tam_matriz):
		if self.aplicacion.imagen != None:
			L =  self.asigna_valores_filtro(tam_matriz)
			imgf = Image.fromarray(self.aplicacion.imagen)
			img_aux = imgf.filter(ImageFilter.Kernel(L[0],L[1],L[2]))
			self.aplicacion.imagen = numpy.asarray(img_aux)
			self.aplicacion.dibujar_img(self.aplicacion.imagen)
			self.desaparece_dialogo()
			self.aplicacion.actualiza_historial()

	def asigna_valores_filtro(self,tam_matriz):
		nom_menu = self.menu.get_name()
		L = []
		if tam_matriz == 3:
			switch = {
		                    "boxfilter": [[1,1,1,1,1,1,1,1,1],9],
		                    "weightedavg": [[1,2,1,2,4,2,1,2,1],16],
		                    "lap_a": [[0,1,0,1,-4,1,0,1,0],1],
		                    "lap_b": [[1,1,1,1,-8,1,1,1,1],1],
		                    "lap_c": [[0,-1,0,-1,4,-1,0,-1,0],1],
		                    "lap_d": [[-1,-1,-1,-1,8,-1,-1,-1,-1],1]
		                    }
			elementos = switch[nom_menu]
			L.append((3,3))
			L.append(elementos[0])
			L.append(elementos[1])
		else:
			switch2 = {
		                    "boxfilter": [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],25],
		                    "weightedavg": [[0,1,2,1,0,1,2,4,2,1,2,4,8,4,2,1,2,4,2,1,0,1,2,1,0],48],
		                    "lap_a": [[0,0,1,0,0,0,1,1,1,0,1,1,-12,1,1,0,1,1,1,0,0,0,1,0,0],1],
		                    "lap_b": [[1,1,1,1,1,1,1,1,1,1,1,1,-24,1,1,1,1,1,1,1,1,1,1,1,1],1],
		                    "lap_c": [[0,0,-1,0,0,0,-1,-1,-1,0,-1,-1,12,-1,-1,0,-1,-1,-1,0,0,0,-1,0,0],1],
		                    "lap_d": [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,24,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],1]
		                    }
			elementos2 = switch2[nom_menu]
			L.append((5,5))
			L.append(elementos2[0])
			L.append(elementos2[1])

		return L

class Frecuencia():

	dialogo = None
	tb_radio = None
	tb_n = None
	aplicacion = None
	filtro = None
	combo_tipo = None
	l19 = None

	def __init__(self,aplicacion):
	    wTree = gtk.glade.XML("pdi.glade","filtros_f")
	    self.dialogo = wTree.get_widget("filtros_f")
	    self.tb_radio = wTree.get_widget("radio_txt")
	    self.tb_n = wTree.get_widget("n_txt")
	    self.combo_tipo = wTree.get_widget("tipo_filtro")
	    self.l19 = wTree.get_widget("label19")
	    self.aplicacion = aplicacion
	    dic = {
	            "on_aceptarF_clicked": self.aplica_filtrofrecuencia,
	        	"on_cancelarF_clicked": self.desaparece_dialogo,
	          }
	    wTree.signal_autoconnect(dic)

	def abre_dialogo(self,widget):
		if  self.aplicacion.imagen != None:
			self.filtro = widget.get_name() 
			self.combo_tipo.set_active(0)
			self.dialogo.set_title(widget.get_label())
			if self.filtro != "butterworth":
				self.tb_n.hide()
				self.l19.hide()
			self.dialogo.show()

	def desaparece_dialogo(self,widget):
	    self.dialogo.destroy()

	def aplica_filtrofrecuencia(self,widget):
		try:
			switch = {
						0:"paso bajo",
						1:"paso alto",
						}
			tipo = switch[self.combo_tipo.get_active()]
			radio = int(self.tb_radio.get_text())
			n = self.tb_n.get_text()

			if n != "":
				n = int(n)
			else:
				n = 0

			self.aplicacion.imagen = self.transforma(self.aplicacion.imagen,radio,n,self.filtro,tipo)
			self.aplicacion.dibujar_img(self.aplicacion.imagen)
			print "radio: "+str(radio)+" n: "+str(n)+" filtro: "+self.filtro+" tipo: "+tipo
		except ValueError(" error"):
			print "Error en la entrada!"
		
		self.desaparece_dialogo(widget)
		self.aplicacion.actualiza_historial()

	def seleccion_operacion(self,dist,D0,n,filtro,tipo):
		if tipo == "paso bajo":
			switch = {
			            "ideal": (dist<=D0),
			            "butterworth": (1/(1+((dist/D0)**(2*n)))),
			            "gaussian": (numpy.exp(-(dist**2)/(2*(D0)**2)))
			         }
		elif tipo == "paso alto":
			switch = {
			            "ideal": (dist>D0),
			            "butterworth": (1/(1+((D0/dist)**(2*n)))),
			            "gaussian": (1-(numpy.exp(-(dist**2)/(2*(D0)**2))))
			         }
		return switch[filtro]


	def transforma(self,img,radio,n,filtro,tipo):
		if self.aplicacion.imagen != None:
			F = numpy.fft.fft2(img)
			F2 = numpy.fft.fftshift(F)

			x = numpy.arange(-img.shape[1]/2.0, img.shape[1]/2.0)
			X = numpy.tile(x, (img.shape[0], 1))
			y = numpy.arange(-img.shape[0]/2.0, img.shape[0]/2.0)[:, numpy.newaxis]
			Y = numpy.tile(y, (1, img.shape[1]))
			dist = numpy.sqrt(X**2 + Y**2)

			MascaraI = self.seleccion_operacion(dist,radio,n,filtro,tipo)

			F3 = F2 * MascaraI
			F4 = numpy.fft.ifftshift(F3)
			F5 = numpy.fft.ifft2(F4).astype(numpy.uint8)
			return F5
