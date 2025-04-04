from gpiozero import LED, MotionSensor
from time import sleep, time

pir = MotionSensor(18)  # PIR en GPIO 18
led = LED(17)           # LED en GPIO 17
counter = 0

ultima_deteccion = 0
tiempo_filtro = 2  # Solo activa el LED si han pasado 2 segundos desde la última detección

while True:
    print(counter)
    sleep(1)
    if pir.motion_detected:
        counter = counter + 1
        ahora = time()
        if ahora - ultima_deteccion > tiempo_filtro:
            print("¡Movimiento detectado!")
            led.on()
            ultima_deteccion = ahora
    else:
        led.off()
    sleep(1)
