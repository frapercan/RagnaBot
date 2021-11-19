import os
import signal

from pynput import keyboard
from threading import Thread
import concurrent.futures

from src.agente import AgenteRagnarok
import yaml

from src.cliente import Cliente

cliente = 0
pesos = 'pesos/pay_fild05_v2.pt'


def on_press(key):
    if key == keyboard.Key.esc:
        os.kill(os.getpid(), signal.SIGINT)


if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    configuracion_global_fichero = open("configuracion/global.yaml")
    configuracion_personajes_fichero = open("configuracion/personajes.yaml")

    # scalar values to Python the dictionary format
    configuracion_global = yaml.load(configuracion_global_fichero, Loader=yaml.FullLoader)
    configuracion_personajes = yaml.load(configuracion_personajes_fichero, Loader=yaml.FullLoader)

    clientes = [Cliente(configuracion_global, configuracion_personaje) for configuracion_personaje in
                configuracion_personajes]



    for cliente in clientes:
        cliente.arrancar_cliente()


    agentes = [AgenteRagnarok(cliente,configuracion_global=configuracion_global,configuracion_personaje=configuracion_personajes['personajes'][0])]
    agente = AgenteRagnarok(configuracion_global=configuracion_global,configuracion_personaje=configuracion_personajes[0])
    agente.empezar_farmeo()

    agente = AgenteRagnarok(cliente, configuracion_global=configuracion_global,
                   configuracion_personaje=configuracion_personajes[0])
    agente.empezar_farmeo()



