#!/usr/bin/env python3
"""
Registrador de datos de sensores en SQLite
- Lee datos de temperatura y humedad del DHT11
- Almacena los datos en una base de datos SQLite
- Permite consultar datos históricos
"""

import Adafruit_DHT
import RPi.GPIO as GPIO
import sqlite3
from datetime import datetime
import time
import pandas as pd
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = int(os.getenv('DHT_PIN', 4))
DB_FILE = 'sensors.db'
INTERVAL = int(os.getenv('INTERVAL', 300))  # 5 minutos por defecto

def init_database():
    """Inicializa la base de datos SQLite"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Tabla para datos de sensores
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            humidity REAL
        )
    ''')
    
    # Tabla para estadísticas diarias
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_stats (
            date DATE PRIMARY KEY,
            avg_temp REAL,
            min_temp REAL,
            max_temp REAL,
            avg_humidity REAL,
            min_humidity REAL,
            max_humidity REAL
        )
    ''')
    
    conn.commit()
    conn.close()

def save_reading(temperature, humidity):
    """Guarda una lectura en la base de datos"""
    if temperature is not None and humidity is not None:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO sensor_readings (temperature, humidity)
            VALUES (?, ?)
        ''', (temperature, humidity))
        
        conn.commit()
        conn.close()
        return True
    return False

def update_daily_stats():
    """Actualiza las estadísticas diarias"""
    conn = sqlite3.connect(DB_FILE)
    
    # Usar pandas para calcular estadísticas
    df = pd.read_sql_query('''
        SELECT 
            date(timestamp) as date,
            AVG(temperature) as avg_temp,
            MIN(temperature) as min_temp,
            MAX(temperature) as max_temp,
            AVG(humidity) as avg_humidity,
            MIN(humidity) as min_humidity,
            MAX(humidity) as max_humidity
        FROM sensor_readings
        WHERE date(timestamp) = date('now')
        GROUP BY date(timestamp)
    ''', conn)
    
    if not df.empty:
        # Actualizar o insertar estadísticas
        for _, row in df.iterrows():
            c = conn.cursor()
            c.execute('''
                INSERT OR REPLACE INTO daily_stats
                (date, avg_temp, min_temp, max_temp, avg_humidity, min_humidity, max_humidity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', tuple(row))
    
    conn.commit()
    conn.close()

def get_daily_stats(days=7):
    """Obtiene estadísticas de los últimos días"""
    conn = sqlite3.connect(DB_FILE)
    
    df = pd.read_sql_query('''
        SELECT *
        FROM daily_stats
        WHERE date >= date('now', ?)
        ORDER BY date DESC
    ''', conn, params=(f'-{days} days',))
    
    conn.close()
    return df

def main():
    """Función principal"""
    print("Iniciando registrador de sensores...")
    
    try:
        # Inicializar base de datos
        init_database()
        
        while True:
            # Leer sensor
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            
            # Guardar lectura
            if save_reading(temperature, humidity):
                print(f"Lectura guardada - Temp: {temperature:.1f}°C, Hum: {humidity:.1f}%")
                # Actualizar estadísticas
                update_daily_stats()
            else:
                print("Error al leer el sensor")
            
            # Esperar para la siguiente lectura
            time.sleep(INTERVAL)
            
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main() 