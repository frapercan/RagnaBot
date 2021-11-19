import os
import time

import numpy as np
from mss import mss
import _thread as thread


class Cliente:
    def __init__(self, configuracion_global, configuracion_personaje):
        self.configuracion_global = configuracion_global
        self.configuracion_personaje = configuracion_personaje
        self.id_cliente = configuracion_personaje['id_cliente']
        self.geometria = None

    def arrancar_cliente(self):
        ficheros_juego_original = os.path.join(self.configuracion_global['directorio_juegos'],
                                               self.configuracion_global['nombre_juego_original'], '*')

        directorio_juego = os.path.join(self.configuracion_global['directorio_juegos'],
                                        self.configuracion_global['nombre_juego']
                                        + str(self.id_cliente))
        ficheros_juego = os.path.join(directorio_juego, '*')
        directorio_prefix = os.path.join(self.configuracion_global['directorio_prefixes'],
                                         str(self.id_cliente))

        ejecutable_cliente = os.path.join(directorio_juego, self.configuracion_global['nombre_cliente'])

        ficheros_parche = os.path.join(self.configuracion_global['directorio_juegos'],
                                       self.configuracion_global['nombre_parche'], '*')

        coordenadas_boton_jugar = self.configuracion_global['coordenadas_boton_jugar']
        jugar_x = coordenadas_boton_jugar[0]
        jugar_y = coordenadas_boton_jugar[1]

        # Ejecutamos el juego a través de Wine

        os.system(f"rm -r {ficheros_juego}")
        os.system(f"cp -r {ficheros_juego_original} {directorio_juego}")

        thread.start_new_thread(os.system,
                                (f"cd {directorio_juego} && WINEPREFIX={directorio_prefix} wine {ejecutable_cliente}",))

        # Esperamos a que el cliente se actualize
        time.sleep(3)
        parchear_juego(ficheros_parche, directorio_juego)
        click_en_jugar(jugar_x, jugar_y)

        time.sleep(self.configuracion_global['inicio_cliente_espera'])
        self.posicionar_ventana()
        self.hacer_login()
        self.coge_geometria()

        return True

    def posicionar_ventana(self):
        self.id_ventana = self.obten_id_ventana()
        self.mueve_ventana_grid()

    def mueve_ventana_grid(self):
        posicion_x = self.configuracion_global['margen_izquierdo'] + \
                     self.id_cliente * self.configuracion_global['ancho_cliente']

        os.popen(f"xdotool windowmove {self.id_ventana} {posicion_x} 0")
        os.system(f"xdotool windowactivate {self.id_ventana}")

    def obten_id_ventana(self):
        id_ventanas = os.popen("xdotool search --onlyvisible --name XATIYARO").read().split()
        id_ventanas.sort()
        id_ventana = id_ventanas[self.id_cliente]
        print(id_ventanas)
        return id_ventana

    def coge_geometria(self):
        geometria = os.popen(f"xwininfo -id {self.id_ventana}").read().split('-geometry')[1].strip()

        x_origen, y_origen = geometria.split('+')[1:]
        ancho, alto = geometria.split('x')[0], geometria.split('x')[1].split('+')[0]

        self.geometria = {"top": int(y_origen), "left": int(x_origen), "width": int(ancho), "height": int(alto)}

    def hacer_login(self):
        self.pulsa('KP_Enter')
        time.sleep(1)

        self.escribe(self.configuracion_personaje['usuario'])
        time.sleep(1)

        self.pulsa('0xff09')
        time.sleep(1)

        self.escribe(self.configuracion_personaje['contraseña'])
        time.sleep(1)

        self.pulsa('KP_Enter')
        time.sleep(1)
        self.pulsa('KP_Enter')
        time.sleep(1)
        self.pulsa('KP_Enter')

    def pulsa(self, tecla):
        print(tecla, self.id_ventana)
        os.system(f"xdotool windowactivate {self.id_ventana}")
        os.system(f"xdotool key {tecla}")

    def escribe(self, texto):
        print(texto, self.id_ventana)

        os.system(f"xdotool windowactivate {self.id_ventana}")
        os.system(f"xdotool type {texto}")
        print(f"xdotool type '{texto}'")


def parchear_juego(ficheros_parche, directorio_juego):
    os.system(f"cp -r {ficheros_parche} {directorio_juego}")
    print('parcheado!', directorio_juego)


def click_en_jugar(jugar_x, jugar_y):
    os.system(f'xdotool mousemove {jugar_x} {jugar_y}')
    os.system('xdotool click 1')


def obten_id_cliente(seleccion_cliente):
    id_cliente = os.popen("xdotool search --onlyvisible --name XATIYARO").read().split()[seleccion_cliente]
    return id_cliente


def mueve_ventana_origen(id_cliente):
    os.popen(f"xdotool windowmove {id_cliente} 0 0")


def coge_geometria(id_cliente):
    geometria = os.popen(f"xwininfo -id {id_cliente}").read().split('-geometry')[1].strip()

    x_origen, y_origen = geometria.split('+')[1:]
    ancho, alto = geometria.split('x')[0], geometria.split('x')[1].split('+')[0]

    geometria = {"top": int(y_origen), "left": int(x_origen), "width": int(ancho), "height": int(alto)}
    return geometria


def obtener_captura(geometria):
    with mss() as sct:
        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(geometria))
        return img[:, :, :3]



