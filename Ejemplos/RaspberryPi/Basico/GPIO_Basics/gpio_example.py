#!/usr/bin/env python3
"""
Ejemplo básico de GPIO en Raspberry Pi
- Control de LED
- Lectura de botón
- Uso de PWM
- Manejo de interrupciones
"""

import RPi.GPIO as GPIO
import time
import schedule
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de pines
LED_PIN = int(os.getenv('LED_PIN', 18))
BUTTON_PIN = int(os.getenv('BUTTON_PIN', 23))
PWM_PIN = int(os.getenv('PWM_PIN', 12))

def setup():
    """Configura los pines GPIO"""
    # Usar numeración BCM
    GPIO.setmode(GPIO.BCM)
    
    # Configurar pines
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PWM_PIN, GPIO.OUT)
    
    # Crear objeto PWM
    pwm = GPIO.PWM(PWM_PIN, 100)  # 100 Hz
    pwm.start(0)
    
    return pwm

def button_callback(channel):
    """Callback para el botón"""
    if GPIO.input(channel):
        print("Botón liberado")
        GPIO.output(LED_PIN, GPIO.LOW)
    else:
        print("Botón presionado")
        GPIO.output(LED_PIN, GPIO.HIGH)

def blink_led():
    """Parpadea el LED"""
    GPIO.output(LED_PIN, not GPIO.input(LED_PIN))

def fade_led(pwm):
    """Efecto de fade en LED con PWM"""
    # Aumentar brillo
    for dc in range(0, 101, 5):
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.1)
    
    # Disminuir brillo
    for dc in range(100, -1, -5):
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.1)

def main():
    """Función principal"""
    print("Iniciando ejemplo de GPIO...")
    
    try:
        # Configuración inicial
        pwm = setup()
        
        # Configurar detección de eventos del botón
        GPIO.add_event_detect(
            BUTTON_PIN,
            GPIO.BOTH,
            callback=button_callback,
            bouncetime=200
        )
        
        # Programar parpadeo del LED cada 2 segundos
        schedule.every(2).seconds.do(blink_led)
        
        # Loop principal
        while True:
            schedule.run_pending()
            
            # Efecto fade cada 5 segundos
            fade_led(pwm)
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pwm.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    main() 