import numpy as np
from PIL import Image
import pygame.camera, pygame.image
from time import sleep

class Sporcamento():

    def read_config(filename):
        options = {}
        f = open(filename)
        for line in f:
            if '#' in line:
                line, comment = line.split('#', 1)
            if '=' in line:
                option, value = line.split('=', 1)
                option = option.strip()
                value = value.strip()
                options[option] = value
        f.close()
        return options

    def img_in_matrice(img):
        print('  Immagine in array')
        img = img.convert('L')
        #prendiamo i dati puri dell'immagine e convertiamola in array in base integer ad 8bit
        return np.asarray(img.getdata(), np.uint8).reshape(img.size[1], img.size[0])

    def crea_differenze(colori, grigi):
        print('  Effettuata differenza tra colori e scala di grigi')
        return colori - grigi

    def salva_immagine_da_array(img, nome):
        #Salviamo l'immagine convertendo da array a stringa
        Image.fromstring('L', (img.shape[1], img.shape[0]), img.tostring()).save(nome)
        print('  Immagine salvata in ' + nome)

    #imhist di matlab
    def conta_bin_e_range(img):
      # get image histogram
      imhist,bins = np.histogram(img.flatten(),256,normed=True)
      cdf = imhist.cumsum() # cumulative distribution function
      cdf = 255 * cdf / cdf[-1] # normalize
      # use linear interpolation of cdf to find new pixel values
      im2 = np.interp(img.flatten(),bins[:-1],cdf)
      return im2.reshape(img.shape), cdf

    def calcola_intensita(intensita):
        array = np.array(range(0, 255))
        for i in array:
            array[i] = i

        return str(sum(array * intensita))

    def indice_sporcamento(riferimento, intensita):
        return str((int(riferimento) + int(intensita))/int(riferimento))

    def init_webcam(options):
        pygame.camera.init()
        cam = pygame.camera.Camera("/dev/video0",(int(options['imageWidth']),int(options['imageHeight'])))
        cam.start()
        return cam

    def scatta_foto(number, options, webcam):
        if str_to_bool(options['onlyWebcam']) == True:
            if number != 0:
                sleep(int(options['sleep']))
            img = webcam.get_image()
            pygame.image.save(img,options['imagePath'] + str(number) + '_webcam.JPG')

def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError
