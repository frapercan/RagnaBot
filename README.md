# Plantilla de programas para Python

![pipy](https://badge.fury.io/py/plantilla-programas-python.svg)
[![codecov](https://codecov.io/gh/BREKIADATA-SL/plantilla-programas-python/branch/main/graph/badge.svg?token=2T1J6LQTJE)](https://codecov.io/gh/BREKIADATA-SL/plantilla-programas-python)


El objetivo de este repositorio es servir de referencia a las distintas herramientas que se están desarrollado dentro de la organización para estandar las siguientes funcionalidades en cada uno de los entornos de trabajo:

-   Empaquetamiento con Pipy
-   Ejecución del Análisis estático del código en integración continua
-   Ejecución de la Generación automatica de Documentación en integración continua
-   Ejecución de pruebas unitarias en integración continua

## Paquete Python

Este repositorio está configurado en los ficheros setup.py y setup.cfg para compilar toda la lógica y empaquetarlas dentro del sistema de PIPY.

De forma que podremos hacer uso de:

pip3 install plantilla-programas-python

## Ejecutar Integración continua en local

Tox es una herramienta de automatización para python, sus comandos son los siguientes:

### Ejecutar Tests, Lint y Compilar la documentación

    tox

### Ejecutar tests

    tox -e py38

### Ejecutar Lint

    tox -e lint

### Compilar la documentación

    tox -e docs


## Integración continua
Github está configurado con dos distintas comprobaciones.

### Tox

Se ejecutará cada vez que se haga una Pull request y realizara el comando Tox completo. Indicandote si todo a ido bien.

### Publicación del paquete en Python

Se ejecutará cada vez que se haga una Pull Request a la rama "Main".

Solamente pasará si el paquete no existe previamente en el repositorio de paquetes, por lo tanto cuando estemos seguros de que todo está finalizado deberemos hacer uso de los comandos:

    bumpversion minor 

Dentro de la version actual del paquete, incrementa en 1 la subversion

    bumversion major (Incrementa la version)
    
 Incrementa la version del paquete



## Documentación
Al estar trabajando sobre repositorios privados, no podemos utilizar readthedocs para alojar la nuestra.

Pero igualmente estára accesible para los desarrolladores bajo el directorio:

/docs/_build/html

![docs](https://github.com/BREKIADATA-SL/plantilla-programas-python/raw/main/imagenes/docs.png)
# RagnaBot
