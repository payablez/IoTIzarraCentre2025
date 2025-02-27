#!/usr/bin/env python3
"""
Ejemplo de uso de triggers en Raspberry Pi
Este script demuestra el uso de interrupciones y eventos con GPIO
"""

import RPi.GPIO as GPIO
import time
from datetime import datetime

# Configuración de pines
BUTTON_PIN = 17  # Pin para el botón
LED_PIN = 18     # Pin para el LED
PIR_PIN = 27     # Pin para sensor PIR (movimiento)

def setup():
    """Configura los pines GPIO"""
    GPIO.setmode(GPIO.BCM)
    
    # Configurar botón con resistencia pull-up
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Configurar LED como salida
    GPIO.setup(LED_PIN, GPIO.OUT)
    
    # Configurar sensor PIR como entrada
    GPIO.setup(PIR_PIN, GPIO.IN)

def button_callback(channel):
    """Callback para el evento del botón"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    state = "presionado" if GPIO.input(channel) == GPIO.LOW else "liberado"
    print(f"[{timestamp}] Botón {state}")
    
    # Toggle LED
    GPIO.output(LED_PIN, not GPIO.input(LED_PIN))

def pir_callback(channel):
    """Callback para el sensor de movimiento"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    if GPIO.input(channel):
        print(f"[{timestamp}] ¡Movimiento detectado!")
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        print(f"[{timestamp}] Sin movimiento")
        GPIO.output(LED_PIN, GPIO.LOW)

def main():
    """Función principal del programa"""
    try:
        setup()
        print("Iniciando ejemplo de triggers...")
        print("Presiona Ctrl+C para terminar")
        
        # Configurar detección de eventos para el botón
        # Detecta tanto flanco de subida como de bajada
        GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, 
                            callback=button_callback, 
                            bouncetime=300)
        
        # Configurar detección de eventos para el sensor PIR
        GPIO.add_event_detect(PIR_PIN, GPIO.BOTH,
                            callback=pir_callback,
                            bouncetime=300)
        
        # Mantener el programa en ejecución
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.cleanup()
        print("Limpieza de GPIO completada")

if __name__ == "__main__":
    main() 