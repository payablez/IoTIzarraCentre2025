#!/usr/bin/env python3
"""
Ejemplo de parpadeo de LED en Raspberry Pi
Conexiones:
- LED positivo (ánodo) -> GPIO18 (Pin 12)
- LED negativo (cátodo) -> GND (cualquier pin GND)
- Resistencia 220Ω en serie con el LED
"""

import RPi.GPIO as GPIO
import time

# Configuración del pin GPIO
LED_PIN = 18

def setup():
    """Configura el GPIO y el pin del LED"""
    # Usar numeración BCM
    GPIO.setmode(GPIO.BCM)
    # Configurar el pin como salida
    GPIO.setup(LED_PIN, GPIO.OUT)
    print(f"LED configurado en GPIO{LED_PIN}")

def cleanup():
    """Limpia la configuración de GPIO"""
    GPIO.cleanup()
    print("\nPrograma terminado")

def main():
    """Función principal del programa"""
    try:
        setup()
        print("Presiona Ctrl+C para terminar")
        
        while True:
            # Encender LED
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("LED encendido")
            time.sleep(1)
            
            # Apagar LED
            GPIO.output(LED_PIN, GPIO.LOW)
            print("LED apagado")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nInterrupción detectada")
    finally:
        cleanup()

if __name__ == "__main__":
    main() 