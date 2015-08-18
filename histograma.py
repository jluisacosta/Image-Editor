try:  
    import gtk.glade
    import gtk.gdk
except:  
    print("GTK No Disponible")
    sys.exit(1)

import numpy
from PIL import Image, ImageDraw

class Vista_histograma():

    ventana = None
    img_hist = None
    aplicacion = None

    def __init__(self,aplicacion):
        wTree = gtk.glade.XML("pdi.glade","histograma")
        self.ventana = wTree.get_widget("histograma")
        self.img_hist = wTree.get_widget("hist_img")
        self.aplicacion = aplicacion

    def muestra_grafico(self):
        if self.aplicacion.imagen != None:
            self.ventana.show()

    def dibujar_histograma(self, img):
        imagen_aux = Image.fromarray(img)
        hist = imagen_aux.histogram()
        max_hist = max(hist)
        valor_mult = 1

        color_fondo = (255,255,255)
        color_linea = (0,0,0)

        histograma = Image.new("RGB", (self.aplicacion.L, self.aplicacion.L), color_fondo)
        pinta = ImageDraw.Draw(histograma)

        y = float(self.aplicacion.L)/max_hist
        x = 0
        for i in hist:
            if int(i)==0: pass
            else:
                pinta.line((x,self.aplicacion.L, x, self.aplicacion.L-(i*y)), fill=color_linea)        
            if x > (self.aplicacion.L-1): x=0
            else: x += 1

        histograma = numpy.asarray(histograma)
        img_rgb = Image.new("RGB", (histograma.shape[0], histograma.shape[1]))
        try:
            if histograma.shape[2] == 3:
                img_rgb = Image.fromarray(histograma)
        except:
            img_rgb = Image.fromarray(histograma).convert("RGB")
        img_pixbuf = gtk.gdk.pixbuf_new_from_array(numpy.asarray(img_rgb), gtk.gdk.COLORSPACE_RGB, 8)

        dest_x = 600.0
        if img.shape[1] > dest_x:
            dest_y = histograma.shape[0]*(dest_x/histograma.shape[1])
            img_pixbuf = img_pixbuf.scale_simple(int(dest_x), int(dest_y), gtk.gdk.INTERP_BILINEAR)
        
        self.img_hist.set_from_pixbuf(img_pixbuf)

