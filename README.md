# Equitorque LAB - Proyecto Final de Principios de Física

Este repositorio contiene el código fuente de la aplicación de escritorio "Equitorque LAB", desarrollada en Python utilizando la biblioteca Flet. La aplicación permite al usuario calcular el equilibrio estático de un sistema de masas, así como simular diferentes escenarios de equilibrio.

> **NOTA**: Se cumple la función principal del código, no obstante; el proyecto sigue en desarrollo respecto a las demás carácteristicas y mejorar la estética y facilidad de uso.

## Tabla de Contenidos

1. [Requisitos previos](#requisitos-previos)
2. [Instalación](#instalación)
3. [Uso](#uso)
4. [Características](#características)
5. [Modos de Uso](#modos-de-uso)
6. [Contribuir](#contribuir)
7. [Créditos](#créditos)

## Requisitos previos

Para ejecutar la aplicación "Equilibrium App", necesitarás tener instalado Python 3.9 o superior. También es necesario tener instaladas las siguientes bibliotecas:

- Requirements: `pip install -r requirements.txt`
---
- Flet: `pip install flet`
- FluentFlet: `pip install fluentflet`
- Pandas: `pip install pandas`
- XlsxWriter: `pip install XlsxWriter`

## Instalación

1. Clona este repositorio en tu computador local: `git clone https://github.com/xRedDev/torque_y_equilibrio.git`
2. Navega hasta la carpeta del proyecto: `cd equilibrium-app`
3. Ejecuta la aplicación: `python main.py` o `flet run main.py`

> **Descargar ejecutable**: Dirigirse hasta el drive donde está la carpeta con los ejecutables y sus versiones. [Link](https://drive.google.com/file/d/1P7TbJZWDg0hgv0yAb6U7vp1g9MN1Bfw8/view?usp=drive_link)

## Uso

Una vez que la aplicación se haya ejecutado, verás la interfaz de usuario principal. Aquí puedes seleccionar el modo de uso que deseas: "Modo Normal", "Modo Custom" o "Teoría". (en desarrollo los que no son el Modo Normal)

### Modo Normal

En este modo, puedes ingresar el número de masas y sus respectivas propiedades (masa, distancia y lado) para calcular el equilibrio estático. La aplicación generará automáticamente las entradas necesarias y te permitirá calcular el equilibrio. También puedes exportar los resultados a un archivo de Excel.

### Modo Custom (en desarrollo)

En este modo, puedes personalizar el sistema de masas y resortes para simular diferentes escenarios de equilibrio. Puedes ingresar las propiedades de las masas y los resortes, así como las condiciones iniciales. La aplicación te permitirá simular el sistema y visualizar el movimiento de las masas.

### Teoría (en desarrollo)

En esta sección, puedes aprender sobre la teoría del equilibrio estático y sus aplicaciones. También puedes explorar diferentes ejemplos y casos de estudio.

## Características

- Cálculo de equilibrio estático para sistemas de masas y resortes.
- Simulación de diferentes escenarios de equilibrio en el modo "Modo Custom".
- Exportación de resultados a un archivo de Excel.
- Diseño intuitivo y fácil de usar.

## Modos de Uso

- Modo Normal: Calcula el equilibrio estático de un sistema de masas y resortes.
- Modo Custom: Personaliza y simula diferentes escenarios de equilibrio en un sistema de masas.
- Teoría: Aprende sobre la teoría del equilibrio estático y sus aplicaciones.

## Contribuir

Si deseas contribuir al proyecto "Equilibrium App", puedes seguir estos pasos:

1. Fork este repositorio en tu cuenta de GitHub.
2. Clona tu fork localmente: `git clone https://github.com/xRedDev/torque_y_equilibrio.git`
3. Crea una nueva rama para tu contribución: `git checkout -b main`
4. Realiza tus cambios en el código fuente.
5. Añade tus cambios al área de preparación: `git add .`
6. Confirma tus cambios: `git commit -m "Tu comentario sobre la mejora de tu código"`
7. Empuja tus cambios a tu fork: `git push origin main`
8. Crea una solicitud de extracción (PR) en este repositorio para fusionar tus cambios con la rama principal.

## Créditos

Este proyecto fue desarrollado por el equipo de trabajo: 
- JUAN JOSÉ OSORIO DÍAZ
- SHARITH CELESTE CASTILLO MENDOZA
- JAIR ENRIQUE ARMENTA RUEDA

durante el curso de Principios de Física, impartido por el profesor **Jaime Taborda**.

Gracias por utilizar la aplicación "Equitorque LAB"! Esperamos que te sea de utilidad y aprendizaje.
