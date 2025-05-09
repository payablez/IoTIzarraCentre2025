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

El sensor ZH03B se ha conectado a la placa LilyGO LoRa32 T3 v1.6.1 utilizando los pines correspondientes de alimentación (VCC y GND) y comunicación serie (TX al pin  2 y RX al pin 33), siguiendo el protocolo UART. Esta conexión permite que el microcontrolador ESP32 reciba los datos de calidad del aire directamente desde el sensor en modo de preguntas y respuestas (Q&A).(a que pines conectarlo)

## Uso

Al encender la estación ambiental, la placa LilyGO LoRa32 v1.6.1 inicializa todos los sensores conectados y comienza a recopilar datos ambientales, que se muestran en tiempo real en la pantalla OLED integrada. El sistema opera de forma continua, actualizando los valores a intervalos regulares.

### Sensor ZH03B – Calidad del Aire (PM2.5 / PM10)
El sensor ZH03B comienza a medir las partículas en el aire utilizando un láser interno. En condiciones promedio de una habitación cerrada, mostrará valores bajos de PM2.5 y PM10 (por ejemplo, entre 5 y 15 µg/m³), indicando una buena calidad del aire. Si se detecta humo, polvo o vapores, los valores aumentarán notablemente.

### Sensor HW-837 – Humedad del Suelo
Este sensor detecta el nivel de humedad presente en la tierra mediante su resistencia interna. En condiciones normales con tierra seca, mostrará un valor bajo en la escala analógica (por ejemplo, entre 200 y 400). Si el sensor se introduce en tierra húmeda, el valor aumentará considerablemente, indicando buen nivel de riego.

### Sensor MQ (Flying Fish) – Detección de Gases y Humo
Tras unos segundos de calentamiento, el sensor MQ comienza a detectar la presencia de gases. En una habitación sin contaminantes, los valores analógicos serán bajos (por debajo de 300). Si se expone a humo, gas de cocina o vapores, el valor aumentará rápidamente, permitiendo detectar situaciones potencialmente peligrosas.

### Potenciómetro BAOTER 3296 – Simulación de Entrada Analógica
Este componente permite modificar manualmente un valor de voltaje que se puede usar para simular una entrada analógica o probar reacciones del sistema. Al girar el tornillo, se cambia el voltaje entre 0V y 3.3V, lo que puede utilizarse, por ejemplo, para ajustar un umbral en el código.

### Sensor DHT11 – Temperatura y Humedad Ambiental
El DHT11 entrega lecturas digitales de temperatura y humedad. En interiores, bajo condiciones normales, se esperaría una temperatura entre 20 °C y 25 °C, y una humedad relativa entre 40% y 60%. Los datos se actualizan aproximadamente cada segundo en la pantalla OLED.


