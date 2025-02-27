#!/usr/bin/env python3
"""
Ejemplo de lectura de temperatura y humedad con sensor DHT11 en Raspberry Pi
Conexiones:
- Pin de datos del DHT11 -> GPIO4 (Pin 7)
- VCC del DHT11 -> 3.3V
- GND del DHT11 -> GND
"""

import Adafruit_DHT
import time
from datetime import datetime

# Configuración del sensor
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

def read_sensor():
    """Lee los datos del sensor DHT11"""
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    return humidity, temperature

def main():
    """Función principal del programa"""
    print("Iniciando lectura del sensor DHT11...")
    print("Presiona Ctrl+C para terminar")
    
    try:
        while True:
            humidity, temperature = read_sensor()
            
            if humidity is not None and temperature is not None:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{current_time}] Temperatura: {temperature:.1f}°C, Humedad: {humidity:.1f}%")
            else:
                print("Error al leer el sensor. Verificar conexiones.")
            
            # Esperar 2 segundos antes de la siguiente lectura
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 