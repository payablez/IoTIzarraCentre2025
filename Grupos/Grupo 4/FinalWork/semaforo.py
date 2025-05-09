import requests
from gpiozero import LED, MotionSensor
from time import sleep, time

pir = MotionSensor(18)  # PIR en GPIO 18
led_verde = LED(17)      # LED verde en GPIO 17
led_rojo = LED(27)       # LED rojo en GPIO 27
counter = 0

# Tiempos de duración del ciclo de semáforo
tiempo_rojo = 5  # Tiempo en el que el LED rojo está encendido (detectar movimiento)
tiempo_verde = 5  # Tiempo en el que el LED verde está encendido (sin detectar movimiento)

# URL de tu Node-RED (esto es lo que necesitas cambiar si es necesario)
url = "http://formacioniot2025.devlon.es/grupo4"  # Cambié aquí la URL

while True:
    # Enciende el LED rojo y comienza a detectar movimiento
    led_rojo.on()
    led_verde.off()
    print("LED rojo encendido - Esperando detección de movimiento")
    
    # Detecta movimiento durante el tiempo que el LED rojo está encendido
    movimiento_detectado = False
    tiempo_inicio = time()  # Marca el tiempo de inicio de la fase de detección (rojo)
    
    while time() - tiempo_inicio < tiempo_rojo:
        if pir.motion_detected:
            print("¡Movimiento detectado!")
            movimiento_detectado = True
            counter += 1  # Incrementa el contador de detecciones
            print(f"Detección número: {counter}")
            
            # Preparar los datos a enviar a Node-RED
            data = {
                "detected": 1,
                "detections": counter,
                "time": time()  # Usando la marca de tiempo
            }

            # Enviar los datos a Node-RED mediante una solicitud POST
            try:
                response = requests.post(url, json=data)
                if response.status_code == 200:
                    print("Datos enviados correctamente a Node-RED")
                else:
                    print(f"Error al enviar los datos. Código de estado: {response.status_code}")
            except Exception as e:
                print(f"Error al hacer la solicitud POST: {e}")
        
        sleep(0.5)  # Espera un poco antes de volver a verificar

    # Cambia al LED verde después de que termine el tiempo del LED rojo
    led_rojo.off()
    led_verde.on()
    print("LED verde encendido - No se detecta movimiento")
    
    # Durante el tiempo que el LED verde está encendido, no detecta movimiento
    tiempo_inicio_verde = time()  # Marca el tiempo de inicio de la fase verde
    
    while time() - tiempo_inicio_verde < tiempo_verde:
        sleep(0.5)  # Durante este tiempo, no se detecta movimiento, solo espera
    
    # Después de la fase verde, comienza de nuevo con el LED rojo
    print("Ciclo completo, reiniciando...")
