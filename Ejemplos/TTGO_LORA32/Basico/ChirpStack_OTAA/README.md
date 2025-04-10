# TTGO LoRa32 - Ejemplo ChirpStack OTAA

Este ejemplo demuestra cómo conectar una placa TTGO LoRa32 a una red LoRaWAN ChirpStack utilizando OTAA con la biblioteca LMIC.
Es un ejemplo modificado de LilyGo-LoRa-Series, examples/LoRaWAN/LMIC_Library_OTTA
https://github.com/Xinyuan-LilyGO/LilyGo-LoRa-Series

## Requisitos de Hardware

- Placa TTGO LoRa32
- Cable USB para programación y alimentación

## Requisitos de Software

- Arduino IDE
- Bibliotecas necesarias:
  - LMIC (LoRaWAN MAC en C)
  - SSD1306 (para pantalla OLED)
  - U8x8lib (para pantalla OLED)

## Configuración de Pines

La placa TTGO LoRa32 utiliza los siguientes pines para la comunicación LoRa:

- SCK: GPIO5
- MISO: GPIO19
- MOSI: GPIO27
- SS: GPIO18
- RST: GPIO23
- DI0: GPIO26 (Interrupción)
- DIO1: GPIO33 (Interrupción)
- DIO2: GPIO32 (Interrupción)

## Configuración OTAA

El ejemplo utiliza los siguientes parámetros OTAA:

- APPEUI: `00 00 00 00 00 00 00 00` (LSB)
- DEVEUI: `70 B3 D5 7E D0 06 6F 8D` (LSB)
- APPKEY: `75 7F E4 B5 D0 BB 39 03 8D 6F 06 D0 7E D5 B3 70` (MSB)

**Nota:** Deberías reemplazar estos valores con tus propias credenciales de dispositivo desde tu servidor ChirpStack.

## Archivos Adicionales

Este proyecto utiliza archivos adicionales de la biblioteca LilyGo LoRa Series:

- `utilities.h`: Contiene definiciones de pines y configuraciones específicas del hardware
- `LoRaBoards.h`: Declaraciones de funciones para la inicialización del hardware
- `LoRaBoards.cpp`: Implementación de las funciones de inicialización del hardware

## Cómo Funciona

1. El dispositivo inicializa la radio LoRa y la pantalla OLED
2. Intenta unirse a la red LoRaWAN utilizando OTAA
3. Una vez unido, envía un mensaje con contador cada 120 segundos
4. La pantalla OLED muestra el estado actual y la información del mensaje

## Solución de Problemas

- Si el dispositivo no puede unirse, verifica tus credenciales OTAA
- Revisa el monitor serial para obtener información detallada de depuración
- Si el dispositivo se reinicia continuamente, verifica que todos los archivos necesarios estén presentes

## Modificaciones

Este ejemplo está basado en el ejemplo LMIC Library OTAA de LilyGo LoRa Series, adaptado para la placa TTGO LoRa32.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles. 