try:  
    import gtk.glade
except:  
    print("GTK No Disponible")
    sys.exit(1)
import numpy

class Operacion():
    dialogo = None
    TextBox = None
    tipo = None
    aplicacion = None

    def __init__(self,aplicacion):
        wTree = gtk.glade.XML("pdi.glade","entrada")
        self.dialogo = wTree.get_widget("entrada")
        self.TextBox = wTree.get_widget("entry1")
        self.aplicacion = aplicacion
        dic = {
                "on_cancelar1_clicked": self.desaparece_dialogo,
                "on_aceptar1_clicked": self.ejecuta,
              }
        wTree.signal_autoconnect(dic)

    def abre_dialogo_valor(self,widget):
        if  self.aplicacion.imagen != None:
            self.tipo = widget.get_name()
            self.dialogo.set_title(widget.get_tooltip_text())
            self.dialogo.show()

    def ejecuta(self,widget):
        try:
            valor = int(self.TextBox.get_text())
            switch = {
                        "bsuma": self.suma(self.aplicacion.imagen,valor,self.aplicacion.L),
                        "bresta": self.resta(self.aplicacion.imagen,valor,self.aplicacion.L),
                        "bdiv": self.division(self.aplicacion.imagen,valor,self.aplicacion.L),
                        "bmult": self.multiplicacion(self.aplicacion.imagen,valor,self.aplicacion.L)
                     }
            self.aplicacion.imagen = switch[self.tipo]
            self.aplicacion.dibujar_img(self.aplicacion.imagen)
        except ValueError(" error"):
            print "Error en la entrada!"

        self.desaparece_dialogo(widget)
        self.aplicacion.actualiza_historial()

    def desaparece_dialogo(self,widget):
        self.dialogo.destroy()

    def suma(self,r, valor,L):
        s = (numpy.clip(numpy.array(r, dtype=numpy.int32)+valor, 0, L-1)).astype(numpy.uint8)
        return s

    def resta(self,r,valor,L):
        s = (numpy.clip(numpy.array(r, dtype=numpy.int32)-valor, 0, L-1)).astype(numpy.uint8)
        return s

    def division(self,r,valor,L):
        s = (numpy.clip(numpy.array(r, dtype=numpy.float32)/valor, 0, L-1)).astype(numpy.uint8)
        return s

    def multiplicacion(self,r,valor,L):
        s = (numpy.clip(numpy.array(r, dtype=numpy.int64)*valor, 0, L-1)).astype(numpy.uint8)
        return s
