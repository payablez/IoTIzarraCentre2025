from gpiozero import LED
from time import sleep

led = LED(18)           # Ajusta al pin GPIO del LED

led.on()               # Enciende el LED
sleep(2)               # Mantiene el LED encendido por 2 segundos
led.off()              # Apaga el LED