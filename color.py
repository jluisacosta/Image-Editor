import numpy as np
from PIL import Image

img = Image.open("cameraman.jpg")
imgc = Image.open("colores.jpg")

print "cameraman : ", len(np.asarray(img).shape)
print "colores : ", len(np.asarray(imgc).shape)