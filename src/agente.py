import os
import subprocess
import time
import _thread as thread

import numpy as np
import torch
import torch.nn as nn
import cv2
from PIL.ImageQt import rgb
from matplotlib import pyplot as plt
from mss import mss

from utils.augmentations import letterbox
from utils.general import increment_path, non_max_suppression
from yolov5.models.common import Conv
from yolov5.models.experimental import Ensemble
from yolov5.utils.downloads import attempt_download

import psutil
from PIL import Image, ImageDraw
from torchvision import transforms


class AgenteRagnarok:
    def __init__(self,cliente, configuracion_global, configuracion_personaje):
        self.configuracion_global = configuracion_global

        self.rol = configuracion_personaje['rol']
        self.pesos = configuracion_personaje['pesos']

        self.id_cliente = self.obten_id_cliente()
        self.geometria = self.coge_geometria()

        self.model = self.cargar_modelo(self.pesos)

        self.turno = False
        self.vision,self.vision_completa = self.obtener_captura()

    def empezar_farmeo(self):
        i = 0
        while True:
            i = i + 1
            imagen, imagen_completa = self.obtener_captura()
            im = transforms.ToPILImage()(imagen[0]).convert("RGB")

            pred = self.model(imagen)[0]
            pred = non_max_suppression(pred, 0.5, 0.5, None, False, max_det=1000)
            try:
                pred_x, pred_y, pred_w, pred_h, confidence, cls = pred[0][0]
                img1 = ImageDraw.Draw(im)
                img1.rectangle((pred_x, pred_y, pred_w, pred_h), width=1)

                left_pad = self.geometria['left']
                top_pad = self.geometria['top']
                window_width = self.geometria['width']
                window_height = self.geometria['height']

                x_1 = (pred_x + pred_w) / 2
                y_1 = (pred_y + pred_h) / 2


                x_1 = ((x_1 / 416) * window_width) + left_pad
                y_1 = ((y_1 / 416) * window_height) + top_pad

                pulsa('2', self.id_cliente)
                click(x_1, y_1)
                img2 = ImageDraw.Draw(imagen_completa)
                img2.rectangle((x_1, y_1, x_1, y_1), width=10)

                im.save(f"imagenes/poison_spore/nc_{str(i)}.jpeg")
                imagen_completa.save(f"imagenes/imagen_completa/{str(i)}.jpeg")
                # display image for 10 seconds22

                # hide image
                for proc in psutil.process_iter():
                    if proc.name() == "display":
                        proc.kill()
                        # pass

            except Exception as e:
                time.sleep(0.3)
                pulsa('9', self.id_cliente)
                time.sleep(0.5)
                if np.random.random() > 0.5:
                    pulsa('3', self.id_cliente)
                if np.random.random() > 0.8:
                    pulsa('4', self.id_cliente)

    def cargar_modelo(self, weights, map_location=None, inplace=True, fuse=True):
        from models.yolo import Detect, Model

        # Loads an ensemble of models weights=[a,b,c] or a single model weights=[a] or weights=a
        model = Ensemble()
        for w in weights if isinstance(weights, list) else [weights]:
            ckpt = torch.load(attempt_download(w), map_location=map_location)  # load
            print(ckpt.get('ema'))
            if fuse:
                model.append(ckpt['ema' if ckpt.get('ema') else 'model'].float().fuse().eval())  # FP32 model
            else:
                model.append(ckpt['ema' if ckpt.get('ema') else 'model'].float().eval())  # without layer fuse

        # Compatibility updates
        for m in model.modules():
            if type(m) in [nn.Hardswish, nn.LeakyReLU, nn.ReLU, nn.ReLU6, nn.SiLU, Detect, Model]:
                m.inplace = inplace  # pytorch 1.7.0 compatibility
                if type(m) is Detect:
                    if not isinstance(m.anchor_grid, list):  # new Detect Layer compatibility
                        delattr(m, 'anchor_grid')
                        setattr(m, 'anchor_grid', [torch.zeros(1)] * m.nl)
            elif type(m) is Conv:
                m._non_persistent_buffers_set = set()  # pytorch 1.6.0 compatibility

        if len(model) == 1:
            return model[-1]  # return model
        else:
            print(f'Ensemble created with {weights}\n')
            for k in ['names']:
                setattr(model, k, getattr(model[-1], k))
            model.stride = model[torch.argmax(torch.tensor([m.stride.max() for m in model])).int()].stride  # max stride
            return model  # return ensemble

    def obtener_captura(self):
        with mss() as sct:
            # Get raw pixels from the screen, save it to a Numpy array

            # imagen pantalla completa para debug
            sct_img = sct.grab({'top': 0, 'left': 0, 'width': 1680, 'height': 1050})
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.save("hola.jpeg")

            imagen = np.array(sct.grab(self.geometria))[:, :, :3]
            imagen = cv2.resize(imagen, dsize=(416, 416), interpolation=cv2.INTER_CUBIC)
            # imagen = letterbox(imagen, [416, 416], stride=16, auto=False)[0]
            imagen = imagen.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to R2GB
            imagen = np.ascontiguousarray(imagen)
            imagen = torch.from_numpy(imagen).to('cpu').float()
            imagen /= 255.0
            imagen = imagen[None]
            print(imagen.shape)
            return imagen, img

    def mueve_ventana_origen(self):
        os.popen(f"xdotool windowmove {self.id_cliente} 0 0")

    def obten_id_cliente(self):
        id_cliente = os.popen("xdotool search --onlyvisible --name XATIYARO").read().split()[-1]
        return id_cliente

    def coge_geometria(self):
        geometria = os.popen(f"xwininfo -id {self.id_cliente}").read().split('-geometry')[1].strip()

        x_origen, y_origen = geometria.split('+')[1:]
        ancho, alto = geometria.split('x')[0], geometria.split('x')[1].split('+')[0]

        return {"top": int(y_origen), "left": int(x_origen), "width": int(ancho), "height": int(alto)}


def click(x, y):
    os.system(f"xdotool mousemove {x} {y}")
    os.system('xmacroplay "$DISPLAY" < test.file')


def pulsa(tecla, id_cliente):
    os.system(f"xdotool windowactivate {id_cliente}")
    os.system(f"xdotool key {tecla}")
