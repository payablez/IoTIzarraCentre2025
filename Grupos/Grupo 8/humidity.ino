#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Configuración del Wi-Fi
const char* ssid     = "IzarraCentre";  // Tu SSID
const char* password = "";              // Tu contraseña WiFi

// Dirección del servidor
const char* serverName = "http://formacioniot2025.devlon.es/grupo8";

// Configuración de la pantalla OLED
#define SCREEN_WIDTH  128
#define SCREEN_HEIGHT  64
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Pines donde se conectan los sensores (ADC1)
const int temperaturePin = 21;  // Sensor de temperatura
const int humidityPin    = 36;  // Sensor de humedad
const int voltagePin     = 35;  // Sensor de voltaje

// Parámetros para conversión (ajustar según tu sensor)
const float voltageReference = 3.3;   // Voltaje de referencia del ADC
const int   adcResolution    = 4095;  // Resolución del ADC del ESP32 (12 bits)

void setup() {
  Serial.begin(115200);

  // Inicializar pantalla OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("Fallo inicializando la pantalla OLED"));
    while (true);  // Detener ejecución
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("Conectando WiFi...");
  display.display();

  // Conectar a Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("Conectando WiFi...");
    display.display();
  }

  Serial.println("WiFi conectado");
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("WiFi conectado");
  display.display();
}

void loop() {
  // Leer valores crudos de los sensores
  int tempRaw = analogRead(temperaturePin);
  int humRaw  = analogRead(humidityPin);
  int voltRaw = analogRead(voltagePin);

  // Convertir el valor crudo en unidades físicas
  float temperature = (tempRaw * voltageReference / adcResolution) * 100.0; // LM35: 10mV/°C
  float humidity    = (humRaw  * voltageReference / adcResolution) * 100.0; // 0–100% en 0–3.3V
  float voltage     = (voltRaw * voltageReference / adcResolution) * 2.0;   // divisor 1:2

  // Crear objeto JSON con los datos
  StaticJsonDocument<200> doc;
  doc["temperatura"] = temperature;
  doc["humedad"]     = humidity;
  doc["voltaje"]     = voltage;

  String jsonData;
  serializeJson(doc, jsonData);
  Serial.println("JSON enviado:");
  Serial.println(jsonData);

  // Enviar el JSON al servidor vía HTTP POST
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(jsonData);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Código HTTP: ");
      Serial.println(httpResponseCode);
      Serial.print("Respuesta del servidor: ");
      Serial.println(response);

      // Mostrar JSON y voltaje en pantalla OLED
      display.clearDisplay();
      display.setTextSize(1);
      display.setCursor(0, 0);
      display.println(jsonData);
      display.println(); // Línea en blanco
      display.print("Voltaje: ");
      display.print(voltage, 2);
      display.println(" V");
      display.display();

    } else {
      Serial.print("Error HTTP: ");
      Serial.println(httpResponseCode);

      // Mostrar error y voltaje en pantalla OLED
      display.clearDisplay();
      display.setTextSize(1);
      display.setCursor(0, 0);
      display.println("Error al enviar");
      display.print("Voltaje: ");
      display.print(voltage, 2);
      display.println(" V");
      display.display();
    }
    http.end();

  } else {
    Serial.println("WiFi desconectado");
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.println("WiFi desconectado");
    display.display();
  }

  delay(60000); // Espera 60 segundos antes de volver a enviar
}