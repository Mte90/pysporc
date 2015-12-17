#!/usr/bin/python3
from core import Sporcamento as core
from core import str_to_bool
from PIL import Image
import numpy as np
import time
start_time = time.time()
#Lettura impostazioni
options = core.read_config('config.ini')
print('Caricamento impostazioni')
webcam = prefix = ''
if str_to_bool(options['onlyWebcam']) == True:
    prefix = '_webcam'
    webcam = core.init_webcam(options)
    options['imagePath'] += 'webcam/'
else:
    output_folder = options['imagePath'] + 'output/'
    options['imagePath'] += 'sporc/'

#Leggo l'immagine
#print('Lettura immagine di riferimento')
#if str_to_bool(options['onlyWebcam']) == True:
#    core.scatta_foto(0, options, webcam)
#img_riferimento = Image.open(options['imagePath'] + '0' + prefix + '.jpg', 'r')
##Converto in scala di grigi
#img_riferimento_grigio_matrice = core.img_in_matrice(img_riferimento)
#pixel_riferimento_totali, intensita_riferimento = core.conta_bin_e_range(img_riferimento_grigio_matrice)

#tanto le dimensioni sono le stesse per tutte
size_x = int(options['imageWidth'])
size_y = int(options['imageHeight'])

#iniettore_riferimento_pulito = core.calcola_intensita(intensita)
#inizializzo i valori
img_diff = ''
img_grigio_matrice = {}
img_differenza = list(range(1,(int(options['imageNumber']))))
numero = indice = '' + "\n"

#Carico le immagini
for folder in range(1,(int(options['sporcNumber'])+1)):
    for count in range(1,(int(options['imageNumber']))):
        print('Caricamento immagine ' + str(folder) + '/' + str(count) + prefix + '.jpg')
        if str_to_bool(options['onlyWebcam']) == True:
            print(' Attesa per il nuovo scatto')
            #leggo l'immagine
            core.scatta_foto(int(count), options, webcam)
        else:
            img_diff = Image.open(options['imagePath'] + str(folder) + '/' + str(count) + prefix + '.jpg', 'r')
            #converto in scala di grigi
            img_grigio_matrice[folder,count] = core.img_in_matrice(img_diff,options)

#elaboro Immagini
for count in range(1,(int(options['imageNumber']))):
    print('Analisi immagine ' + str(count))
    #faccio la differenza
    img_differenza = core.crea_differenze(img_grigio_matrice[1,count], img_grigio_matrice[2,count])
    img_differenza = img_differenza[0]
    #salvo l'immagine
    if str_to_bool(options['onlyWebcam']) != True:
        core.salva_immagine_da_array(img_differenza, output_folder + str(count) + prefix + '_differenza.jpg', options)
    else:
        core.salva_immagine_da_array(img_differenza, options['imagePath'] + str(count) + prefix + '_differenza.jpg', options)
#    numero += "Numero Sporcamento Differenza " + str(count) + ": " + core.calcola_intensita(intensita) + "\n"
#    indice += "Indice Sporcamento " + str(count) + ": " + core.indice_sporcamento(iniettore_riferimento_pulito, core.calcola_intensita(intensita)) + "\n"
#stampo la roba finale
#print('Numero Iniettore Pulito: ' + iniettore_riferimento_pulito)
print(numero)
print(indice)
print("--- %s secondi ---" % round(time.time() - start_time, 2))