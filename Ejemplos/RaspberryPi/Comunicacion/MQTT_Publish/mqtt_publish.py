#!/usr/bin/env python3
"""
Ejemplo de publicación MQTT en Raspberry Pi
Este script publica datos de temperatura simulados a un broker MQTT
"""

import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime

# Configuración MQTT
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/raspberry/sensor"
CLIENT_ID = f"raspberry-pi-{random.randint(0, 1000)}"

def on_connect(client, userdata, flags, rc):
    """Callback que se ejecuta cuando se conecta al broker"""
    if rc == 0:
        print("Conectado al broker MQTT")
        print(f"Usando cliente ID: {CLIENT_ID}")
    else:
        print(f"Error de conexión, código: {rc}")

def on_publish(client, userdata, mid):
    """Callback que se ejecuta cuando se publica un mensaje"""
    print(f"Mensaje {mid} publicado")

def create_message():
    """Crea un mensaje con datos simulados"""
    return {
        "timestamp": datetime.now().isoformat(),
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(40, 60), 2),
        "device_id": CLIENT_ID
    }

def main():
    """Función principal del programa"""
    # Crear cliente MQTT
    client = mqtt.Client(CLIENT_ID)
    
    # Asignar callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        # Conectar al broker
        print(f"Conectando a {MQTT_BROKER}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        # Iniciar loop en segundo plano
        client.loop_start()
        
        print("Presiona Ctrl+C para terminar")
        
        while True:
            # Crear y publicar mensaje
            message = create_message()
            payload = json.dumps(message)
            
            print(f"\nPublicando mensaje: {payload}")
            client.publish(MQTT_TOPIC, payload)
            
            # Esperar antes de la siguiente publicación
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Desconectar cliente
        client.loop_stop()
        client.disconnect()
        print("Desconectado del broker MQTT")

if __name__ == "__main__":
    main() 