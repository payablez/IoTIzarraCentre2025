# -*- coding: utf-8 -*-

''' Copyright (C) 2017 Iván Rodríguez Méndez
This software is distributed under the GNU General Public
Licence (version 3 or later); please refer to the file
Licence.txt, included with the software, for details.
'''

import RPi.GPIO as GPIO
import time

# Configuración de pines
GPIO.setmode(GPIO.BCM)

# Pines para los semáforos de peatones
verde_peaton = 14  # GPIO 14 (LED verde peatones)
rojo_peaton = 18   # GPIO 18 (LED rojo peatones)

# Configuración del sensor PIR
PIR_PIN = 27  # GPIO 27 (sensor PIR)
GPIO.setup(PIR_PIN, GPIO.IN)

# Configuración de los pines de los semáforos
GPIO.setup(verde_peaton, GPIO.OUT)
GPIO.setup(rojo_peaton, GPIO.OUT)

# Configuración de tiempo
tiempoCruce = 3  # Tiempo que se mantiene el semáforo verde

# Función para cambiar el semáforo
def cambioSemaforo():
    GPIO.output(rojo_peaton, False)  # Apagar el semáforo rojo
    GPIO.output(verde_peaton, True)  # Encender el semáforo verde
    print("Semáforo verde para peatones ENCENDIDO")
    time.sleep(tiempoCruce)  # Mantener verde por el tiempo de cruce

    # Parpadeo de semáforo verde (como señal de cruce)
    for i in range(10):
        GPIO.output(verde_peaton, True)
        time.sleep(0.25)
        GPIO.output(verde_peaton, False)
        time.sleep(0.25)
    
    GPIO.output(rojo_peaton, True)  # Después de 10 parpadeos, apagar el verde y encender el rojo
    print("Semáforo rojo para peatones ENCENDIDO")

def main():
    # Configuración inicial (Rojo encendido)
    GPIO.output(verde_peaton, False)
    GPIO.output(rojo_peaton, True)
    
    tiempoCambio = time.time()  # Tiempo de la última acción

    while True:
        # Leer el estado del sensor PIR
        estado_pir = GPIO.input(PIR_PIN)

        # Si el sensor PIR detecta movimiento y ha pasado suficiente tiempo
        if estado_pir == GPIO.HIGH and (time.time() - tiempoCambio > 5):
            print("Movimiento detectado.")
            tiempoCambio = time.time()  # Actualizar el tiempo de la última detección
            cambioSemaforo()  # Cambiar el semáforo cuando se detecte movimiento
        
        time.sleep(0.1)  # Esperar un poco para evitar la lectura continua sin descanso

# Ejecutar el programa principal
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
    finally:
        GPIO.cleanup()  # Limpiar la configuración de los pines GPIO al finalizar
