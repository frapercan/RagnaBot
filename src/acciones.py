import os


def click(x, y):
    os.system(f"xdotool mousemove {x} {y}")
    os.system('xmacroplay "$DISPLAY" < test.file')

def pulsa(tecla,id_cliente):
    os.system(f"xdotool windowactivate {id_cliente}")
    os.system(f"xdotool key {tecla}")