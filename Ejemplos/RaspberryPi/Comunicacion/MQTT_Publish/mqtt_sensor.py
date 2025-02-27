#!/usr/bin/env python3
"""
Publicador MQTT para datos de sensores
- Lee datos del sensor DHT11
- Publica temperatura y humedad vía MQTT
- Configurable mediante variables de entorno
"""

import paho.mqtt.client as mqtt
import Adafruit_DHT
import RPi.GPIO as GPIO
import json
import time
import schedule
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
MQTT_BROKER = os.getenv('MQTT_BROKER', 'broker.hivemq.com')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'sensors/dht11')
MQTT_CLIENT_ID = os.getenv('MQTT_CLIENT_ID', 'raspberry_sensor')
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = int(os.getenv('DHT_PIN', 4))
PUBLISH_INTERVAL = int(os.getenv('PUBLISH_INTERVAL', 30))  # segundos

# Configuración de LED para indicar estado
LED_PIN = int(os.getenv('LED_PIN', 18))
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
    """Callback cuando se conecta al broker MQTT"""
    if rc == 0:
        print("Conectado al broker MQTT")
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED encendido = conectado
    else:
        print(f"Error de conexión, código: {rc}")
        GPIO.output(LED_PIN, GPIO.LOW)

def on_disconnect(client, userdata, rc):
    """Callback cuando se desconecta del broker MQTT"""
    print("Desconectado del broker MQTT")
    GPIO.output(LED_PIN, GPIO.LOW)

def on_publish(client, userdata, mid):
    """Callback cuando se publica un mensaje"""
    print(f"Mensaje {mid} publicado")
    # Parpadear LED para indicar publicación
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(LED_PIN, GPIO.HIGH)

def read_sensor():
    """Lee datos del sensor DHT11"""
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return temperature, humidity

def publish_sensor_data():
    """Lee y publica datos del sensor"""
    temperature, humidity = read_sensor()
    
    if temperature is not None and humidity is not None:
        # Crear payload
        payload = {
            'temperature': round(temperature, 2),
            'humidity': round(humidity, 2),
            'timestamp': datetime.now().isoformat()
        }
        
        # Publicar mensaje
        client.publish(
            MQTT_TOPIC,
            json.dumps(payload),
            qos=1
        )
        print(f"Datos publicados - Temp: {temperature:.1f}°C, Hum: {humidity:.1f}%")
    else:
        print("Error al leer el sensor")

def main():
    """Función principal"""
    print("Iniciando publicador MQTT...")
    
    try:
        # Configurar cliente MQTT
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_publish = on_publish
        
        # Conectar al broker
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        # Iniciar loop en thread separado
        client.loop_start()
        
        # Programar publicación periódica
        schedule.every(PUBLISH_INTERVAL).seconds.do(publish_sensor_data)
        
        # Loop principal
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        GPIO.cleanup()

if __name__ == '__main__':
    # Crear cliente MQTT
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    main() 