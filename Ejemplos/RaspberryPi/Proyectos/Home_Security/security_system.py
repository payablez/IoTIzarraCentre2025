#!/usr/bin/env python3
"""
Sistema de Seguridad para el Hogar con Raspberry Pi

Este proyecto implementa un sistema de seguridad que incluye:
- Detección de movimiento con sensor PIR
- Captura de imágenes con cámara
- Notificaciones por correo electrónico
- Almacenamiento de eventos en base de datos
- Interfaz web para monitoreo
- Control de alarma sonora
- LED de estado
"""

import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import threading
import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, jsonify, request
import os
import json

# Configuración de pines
PIR_PIN = 17
LED_PIN = 18
BUZZER_PIN = 27

# Configuración de correo
EMAIL_FROM = "tu_correo@gmail.com"
EMAIL_TO = "destino@email.com"
EMAIL_PASSWORD = "tu_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Configuración de la aplicación
IMAGES_DIR = "static/images"
DB_FILE = "security.db"
app = Flask(__name__)

# Variables globales
system_armed = False
motion_detected = False
last_detection = None
camera = None

def setup():
    """Configura el hardware y la base de datos"""
    # Configurar GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    
    # Crear directorio para imágenes
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    # Inicializar base de datos
    init_database()
    
    # Inicializar cámara
    global camera
    camera = PiCamera()
    camera.resolution = (1280, 720)
    
    print("Sistema inicializado")

def init_database():
    """Inicializa la base de datos SQLite"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Tabla de eventos
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            type TEXT,
            description TEXT,
            image_path TEXT
        )
    ''')
    
    # Tabla de configuración
    c.execute('''
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def log_event(event_type, description, image_path=None):
    """Registra un evento en la base de datos"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO events (type, description, image_path)
        VALUES (?, ?, ?)
    ''', (event_type, description, image_path))
    
    conn.commit()
    conn.close()

def capture_image():
    """Captura una imagen con la cámara"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"{IMAGES_DIR}/motion_{timestamp}.jpg"
    
    camera.capture(image_path)
    return image_path

def send_email_alert(image_path):
    """Envía una alerta por correo electrónico"""
    msg = MIMEMultipart()
    msg['Subject'] = '¡Alerta de Seguridad!'
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    
    text = MIMEText("Se ha detectado movimiento en tu casa.")
    msg.attach(text)
    
    with open(image_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
        msg.attach(img)
    
    # Enviar correo
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

def apagar_alarma():
    """Apaga el buzzer de la alarma"""
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def apagar_led():
    """Apaga el LED de estado"""
    GPIO.output(LED_PIN, GPIO.LOW)

def handle_motion(channel):
    """Se ejecuta cuando el sensor de movimiento detecta algo"""
    global motion_detected, last_detection
    
    # Si el sistema no está armado, no hacer nada
    if not system_armed:
        return
    
    motion_detected = True
    last_detection = datetime.now()
    
    # Capturar imagen
    image_path = capture_image()
    
    # Activar alarma y LED
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    GPIO.output(LED_PIN, GPIO.HIGH)
    
    # Registrar el evento en la base de datos
    log_event("motion", "Movimiento detectado", image_path)
    
    # Enviar alerta por correo
    try:
        send_email_alert(image_path)
    except Exception as e:
        print(f"Error al enviar correo: {e}")
    
    # Programar el apagado de la alarma y LED después de 5 segundos
    threading.Timer(5.0, apagar_alarma).start()
    threading.Timer(5.0, apagar_led).start()
    
    motion_detected = False

# Rutas de la aplicación web
@app.route('/')
def home():
    """Página principal"""
    return render_template('index.html', armed=system_armed)

@app.route('/api/status')
def get_status():
    """Estado del sistema"""
    return jsonify({
        'armed': system_armed,
        'motion_detected': motion_detected,
        'last_detection': last_detection.isoformat() if last_detection else None
    })

@app.route('/api/events')
def get_events():
    """Obtiene los últimos eventos"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute('''
        SELECT timestamp, type, description, image_path
        FROM events
        ORDER BY timestamp DESC
        LIMIT 10
    ''')
    
    events = [{
        'timestamp': row[0],
        'type': row[1],
        'description': row[2],
        'image': row[3]
    } for row in c.fetchall()]
    
    conn.close()
    return jsonify(events)

@app.route('/api/arm', methods=['POST'])
def arm_system():
    """Activa/desactiva el sistema"""
    global system_armed
    
    data = request.get_json()
    system_armed = data.get('armed', False)
    
    GPIO.output(LED_PIN, GPIO.HIGH if system_armed else GPIO.LOW)
    log_event("system", "Sistema " + ("armado" if system_armed else "desarmado"))
    
    return jsonify({'success': True, 'armed': system_armed})

def cleanup():
    """Limpia los recursos"""
    GPIO.cleanup()
    if camera:
        camera.close()

def main():
    """Función principal"""
    try:
        setup()
        
        # Configurar detección de movimiento
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=handle_motion)
        
        # Iniciar servidor web
        app.run(host='0.0.0.0', port=8000)
        
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cleanup()

if __name__ == '__main__':
    main() 