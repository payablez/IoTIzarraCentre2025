# Grupo 7

## Integrantes
- Gaizka Vecino
- Ibai Perez
- Aritz Arruabarrena
- Aner Rodriguez

## Descripción del Proyecto

El objetivo de este proyecto es visualizar en la pantalla OLED integrada de la placa LilyGO LoRa32 v1.6.1 los datos de distintos sensores ambientales. Para ello, se ha realizado la conexión e integración de varios sensores que permiten obtener información sobre el entorno, como la calidad del aire, humedad del suelo, presencia de gases, temperatura y humedad del ambiente.

Este proyecto está pensado como una estación ambiental portátil y de bajo consumo, capaz de mostrar los valores directamente en su pantalla sin necesidad de conexión a otro dispositivo externo. La placa seleccionada, la LilyGO LoRa32 v1.6.1, combina conectividad LoRa, microcontrolador ESP32 y pantalla OLED, facilitando así tanto la adquisición como la visualización de los datos.

### 1. Placa Base

**Modelo:** LilyGO LoRa32 v1.6.1  
**Pantalla OLED integrada (I2C)**  
Esta placa cuenta con un microcontrolador ESP32 y una pantalla OLED incorporada que permite mostrar los datos recogidos por los sensores en tiempo real. Su conectividad LoRa puede aprovecharse en futuras ampliaciones para transmitir los datos de forma remota.

### 2. Sensores Utilizados

#### 2.1 Sensor ZH03B  
**Objetivo:** Medir la calidad del aire (PM2.5 / PM10)  
**Interfaz:** UART (modo Q&A)  
Este sensor láser permite medir partículas en suspensión en el aire, como polvo fino y grueso, lo cual es clave para conocer el nivel de contaminación ambiental.

#### 2.2 Sensor HW-837  
**Objetivo:** Medir la humedad del suelo  
**Interfaz:** Analógica  
Se utiliza para detectar el nivel de humedad en el suelo. Es especialmente útil en proyectos relacionados con agricultura o sistemas de riego automático.

#### 2.3 Sensor MQ (Flying Fish)  
**Objetivo:** Detectar gases o humo  
**Interfaz:** Analógica  
Este sensor es capaz de detectar la presencia de gases peligrosos o humo, lo que permite usarlo como un sistema de alerta o monitoreo ambiental.

#### 2.4 Potenciómetro BAOTER 3296  
**Objetivo:** Regular y simular niveles analógicos de referencia  
**Interfaz:** Analógica  
El potenciómetro se utiliza en este proyecto para simular distintos niveles de señal analógica, ideal para pruebas de calibración o ajustes manuales de umbrales.

#### 2.5 Sensor DHT11  
**Objetivo:** Medir temperatura y humedad ambiental  
**Interfaz:** Digital (1-Wire)  
Este sensor compacto proporciona información básica sobre temperatura y humedad, dos parámetros esenciales en cualquier monitoreo ambiental.

## Estructura
- `Chirpstack/`: Contiene los archivos de codificación/decodificación para ChirpStack
- `Aplicacion/`: Contiene el código de la aplicación principal

## Instrucciones de Instalación
[Instrucciones específicas de instalación]

## Uso
[Instrucciones de uso] 
