# Grupo 6 - Sistema de Monitoreo Ambiental

## Integrantes

- Sergio Lopez  
- Erik Montero  
- Mikel Perez  
- Ignacio Arrizabalaga

## Descripción del Proyecto

Sistema de monitoreo basado en ESP32 que integra múltiples sensores (PIR, LDR, ultrasónico) para detectar movimiento, medir niveles de luz y calcular distancias. El sistema envía los datos recopilados a un servidor web mediante solicitudes HTTP y controla automáticamente un LED basado en las condiciones del entorno.

En este proyecto utilizamos la placa **ESP32-WROOM-32D** para captar datos y enviarlos mediante peticiones HTTP hacia un servidor local donde empleamos **Node-RED** como intermediario. Node-RED recibe las solicitudes a través de una ruta específica (`/grupo6`) y redirige los datos a una base de datos **InfluxDB**, donde se almacenan con marcas de tiempo para su posterior análisis.

## Arquitectura del Sistema

### 1. Capa de Adquisición de Datos (ESP32)

- Sensores conectados al ESP32-WROOM-32D  
- Envío de datos mediante peticiones HTTP GET

### 2. Capa de Procesamiento (Node-RED)

- Recepción de solicitudes en la ruta `/grupo6`  
- Procesamiento y redirección de datos  
- Respuesta al dispositivo con estado HTTP 200

### 3. Capa de Almacenamiento (InfluxDB)

- Base de datos de series temporales  
- Almacenamiento de datos con marcas de tiempo

### 4. Capa de Visualización (Grafana)

- Paneles personalizados para visualización en tiempo real  
- Consultas a InfluxDB para representar gráficamente los datos  
- Monitoreo de variables de entorno (luz, movimiento, distancia)

## Estructura del Proyecto

- Chirpstack/ Contiene los archivos de codificación/decodificación para ChirpStack
- Aplicacion/ Contiene el código de la aplicación principal
- main.ino Código principal para el ESP32


## Hardware Utilizado

- ESP32-WROOM-32D Development Board  
- Sensor PIR (movimiento)  
- Sensor LDR (luz)  
- Sensor ultrasónico HC-SR04 (distancia)  
- LED

## Conexiones de Hardware

- Sensor PIR → pin 19  
- LED → pin 21  
- Sensor ultrasónico:  
  - TRIGGER → pin 17  
  - ECHO → pin 16  
- Sensor LDR → pin 34

## Instalación y Configuración

### Requisitos Previos

- Arduino IDE instalado  
- Biblioteca ESP32 para Arduino  
- Bibliotecas adicionales:  
  - WiFi  
  - HTTPClient  
  - esp_task_wdt

### Configuración WiFi

Asegúrate de configurar las credenciales correctamente en el archivo `main.ino`:

```cpp
// Wi-Fi credentials
const char* ssid = "IzarraCentre";       // (Wi-Fi name)
const char* password = "Enter Password"; // (Wi-Fi password)
```

