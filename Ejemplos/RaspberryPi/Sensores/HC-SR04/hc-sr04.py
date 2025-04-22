#Script para python raspberry pi para leer distancia de sensor hc-sr04 con la librería DistanceSensor de gpiozero

#https://gpiozero.readthedocs.io/en/stable/api_input.html#distancesensor-hc-sr04
#Connect the GND pin of the sensor to a ground pin on the Pi.
#Connect the TRIG pin of the sensor a GPIO pin.
#Connect one end of a 330Ω resistor to the ECHO pin of the sensor.
#Connect one end of a 470Ω resistor to the GND pin of the sensor.
#Connect the free ends of both resistors to another GPIO pin. This forms the required voltage divider.
#Finally, connect the VCC pin of the sensor to a 5V pin on the Pi.

from gpiozero import DistanceSensor
import time

sensor = DistanceSensor(echo=24, trigger=23)

while True:
    print(sensor.distance)
    time.sleep(1)