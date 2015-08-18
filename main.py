import sys
try:  
    import pygtk  
    pygtk.require("2.0")  
except:  
    pass  
try:  
    import gtk.glade
    import gtk.gdk
except:  
    print("GTK No Disponible")
    sys.exit(1)

from types import *
import numpy
from PIL import Image
import operaciones, contraste, fracc, histograma, compresion, filtro, igs,huffman,Lmedia,huffman_truncado,codigo_bn
import binary_shift, huffman_shift, lre,caritmetica, entropia
import parchivos as aigs
import arch_huff as ah
import arch_hufft4 as aht4
import arch_cbn as acbn
import arch_lre as al
import arch_ca as aca
import matplotlib.colors as c
import colorsys as cs

class aplicacion_pdi():
    historial = []
    historial_color = []
    indice_historial = -1
    hist_img = None
    imagen = None
    wTree = None
    L = 256
    dialogo_tp = None
    nombre_archivo = None
    h = None 
    color = False
    imagen_color = None

    def __init__(self):
        self.wTree = gtk.glade.XML("pdi.glade")
        dic = {
            "on_imageMain_destroy": self.salir,
            "on_menuSalir_activate": self.salir,
            "on_abrir_activate": self.abrir_imagen,
            "on_bnegativo_clicked": self.img_negativo,
            "on_bsuma_clicked": self.pide_valor,
            "on_bresta_clicked": self.pide_valor,
            "on_bdiv_clicked": self.pide_valor,
            "on_bmult_clicked": self.pide_valor,
            "on_bcontraste_clicked": self.ingresa_valores_contraste,
            "on_bfracc1_clicked": self.ingresa_valores_fracc,
            "on_bfracc2_clicked": self.ingresa_valores_fracc2,
            "on_bfnb_clicked": self.ingresa_fnb,
            "on_bhist_clicked": self.abre_histograma,
            "on_bcdr_clicked": self.ingresa_crd,
            "on_bdeshacer_clicked": self.regresa_estado_anterior,
            "on_brehacer_clicked": self.avanza_estado_siguiente,
            "on_boxfilter_activate": self.aplica_filtro,
            "on_weightedavg_activate": self.aplica_filtro,
            "on_lap_a_activate": self.aplica_filtro,
            "on_lap_b_activate": self.aplica_filtro,
            "on_lap_c_activate": self.aplica_filtro,
            "on_lap_d_activate": self.aplica_filtro,
            "on_diferencial_activate": self.ingresa_diferencial,
            "on_ideal_activate": self.aplica_filtro_frecuencias,
            "on_butterworth_activate": self.aplica_filtro_frecuencias,
            "on_gaussian_activate": self.aplica_filtro_frecuencias,
            "on_guardar_como_activate": self.guardar_imagen,
            "on_bigs_clicked": self.guarda_igs,
            "on_bhfm_clicked": self.guarda_huffman,
            "on_bhft_clicked": self.guarda_huffman_truncado,
            "on_bcbn_clicked": self.guarda_codigo_bn,
            "on_bbsh_clicked": self.guarda_binary_shift,
            "on_bhfs_clicked": self.guarda_huffman_shift,
            "on_blre_clicked": self.guarda_lre,
            "on_bcar_clicked": self.guarda_cod_ar,
            "on_primer_orden_activate": self.abre_msj_entropia,
            "on_segundo_orden_activate": self.abre_msj_entropia,
            "on_ok_entropia_clicked": self.cierra_msj,
        }
        self.wTree.signal_autoconnect(dic)
        self.dialogo_tp = self.wTree.get_widget("tipo_archivo")
        gtk.main()
        
    def dibujar_img(self, img):
        img_rgb = Image.new("RGB", (img.shape[0], img.shape[1]))
        
        if self.color == True:
            self.imagen_color[:,:,2] = self.imagen.reshape(self.imagen_color.shape[0],self.imagen_color.shape[1])
            img_rgb = Image.fromarray(c.hsv_to_rgb(self.imagen_color).astype(numpy.uint8))
        else:
            img_rgb = Image.fromarray(img).convert("RGB")

        img_pixbuf = gtk.gdk.pixbuf_new_from_array(numpy.asarray(img_rgb), gtk.gdk.COLORSPACE_RGB, 8)

        dest_x = 600.0
        escala = " 100%"
        if img.shape[1] > dest_x:
            dest_y = img.shape[0]*(dest_x/img.shape[1])
            img_pixbuf = img_pixbuf.scale_simple(int(dest_x), int(dest_y), gtk.gdk.INTERP_BILINEAR)
            escala = "{0:.2f}".format((dest_x/img.shape[1])*100)+"%"
        
        self.wTree.get_widget("image1").set_from_pixbuf(img_pixbuf)
        self.wTree.get_widget("dimension").set_label(str(img.shape[1])+"x"+str(img.shape[0]))
        self.wTree.get_widget("escala").set_active(0)
        self.actualiza_histograma()

    def abrir_imagen(self, widget):
        img = None
        fc = gtk.FileChooserDialog(title='Abrir imagen...', parent=None, action=gtk.FILE_CHOOSER_ACTION_OPEN, 
                                   buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        fc.set_default_response(gtk.RESPONSE_OK)
        respuesta = fc.run()
        if respuesta == gtk.RESPONSE_OK:
            self.nombre_archivo = fc.get_filename()
            ext = self.nombre_archivo[-4:]

            if ext == ".jpg":
                img = Image.open(self.nombre_archivo)
                self.imagen = numpy.asarray(img,dtype=numpy.float64)
                if len(self.imagen.shape) == 3: # si es a color
                    self.imagen_color = c.rgb_to_hsv(self.imagen)
                    self.imagen = self.imagen_color[:,:,2]
                    self.imagen = self.imagen.astype(numpy.uint8)
                    self.color = True
                else:
                    self.color = False
            else:
                self.imagen = self.switch_ext(ext)

            self.dibujar_img(self.imagen)
            self.historial = []
            self.historial_color = []
            self.indice_historial = -1
            self.actualiza_historial()
        fc.destroy()

    def guardar_imagen(self, widget):
        if self.imagen != None:
            fc = gtk.FileChooserDialog(title='Guardar como...', parent=None, action=gtk.FILE_CHOOSER_ACTION_SAVE, 
                                       buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
            fc.set_default_response(gtk.RESPONSE_OK)
            respuesta = fc.run()
            if respuesta == gtk.RESPONSE_OK:
                self.nombre_archivo = fc.get_filename()
                self.dialogo_tp.show()
            fc.destroy()

    def guarda_igs(self,widget):
        n = self.wTree.get_widget("igs_n").get_text()
        n = int(n)
        img_x = igs.igs(self.imagen.astype(numpy.uint8),n)
        if aigs.crea_guarda_archivo_igs(self.nombre_archivo+".igs",img_x,n):
            print "Archivo creado!"
        self.dialogo_tp.hide()

    def abre_igs(self):
        md = aigs.abre_igs(self.nombre_archivo)
        print "Archivo leido!, recuperando bytes..."
        lista_bytes = igs.recupera_bytes(md[1],md[0][2])
        print "Bytes recuperados, transformando a valores originales..."
        valores = igs.transforma_bytesavalores(lista_bytes)
        print "Valores transformados, construyendo matriz leida..."
        m = igs.recupera_matriz(md[0][0],md[0][1],valores)
        #print "Matriz leida de archivo: \n",m
        return igs.normaliza_a(self.L,md[0][2],m)

    def guarda_huffman(self,widget):
        imagen_aux = Image.fromarray(self.imagen)
        h = imagen_aux.histogram()
        tabla_codigos = huffman.genera_tabla_codigos(h)
        lm = Lmedia.calcula_L_media(tabla_codigos.items,(self.imagen.shape[0]*self.imagen.shape[1]))
        cadena01 = huffman.codificar_img(tabla_codigos,self.imagen)
        self.wTree.get_widget("dimension").set_label("Lmedia : "+str(lm))
        if ah.crea_guarda_archivo_huffman(self.nombre_archivo+".hfm",self.imagen,tabla_codigos,cadena01):
            print "Archivo Huffman creado!"
        self.dialogo_tp.hide()

    def abre_huffman(self):
        md = ah.abre_huffman(self.nombre_archivo)
        valores = huffman.decodificar_img(md[0],md[1],md[2],md[3])
        img = numpy.asarray(huffman.recupera_matriz(md[0],md[1],valores))
        return img

    def guarda_huffman_truncado(self,widget):
        t = self.wTree.get_widget("hft_t").get_text()
        imagen_aux = Image.fromarray(self.imagen)
        h = imagen_aux.histogram()
        tc = huffman_truncado.genera_tabla_codigos_truncado(h,int(t))
        dim = self.imagen.shape[0]*self.imagen.shape[1]
        lm = Lmedia.calcula_L_media(tc.items,dim)
        self.wTree.get_widget("dimension").set_label("Lmedia : "+str(lm))
        cadena01 = huffman_truncado.codificar_img(tc,self.imagen)

        if aht4.crea_guarda_archivo(self.nombre_archivo+".htf",self.imagen,tc,cadena01):
            print "Archivo huffman truncado creado!"
        self.dialogo_tp.hide()

    def abre_huffman_truncado(self):
        md = aht4.abre_archivo(self.nombre_archivo)
        valores = huffman_truncado.decodificar_img(md[0],md[1],md[2],md[3])
        img = numpy.asarray(huffman_truncado.recupera_matriz(md[0],md[1],valores))
        return img

    def guarda_codigo_bn(self,widget):
        imagen_aux = Image.fromarray(self.imagen)
        h = imagen_aux.histogram()
        n = self.wTree.get_widget("cbn_n").get_text()
        tc = codigo_bn.tabla_base(h,int(n))
        tc.asigna_codigo()
        dim = self.imagen.shape[0]*self.imagen.shape[1]
        lm = Lmedia.calcula_L_media(tc.items,dim)
        self.wTree.get_widget("dimension").set_label("Lmedia : "+str(lm))
        cadena01 = codigo_bn.codificar_img(tc,self.imagen)

        if acbn.crea_guarda_archivo(self.nombre_archivo+".cbn",self.imagen,tc,cadena01):
            print "Archivo codigo bn creado!"
        self.dialogo_tp.hide()

    def abre_codigo_bn(self):
        md = acbn.abre_archivo(self.nombre_archivo)
        valores = codigo_bn.decodificar_img(md[0],md[1],md[2],md[3],md[4])
        img = numpy.asarray(codigo_bn.recupera_matriz(md[0],md[1],valores))
        return img

    def guarda_binary_shift(self,widget):
        imagen_aux = Image.fromarray(self.imagen)
        h = imagen_aux.histogram()
        nbl = self.wTree.get_widget("bsh_nb").get_text()
        tc = binary_shift.tabla_base(h,int(nbl))
        tc.asigna_codigo()
        dim = self.imagen.shape[0]*self.imagen.shape[1]
        lm = Lmedia.calcula_L_media(tc.items,dim)
        self.wTree.get_widget("dimension").set_label("Lmedia : "+str(lm))
        cadena01 = binary_shift.codificar_img(tc,self.imagen)
        if aht4.crea_guarda_archivo(self.nombre_archivo+".bsh",self.imagen,tc,cadena01):
            print "Archivo binary shift creado!"
        self.dialogo_tp.hide()

    def abre_binary_shift(self):
        md = aht4.abre_archivo(self.nombre_archivo)
        valores = binary_shift.decodificar_img(md[0],md[1],md[2],md[3])
        img = numpy.asarray(binary_shift.recupera_matriz(md[0],md[1],valores))
        return img

    def guarda_huffman_shift(self,widget):
        imagen_aux = Image.fromarray(self.imagen)
        h = imagen_aux.histogram()
        nbl = self.wTree.get_widget("hfs_nb").get_text()
        tc = huffman_shift.genera_tabla_codigos_shift(h,int(nbl))
        dim = self.imagen.shape[0]*self.imagen.shape[1]
        lm = Lmedia.calcula_L_media(tc.items,dim)
        self.wTree.get_widget("dimension").set_label("Lmedia : "+str(lm))
        cadena01 = huffman_shift.codificar_img(tc,self.imagen)
        if aht4.crea_guarda_archivo(self.nombre_archivo+".hfs",self.imagen,tc,cadena01):
            print "Archivo huffman shift creado!"
        self.dialogo_tp.hide()

    def abre_huffman_shift(self):
        md = aht4.abre_archivo(self.nombre_archivo)
        valores = huffman_shift.decodificar_img(md[0],md[1],md[2],md[3])
        img = numpy.asarray(huffman_shift.recupera_matriz(md[0],md[1],valores))
        return img

    def guarda_lre(self,widget):
        planos = lre.dame_planos(self.imagen.astype(numpy.uint8))
        items = lre.genera_items(planos)
        if al.crea_guarda_archivo(self.nombre_archivo+".lre",self.imagen.astype(numpy.uint8),items):
            print "Archivo LRE creado!"
        self.dialogo_tp.hide()

    def abre_lre(self):
        md = al.abre_archivo(self.nombre_archivo)
        img = lre.decodificacion(md[0],md[1],md[2])
        return img

    def guarda_cod_ar(self,widget):
        tam_fragmento = 2
        imagen_aux = Image.fromarray(self.imagen)
        h = imagen_aux.histogram()
        img_f = self.imagen.flatten()
        tablalim = caritmetica.tabla_limites(h,float(len(img_f)))
        nums = caritmetica.codifica_img(tablalim,img_f,tam_fragmento)

        if aca.crea_guarda_archivo(self.nombre_archivo+".car",self.imagen,tablalim,nums,tam_fragmento):
            print "Archivo codificacion aritmetica creado!"
        self.dialogo_tp.hide()

    def abre_cod_ar(self):
        md = aca.abre_archivo(self.nombre_archivo)
        matriz = caritmetica.decodificacion(md[0],md[1],md[2],md[3],md[4])
        img = matriz.astype(numpy.uint8)
        return img

    def switch_ext(self,ext):
        if ext == ".igs":
            img = self.abre_igs()
        elif ext == ".hfm":
            img = self.abre_huffman()
        elif ext == ".htf":
            img = self.abre_huffman_truncado()
        elif ext == ".cbn":
            img = self.abre_codigo_bn()
        elif ext == ".bsh":
            img = self.abre_binary_shift()
        elif ext == ".hfs":
            img = self.abre_huffman_shift()
        elif ext == ".lre":
            img = self.abre_lre()
        elif ext == ".car":
            img = self.abre_cod_ar()

        return img

    def abre_msj_entropia(self,widget):
        if self.imagen != None:
            nombre = widget.get_name()
            if nombre == "primer_orden":
                cad = "Est. de 1er orden: " + str(entropia.primer_orden(self.imagen))
            else:
                cad = "Est. de 2o orden: " + str(entropia.segundo_orden(self.imagen))

            self.wTree.get_widget("label_entropia").set_text(cad)
            self.wTree.get_widget("mnsj").show()

    def cierra_msj(self,widget):
        self.wTree.get_widget("mnsj").hide()


    def salir(self, widget):
        gtk.main_quit()

    ''' CODIGO ALGORITMOS... '''

    ''' Negativo. '''

    def img_negativo(self, widget):
        if self.imagen != None:
            self.imagen = (self.L - 1) - self.imagen
            self.dibujar_img(self.imagen)
            self.actualiza_historial()

    ''' Calculo de distancias entre pixeles. '''

    def distancia_euclidiana(self,x,y,s,t):
        de = sqrt(pow(x-s,2)+pow(y-t,2))
        return de

    def distancia_d4(self,x,y,s,t):
        dd4 = abs(x-s)+abs(y-t)
        return dd4

    def distancia_d8(self,x,y,s,t):
        dd8 = max(abs(x-s),abs(y-t))
        return dd8

    ''' Operaciones +,-,*,/. '''

    def pide_valor(self,widget):
        operacion = operaciones.Operacion(self)
        operacion.abre_dialogo_valor(widget)

    ''' Contraste. '''

    def ingresa_valores_contraste(self,widget):
        c = contraste.Contraste(self)
        c.abre_dialogo(widget)

    ''' Fraccionamiento de nivel de grises. '''

    def ingresa_valores_fracc(self,widget):
        fng1 = fracc.Fng(self)
        fng1.abre_dialogo_fracc1()

    def ingresa_valores_fracc2(self,widget):
        fng2 = fracc.Fng(self)
        fng2.abre_dialogo_fracc2()

    ''' Fraccionamiento a nivel de bits. '''

    def ingresa_fnb(self,widget):
        fnb = fracc.Fnb(self)
        fnb.abre_dialogo()

    ''' Histograma. '''

    def abre_histograma(self,widget):
        self.hist_img.muestra_grafico()

    def actualiza_histograma(self):
        if type(self.hist_img) is NoneType:
            self.hist_img = histograma.Vista_histograma(self)

        self.hist_img.dibujar_histograma(self.imagen)

    ''' Compresion de rango dinamico. '''

    def ingresa_crd(self,widget):
        crd = compresion.Rango_dinamico(self)
        crd.abre_dialogo()

    ''' Deshacer/Rehacer. '''

    def regresa_estado_anterior(self,widget):
        if len(self.historial) > 1 and self.indice_historial > 0:
            self.indice_historial -= 1
            img_aux = self.historial[self.indice_historial]
            self.imagen = img_aux
            if self.color == True:
                imgc_aux = self.historial_color[self.indice_historial]
                self.imagen_color = imgc_aux
            self.dibujar_img(self.imagen)

    def avanza_estado_siguiente(self,widget):
        if self.indice_historial < (len(self.historial)-1):
            self.indice_historial += 1
            img_aux = self.historial[self.indice_historial]
            self.imagen = img_aux
            if self.color == True:
                imgc_aux = self.historial_color[self.indice_historial]
                self.imagen_color = imgc_aux
            self.dibujar_img(self.imagen)

    def verificar_siguientes_estados(self):
        if self.indice_historial < (len(self.historial)-1):
            for i in range(self.indice_historial,len(self.historial)-1):
                    self.historial.pop()
                    if self.color == True:
                        self.historial_color.pop()

    def actualiza_historial(self):
        self.verificar_siguientes_estados()
        self.historial.append(self.imagen)
        self.historial_color.append(self.imagen_color)
        self.indice_historial += 1

    ''' FILTROS EN EL DOMINIO ESPACIAL. '''

    ''' Smoothing/Sharpening. '''

    def aplica_filtro(self,widget):
        fil_esp = filtro.Espacial(self)
        fil_esp.abre_dialogo(widget)

    ''' Gradient (Diferencial - Sobel). '''
    
    def ingresa_diferencial(self,widget):
        fil_dif = filtro.Diferencial(self)
        fil_dif.abre_dialogo()

    ''' FILTROS EN EL DOMINIO DE LAS FRECUENCIAS. '''

    ''' Ideal(Fourier)/Butterworth/Gaussian. '''

    def aplica_filtro_frecuencias(self,widget):
        ff = filtro.Frecuencia(self)
        ff.abre_dialogo(widget)

start = aplicacion_pdi()
