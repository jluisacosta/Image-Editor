try:  
    import gtk.glade
except:  
    print("GTK No Disponible")
    sys.exit(1)
    
import numpy

class Rango_dinamico():

    dialogo = None
    entrada = None
    aplicacion = None

    def __init__(self,aplicacion):
        wTree = gtk.glade.XML("pdi.glade","comp_rd")
        self.dialogo = wTree.get_widget("comp_rd")
        self.entrada = wTree.get_widget("entry3")
        self.aplicacion = aplicacion
        dic = {
                "on_aceptar4_clicked": self.aplica_rango,
                "on_cancelar4_clicked": self.desaparece_dialogo,
              }
        wTree.signal_autoconnect(dic)

    def abre_dialogo(self):
        if  self.aplicacion.imagen != None:
            self.dialogo.show()

    def aplica_rango(self,widget):
        try:
            nbit = int(self.entrada.get_text())
            self.aplicacion.imagen = self.comp_rango_dinamico(self.aplicacion.imagen,nbit)
            self.aplicacion.dibujar_img(self.aplicacion.imagen)
        except ValueError(" error"):
            print "Error en la entrada!"

        self.desaparece_dialogo(widget)
        self.aplicacion.actualiza_historial()

    def desaparece_dialogo(self,widget):
        self.dialogo.destroy()

    def comp_rango_dinamico(self,r,nbit):
        L = pow(2,nbit)
        R = r.shape[0]
        c = (L-1)/numpy.log10(R)
        s = (numpy.clip(c*numpy.log10(1+numpy.array(r, dtype=numpy.int32)), 0, R-1)).astype(numpy.uint8)
        SX = s/float(L-1)
        SX2 = (SX*255).astype(numpy.uint8)
        return SX2