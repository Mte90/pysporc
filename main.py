#!/usr/bin/python3
from core import Sporcamento as core
from PIL import Image
import numpy as np
import time
start_time = time.time()
#Lettura impostazioni
options = core.read_config('config.ini')
print('Caricamento impostazioni')
if bool(options['onlyWebcam']) == True:
    prefix = '_webcam'
    webcam = core.init_webcam(options)
else:
    webcam = prefix = ''
#Leggo l'immagine
print('Lettura immagine di riferimento')
core.scatta_foto(0, options, webcam)
img_riferimento = Image.open(options['imagePath'] + '0' + prefix + '.JPG', 'r')
#Converto in scala di grigi
img_riferimento_grigio_matrice = core.img_in_matrice(img_riferimento)
pixel_riferimento_totali, intensita_riferimento = core.conta_bin_e_range(img_riferimento_grigio_matrice)
#tanto le dimensioni sono le stesse per tutte
size_x = img_riferimento_grigio_matrice.shape[0]
size_y = img_riferimento_grigio_matrice.shape[1]
#intensita reset
intensita_reset = np.array(range(0, 255))
for i in intensita_reset:
    intensita_reset[i] = 0
intensita = intensita_reset
#cerco di eliminare il rumore
for x in range(size_x):
    for y in range(size_y):
        #sommo le intensita
        intensita[img_riferimento_grigio_matrice[x,y]]+=1

iniettore_riferimento_pulito = core.calcola_intensita(intensita)
#inizializzo i valori
img_diff = img_diff_grigio_matrice = differenza = [1, 2, 3, 4, 5]
numero = indice = '' + "\n"

for count in range(1,(int(options['imageNumber']) + 1)):
    print('Caricamento immagine ' + str(count) + prefix + '.JPG')
    print(' Attesa per il nuovo scatto')
    #leggo l'immagine
    core.scatta_foto(int(count), options, webcam)
    img_diff[count] = Image.open(options['imagePath'] + str(count) + prefix + '.JPG', 'r')
    #converto in scala di grigi
    img_diff_grigio_matrice[count] = core.img_in_matrice(img_diff[count])
    #faccio la differenza
    differenza[count] = core.crea_differenze(img_riferimento_grigio_matrice, img_diff_grigio_matrice[count])
    #intensita reset
    intensita = intensita_reset
    #cerco di eliminare il rumore
    for x in range(size_x):
        for y in range(size_y):
            if img_diff_grigio_matrice[count][x,y] >= int(options['rumour']):
                img_diff_grigio_matrice[count][x,y]=0
            #sommo le intensita
            intensita[img_diff_grigio_matrice[count][x,y]]+=1
    #salvo l'immagine
    core.salva_immagine_da_array(differenza[count], options['imagePath'] + str(count) + prefix + '_differenza.JPG')
    numero += "Numero Sporcamento Differenza " + str(count) + ": " + core.calcola_intensita(intensita) + "\n"
    indice += "Indice Sporcamento " + str(count) + ": " + core.indice_sporcamento(iniettore_riferimento_pulito, core.calcola_intensita(intensita)) + "\n"
#stampo la roba finale
print('Numero Iniettore Pulito: ' + iniettore_riferimento_pulito)
print(numero)
print(indice)
print("--- %s secondi ---" % round(time.time() - start_time, 2))