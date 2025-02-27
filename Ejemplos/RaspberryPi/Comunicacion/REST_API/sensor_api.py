#!/usr/bin/env python3
"""
API REST para sensores
- Expone endpoints para leer y escribir datos de sensores
- Autenticación JWT
- Documentación Swagger
- Almacenamiento en SQLite
"""

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_swagger_ui import get_swaggerui_blueprint
from marshmallow import Schema, fields
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

# Inicialización
api = Api(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Configuración Swagger
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sensor API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Modelos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Schemas
class SensorReadingSchema(Schema):
    id = fields.Int(dump_only=True)
    sensor_id = fields.Str(required=True)
    type = fields.Str(required=True)
    value = fields.Float(required=True)
    timestamp = fields.DateTime(dump_only=True)

sensor_schema = SensorReadingSchema()
sensors_schema = SensorReadingSchema(many=True)

# Recursos API
class AuthResource(Resource):
    def post(self):
        """Login y obtención de token JWT"""
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # En producción usar hash
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

class SensorResource(Resource):
    @jwt_required()
    def get(self, sensor_id=None):
        """Obtiene lecturas de sensores"""
        if sensor_id:
            readings = SensorReading.query.filter_by(sensor_id=sensor_id).all()
        else:
            readings = SensorReading.query.all()
        return sensors_schema.dump(readings)
    
    @jwt_required()
    def post(self):
        """Registra una nueva lectura de sensor"""
        json_data = request.get_json()
        try:
            data = sensor_schema.load(json_data)
            reading = SensorReading(
                sensor_id=data['sensor_id'],
                type=data['type'],
                value=data['value']
            )
            db.session.add(reading)
            db.session.commit()
            return sensor_schema.dump(reading), 201
        except Exception as e:
            return {'message': str(e)}, 400

class SensorStatsResource(Resource):
    @jwt_required()
    def get(self, sensor_id):
        """Obtiene estadísticas de un sensor"""
        readings = SensorReading.query.filter_by(sensor_id=sensor_id).all()
        if not readings:
            return {'message': 'No readings found'}, 404
        
        values = [r.value for r in readings]
        return {
            'sensor_id': sensor_id,
            'count': len(values),
            'average': sum(values) / len(values),
            'min': min(values),
            'max': max(values)
        }

# Rutas API
api.add_resource(AuthResource, '/api/auth')
api.add_resource(SensorResource, '/api/sensors', '/api/sensors/<string:sensor_id>')
api.add_resource(SensorStatsResource, '/api/sensors/<string:sensor_id>/stats')

@app.before_first_request
def create_tables():
    """Crea las tablas de la base de datos"""
    db.create_all()
    
    # Crear usuario de prueba si no existe
    if not User.query.filter_by(username='admin').first():
        user = User(username='admin', password='admin')  # En producción usar hash
        db.session.add(user)
        db.session.commit()

def main():
    """Función principal"""
    try:
        # Iniciar servidor
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()

"""
Ejemplos de uso de la API:

1. Obtener datos de sensores:
   curl http://localhost:5000/api/v1/sensors

2. Obtener estado del LED:
   curl http://localhost:5000/api/v1/led

3. Encender LED:
   curl -X POST -H "Content-Type: application/json" \
        -d '{"state": true}' \
        http://localhost:5000/api/v1/led

4. Apagar LED:
   curl -X POST -H "Content-Type: application/json" \
        -d '{"state": false}' \
        http://localhost:5000/api/v1/led

5. Obtener estado del sistema:
   curl http://localhost:5000/api/v1/status
""" 