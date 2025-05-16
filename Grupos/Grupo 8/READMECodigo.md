# Control de Humedad y Temperatura con Sistema de Riego

Este proyecto implementa un nodo IoT basado en ESP32 que lee tres sensores (temperatura analógica, humedad analógica y tensión de batería) y un sensor DHT11 digital, controla un relé en función de la humedad y envía periódicamente los datos en formato JSON a un servidor HTTP. Además muestra el estado y lecturas en un display OLED SSD1306.

## Características

- Lectura de:
  - **Temperatura analógica** (LM35 o sensor similar).
  - **Humedad analógica** (salida 0–3.3 V → 0–100 %).
  - **Tensión de batería** (con divisor 1:2).
  - **Sensor DHT11** (temperatura y humedad digital, sólo para estado “online”).
- Control de **relé** según humedad analógica (activo si < 20 %).
- Conexión Wi-Fi a red local.
- Envío HTTP POST con JSON al servidor configurado.
- Visualización en OLED SSD1306:
  - Estado de conexión Wi-Fi.
  - Respuesta del servidor.
  - Lecturas de sensores y estado DHT11.
- Ciclo de muestreo cada 60 s.

## Hardware

- **ESP32** (Módulo con ADC1 y soporte I²C).
- **Sensor de temperatura analógico** (por ejemplo LM35).
- **Sensor de humedad analógico** (salida 0–3.3 V).
- **Sensor DHT11**.
- **Relé** (para activar/desactivar un actuador).
- **Display OLED SSD1306** I²C (128×64).
- Resistencias para divisor de tensión (1:2).
- Cables y protoboard o PCB.

## Esquema de conexiones

| Señal / Pin           | ESP32        | Componente         |
|-----------------------|--------------|--------------------|
| Temperatura analógica | GPIO 39 (ADC1_3) | LM35              |
| Humedad analógica     | GPIO 35 (ADC1_7) | Sensor analógico  |
| Voltaje batería       | GPIO 32 (ADC1_4) | Divisor 1:2       |
| DHT11 DATA            | GPIO 4       | DHT11              |
| Relé                  | GPIO 26      | Módulo relé        |
| OLED SCL              | GPIO 22 (I²C) | SSD1306 SCL       |
| OLED SDA              | GPIO 21 (I²C) | SSD1306 SDA       |
| GND, 3V3              | GND, 3.3 V   | Alimentación       |

> **Nota:** Ajusta los pines I²C si tu placa ESP32 usa otros.

## Requisitos de software

- **Arduino IDE** o **PlatformIO**.
- Librerías:
  - `WiFi.h` (ESP32 core).
  - `HTTPClient.h`.
  - `ArduinoJson` (v6.x).
  - `Adafruit_GFX` y `Adafruit_SSD1306`.
  - `DHT sensor library` y `DHT.h`.

Instala las librerías desde el Gestor de Librerías del IDE o `platformio.ini`.

## Configuración

1. Clona o copia este repositorio.
2. En el sketch, edita:
   ```cpp
    const char* ssid       = "IzarraCentre";
    const char* password   = "";
    const char* serverName = "http://formacioniot2025.devlon.es/grupo8";
    ```
 ## Arduino Codigo
```ino
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include <DHT.h>
 
// Definimos el pin digital donde se conecta el sensor
#define DHTPIN 36
// Dependiendo del tipo de sensor
#define DHTTYPE DHT11
 
// Inicializamos el sensor DHT11
DHT dht(DHTPIN, DHTTYPE);

// ——— Configuración Wi-Fi y servidor ———
const char* ssid       = "IzarraCentre";
const char* password   = "";
const char* serverName = "http://formacioniot2025.devlon.es/grupo8";

// ——— OLED I²C ———
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// ——— Pines de sensores ———
const int tempPin   = 36;  // ADC1_CH0: temperatura analógica (0–3.3V)
const int humPin    = 39;  // ADC1_CH3: humedad analógica   (0–3.3V)
const int relayPin  = 26;  // Salida digital para el relé

// ——— Parámetros ADC ———
const float voltageRef = 3.3;
const int   resolution = 4095;

void setup() {
  Serial.begin(115200);

  // OLED de bienvenida
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("Error OLED");
    while (true);
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("Temp->GPIO36");
  display.println("Hum->GPIO39");
  display.println("Relay->GPIO26");
  display.println("Voltaje->USB");
  display.display();
  delay(3000);

  // Conexión Wi-Fi
  display.clearDisplay();
  display.setCursor(0,0);
  display.println("Conectando WiFi...");
  display.display();
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  display.clearDisplay();
  display.setCursor(0,0);
  display.println("WiFi conectado");
  display.display();

  // Configura relé
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);

  dht.begin();

}

void loop() {
  // Lee temperatura analógica
  // int rawT = analogRead(tempPin);
  // float vT = rawT * voltageRef / resolution;
  // float temperature = vT * 100.0; // e.g., LM35: 10 mV/°C
  float temperature = dht.readTemperature();


  // Lee humedad analógica
  int rawH = analogRead(humPin);
  float vH = rawH * voltageRef / resolution;
  float humidity = vH * 100.0;    // 0–3.3V → 0–100%

  // Voltaje desde USB (5 V fijo)
  float voltage = 5.0;

  // Control del relé si humedad < 20%
  digitalWrite(relayPin, humidity < 20.0 ? HIGH : LOW);

  // Construye JSON
  StaticJsonDocument<200> doc;
  doc["temperatura"] = temperature;
  doc["humedad"]     = humidity;
  doc["voltaje"]     = voltage;

  String jsonData;
  serializeJson(doc, jsonData);
  Serial.println("JSON → " + jsonData);

  // Envío HTTP POST
  display.clearDisplay();
  display.setCursor(0,0);
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type","application/json");
    int code = http.POST(jsonData);
    http.end();
    display.println(code>0 ? "Enviado OK" : "Error envio");
  } else {
    display.println("WiFi desconectado");
  }

  // Muestra datos en OLED
  display.println();
  display.printf("Temp: %.2f C\n", temperature);
  display.printf("Hum:  %.2f %%\n", humidity);
  display.printf("Vbat: %.2f V\n", voltage);
  display.display();

  delay(60000);
}
```
