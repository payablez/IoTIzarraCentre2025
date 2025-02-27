#!/usr/bin/env python3
"""
Dashboard IoT para visualización de datos en tiempo real
- Muestra datos de sensores
- Gráficos históricos
- Actualización en tiempo real vía MQTT
- Almacenamiento en SQLite
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt
import json
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
MQTT_BROKER = os.getenv('MQTT_BROKER', 'localhost')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'sensors/#')
DB_FILE = 'dashboard.db'

# Inicialización de Flask y SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Inicialización de Dash para gráficos
dash_app = Dash(__name__, server=app, url_base_pathname='/dash/')

def init_database():
    """Inicializa la base de datos SQLite"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Tabla para datos de sensores
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            sensor_id TEXT,
            type TEXT,
            value REAL
        )
    ''')
    
    conn.commit()
    conn.close()

def save_sensor_data(sensor_id, data_type, value):
    """Guarda datos del sensor en la base de datos"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO sensor_data (sensor_id, type, value)
        VALUES (?, ?, ?)
    ''', (sensor_id, data_type, value))
    
    conn.commit()
    conn.close()

# Callback MQTT
def on_message(client, userdata, message):
    """Maneja mensajes MQTT recibidos"""
    try:
        payload = json.loads(message.payload.decode())
        sensor_id = message.topic.split('/')[-1]
        
        # Guardar cada tipo de dato
        for data_type, value in payload.items():
            if isinstance(value, (int, float)):
                save_sensor_data(sensor_id, data_type, value)
                # Emitir a clientes web
                socketio.emit('sensor_update', {
                    'sensor': sensor_id,
                    'type': data_type,
                    'value': value,
                    'timestamp': datetime.now().isoformat()
                })
    except Exception as e:
        print(f"Error procesando mensaje MQTT: {e}")

# Configuración del cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

# Rutas de Flask
@app.route('/')
def home():
    """Página principal del dashboard"""
    return render_template('index.html')

@app.route('/api/sensor_data')
def get_sensor_data():
    """API para obtener datos históricos"""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query('''
        SELECT * FROM sensor_data
        WHERE timestamp >= datetime('now', '-24 hours')
        ORDER BY timestamp DESC
    ''', conn)
    conn.close()
    
    return df.to_json(orient='records')

# Layout de Dash
dash_app.layout = html.Div([
    html.H1('Gráficos de Sensores'),
    
    dcc.Dropdown(
        id='sensor-selector',
        options=[
            {'label': 'Temperatura', 'value': 'temperature'},
            {'label': 'Humedad', 'value': 'humidity'},
            {'label': 'Luz', 'value': 'light'}
        ],
        value='temperature'
    ),
    
    dcc.Graph(id='sensor-graph'),
    
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # Actualizar cada 30 segundos
        n_intervals=0
    )
])

@dash_app.callback(
    Output('sensor-graph', 'figure'),
    [Input('sensor-selector', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graph(selected_sensor, n):
    """Actualiza el gráfico con datos del sensor seleccionado"""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(f'''
        SELECT timestamp, value 
        FROM sensor_data 
        WHERE type = ?
        AND timestamp >= datetime('now', '-24 hours')
    ''', conn, params=(selected_sensor,))
    conn.close()
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    fig = px.line(df, x='timestamp', y='value',
                  title=f'Datos de {selected_sensor} últimas 24 horas')
    return fig

def main():
    """Función principal"""
    try:
        # Inicializar base de datos
        init_database()
        
        # Conectar a MQTT
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.subscribe(MQTT_TOPIC)
        mqtt_client.loop_start()
        
        # Iniciar servidor web
        socketio.run(app, host='0.0.0.0', port=8000, debug=True)
        
    except KeyboardInterrupt:
        print("\nDeteniendo servidor...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == '__main__':
    main() 