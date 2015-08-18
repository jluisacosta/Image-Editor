try:  
    import gtk.glade
except:  
    print("GTK No Disponible")
    sys.exit(1)

import numpy

class Contraste():
    dialogo = None
    r1 = None
    r2 = None
    s1 = None
    s2 = None
    aplicacion = None

    def __init__(self,aplicacion):
        wTree = gtk.glade.XML("pdi.glade","contraste")
        self.dialogo = wTree.get_widget("contraste")
        self.r1 = wTree.get_widget("r1")
        self.r2 = wTree.get_widget("r2")
        self.s1 = wTree.get_widget("s1")
        self.s2 = wTree.get_widget("s2")
        self.aplicacion = aplicacion
        dic = {
                "on_cancelar_clicked": self.desaparece_dialogo,
                "on_aceptar_clicked": self.aplica,
              }
        wTree.signal_autoconnect(dic)

    def abre_dialogo(self,widget):
        if self.aplicacion.imagen != None:
            self.dialogo.set_title(widget.get_tooltip_text())
            self.dialogo.show()

    def aplica(self,widget):
        try:
            r1 = int(self.r1.get_text())
            r2 = int(self.r2.get_text())
            s1 = int(self.s1.get_text())
            s2 = int(self.s2.get_text())
            self.aplicacion.imagen = self.contraste(self.aplicacion.imagen,r1,s1,r2,s2,self.aplicacion.L)
            self.aplicacion.dibujar_img(self.aplicacion.imagen)
        except ValueError(" error"):
            print "Error en la entrada!"

        self.desaparece_dialogo(widget)
        self.aplicacion.actualiza_historial()

    def desaparece_dialogo(self,widget):
        self.dialogo.destroy()

    def contraste(self,r,r1,s1,r2,s2,L):
        temp1 = ((r < r1).astype(numpy.uint8))
        temp2 = (((r >= r1)&(r < r2)).astype(numpy.uint8))
        temp3 = ((r >= r2).astype(numpy.uint8))

        sa = temp1*((s1/r1)*r)
        sb = temp2*((s2-s1)/(r2-r1)*r+(s1-(s2-s1)/(r2-r1)*r1))
        sc = temp3*((L-s2)/(L-r2)*r+s2-((L-s2)/(L-r2))*r2)

        s = sa + sb + sc
        return s