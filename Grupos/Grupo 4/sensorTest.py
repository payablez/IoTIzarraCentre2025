import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)  # PIR en GPIO 18

while True:
    estado = GPIO.input(18)
    print(f"Estado PIR: {estado}")  # Imprime 0 si detecta movimiento, 1 si no
    time.sleep(1)
