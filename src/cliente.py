import os

import numpy as np
from mss import mss



def obten_id_cliente(seleccion_cliente):
    id_cliente = os.popen("xdotool search --onlyvisible --name XATIYARO").read().split()[seleccion_cliente]
    return id_cliente

def mueve_ventana_origen(id_cliente):
    os.popen(f"xdotool windowmove {id_cliente} 0 0")

def coge_geometria(id_cliente):
    geometria = os.popen(f"xwininfo -id {id_cliente}").read().split('-geometry')[1].strip()
    print(id_cliente)
    print(geometria)

    x_origen, y_origen = geometria.split('+')[1:]
    ancho, alto = geometria.split('x')[0],geometria.split('x')[1].split('+')[0]

    geometria = {"top": int(y_origen), "left": int(x_origen), "width": int(ancho), "height": int(alto)}
    return geometria

def obtener_captura(geometria):
    with mss() as sct:
        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(geometria))
        return img[:,:,:3]

