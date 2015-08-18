try:  
    import gtk.glade
except:  
    print("GTK No Disponible")
    sys.exit(1)

import numpy

class Fng():

	dialogo = None
	A = None
	B = None
	lim1 = None
	lim2 = None
	label12 = None
	aplicacion = None
	tipo = None

	def __init__(self,aplicacion):
		wTree = gtk.glade.XML("pdi.glade","fraccionamiento")
		self.dialogo = wTree.get_widget("fraccionamiento")
		self.A = wTree.get_widget("A")
		self.B = wTree.get_widget("B")
		self.lim1 = wTree.get_widget("lim1")
		self.lim2 = wTree.get_widget("lim2")
		self.label12 = wTree.get_widget("label12")
		self.aplicacion = aplicacion
		dic = {
		        "on_cancelar2_clicked": self.cierra_dialogo,
		    	"on_aceptar2_clicked": self.modifica_niveles,
		      }
		wTree.signal_autoconnect(dic)

	def abre_dialogo_fracc1(self):
	    if self.aplicacion.imagen != None:
	        self.lim2.show()
	        self.label12.show()
	        self.tipo = 1
	        self.dialogo.show()

	def abre_dialogo_fracc2(self):
	    if self.aplicacion.imagen != None:
	        self.lim2.hide()
	        self.label12.hide()
	        self.tipo = 2
	        self.dialogo.show()

	def cierra_dialogo(self,widget):
		self.dialogo.destroy()

	def modifica_niveles(self,widget):
	    try:
	        A = int(self.A.get_text())
	        B = int(self.B.get_text())
	        lim1 = int(self.lim1.get_text())
	        lim2 = self.lim2.get_text()
	        l2 = 0

	        if lim2 != "":
	            l2 =  int(lim2)

	        switch = {
	                    1: self.fracc1(self.aplicacion.imagen,A,B,lim1,l2),
	                    2: self.fracc2(self.aplicacion.imagen,A,B,lim1)
	                 }
	        self.aplicacion.imagen = switch[self.tipo]
	        self.aplicacion.dibujar_img(self.aplicacion.imagen)
	    except ValueError(" error"):
	        print "Error en la entrada!"

	    self.cierra_dialogo(widget)
	    self.aplicacion.actualiza_historial()


	def fracc1(self,r,A,B,lim1,lim2):
	    temp1 = ((r<A).astype(numpy.uint8))
	    temp2 = (((r>=A)&(r<B)).astype(numpy.uint8))
	    temp3 = ((r>=B).astype(numpy.uint8))
	    sa = temp1*lim1
	    sb = temp2*lim2
	    sc = temp3*lim1
	    s = sa + sb + sc
	    return s

	def fracc2(self,r,A,B,lim1):
	    temp1 = (((r>=A)&(r<B)).astype(numpy.uint8))
	    temp2 = (((r<A)|(r>=B)).astype(numpy.uint8))

	    sa = temp1*lim1
	    sb = temp2*r
	    s = sa + sb
	    return s

class Fnb():

	dialogo = None
	entrada = None
	aplicacion = None

	def __init__(self,aplicacion):
		wTree = gtk.glade.XML("pdi.glade","num_fnb")
		self.dialogo = wTree.get_widget("num_fnb")
		self.entrada = wTree.get_widget("entry2")
		self.aplicacion = aplicacion
		dic = {
		        "on_aceptar3_clicked": self.muestra_capa,
            	"on_cancelar3_clicked": self.desaparece_dialogo,
		      }
		wTree.signal_autoconnect(dic)

	def abre_dialogo(self):
	    if  self.aplicacion.imagen != None:
	        self.dialogo.show()

	def muestra_capa(self,widget):
	    try:
	        nbit = int(self.entrada.get_text())
	        self.aplicacion.imagen = self.fraccionamiento_nbits(self.aplicacion.imagen,nbit,self.aplicacion.L)
	        self.aplicacion.dibujar_img(self.aplicacion.imagen)
	    except ValueError(" error"):
	        print "Error en la entrada!"

	    self.desaparece_dialogo(widget)
	    self.aplicacion.actualiza_historial()

	def desaparece_dialogo(self,widget):
	    self.dialogo.destroy()

	def fraccionamiento_nbits(self,r,nbit,L):
		try:
			img = r & pow(2,nbit-1)
			img = img >> (nbit-1)
			img = img * (L-1)
		except ValueError(" error"):
			print "Error fraccionamiento_nbits(r,nbit,L)"
		return img
