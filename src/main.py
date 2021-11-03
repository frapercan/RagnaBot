import os
import signal

from pynput import keyboard

from src.agente import AgenteRagnarok

cliente = 0
pesos = 'pesos/pay_fild05_v2.pt'


def on_press(key):
    if key == keyboard.Key.esc:
        os.kill(os.getpid(), signal.SIGINT)


if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread

    agente = AgenteRagnarok(cliente, pesos)
    agente.empezar_farmeo()

    import torch
    # while True:
    #
    #     # start_time = time.time()
    #     # habilidad_en_monstruo(1,directorio_monstruo)
    #
    #     print("--- %s seconds ---" % (time.time() - start_time))
