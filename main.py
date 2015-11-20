#!/usr/bin/python3
from core import Sporcamento as core
from PIL import Image
import numpy as np
import time
start_time = time.time()

#Leggo l'immagine
print('Lettura immagine di riferimento')
img_riferimento = Image.open('0_orig.JPG', 'r')

#Converto in scala di grigi
img_riferimento_grigio_matrice = core.img_in_matrice(img_riferimento)
pixel_riferimento_totali, intensita_riferimento = core.conta_bin_e_range(img_riferimento_grigio_matrice)

#tanto le dimensioni sono le stesse per tutte
size_x = img_riferimento_grigio_matrice.shape[0]
size_y = img_riferimento_grigio_matrice.shape[1]

intensita = np.array(range(0, 255))

for i in intensita:
    intensita[i] = 0

for x in range(size_x):
    for y in range(size_y):
        #sommo le intensita
        intensita[img_riferimento_grigio_matrice[x,y]]+=1

iniettore_riferimento_pulito = core.calcola_intensita(intensita)

#inizializzo i valori
img_diff = img_diff_grigio_matrice = differenza = [1, 2, 3, 4, 5]
numero = indice = '' + "\n"

for count in range(1,5):
    print('Caricamento immagine ' + str(count) + '_orig.JPG')
    #leggo l'immagine
    img_diff[count] = Image.open(str(count) + '_orig.JPG', 'r')
    #converto in scala di grigi
    img_diff_grigio_matrice[count] = core.img_in_matrice(img_diff[count])
    #faccio la differenza
    differenza[count] = core.crea_differenze(img_riferimento_grigio_matrice, img_diff_grigio_matrice[count])

    intensita = np.array(range(0, 255))
    for i in intensita:
        intensita[i] = 0

    for x in range(size_x):
        for y in range(size_y):
            #cerco di eliminare il rumore
            if img_diff_grigio_matrice[count][x,y] >= 120:
                img_diff_grigio_matrice[count][x,y]=0
            #sommo le intensita
            intensita[img_diff_grigio_matrice[count][x,y]]+=1

    core.salva_immagine_da_array(differenza[count], str(count) + '_differenza.JPG')
    numero += "Numero Sporcamento Differenza " + str(count) + ": " + core.calcola_intensita(intensita) + "\n"
    indice += "Indice Sporcamento " + str(count) + ": " + core.indice_sporcamento(iniettore_riferimento_pulito, core.calcola_intensita(intensita)) + "\n"

print('Numero Iniettore Pulito: ' + iniettore_riferimento_pulito)
print(numero)
print(indice)
print("--- %s secondi ---" % round(time.time() - start_time, 2))