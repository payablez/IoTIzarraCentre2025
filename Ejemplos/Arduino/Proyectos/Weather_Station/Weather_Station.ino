/*
 * Estación Meteorológica con Arduino
 * 
 * Este proyecto implementa una estación meteorológica completa que:
 * - Mide temperatura y humedad con DHT11
 * - Mide presión atmosférica con BMP180
 * - Mide intensidad de luz con LDR
 * - Detecta lluvia con sensor FC-37
 * - Muestra datos en pantalla LCD
 * - Envía datos por MQTT
 * - Guarda datos en tarjeta SD
 * 
 * Conexiones:
 * - DHT11: Pin 2
 * - BMP180: I2C (A4/A5)
 * - LDR: A0
 * - Sensor lluvia: A1
 * - LCD: I2C (A4/A5)
 * - SD Card:
 *   - MOSI: Pin 11
 *   - MISO: Pin 12
 *   - CLK: Pin 13
 *   - CS: Pin 10
 * - LED Estado: Pin 8
 * 
 * Requiere las siguientes bibliotecas:
 * - DHT sensor library
 * - Adafruit BMP085 library
 * - LiquidCrystal I2C
 * - SD
 * - ArduinoJson
 * - ESP8266WiFi
 * - PubSubClient
 */

#include <DHT.h>
#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <LiquidCrystal_I2C.h>
#include <SD.h>
#include <SPI.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// Configuración de pines
#define DHTPIN 2
#define DHTTYPE DHT11
#define LDR_PIN A0
#define RAIN_PIN A1
#define LED_PIN 8
#define SD_CS_PIN 10

// Configuración de red
const char* ssid = "TU_SSID";
const char* password = "TU_PASSWORD";
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "weather/station1";

// Intervalos de tiempo (ms)
const long SENSOR_INTERVAL = 2000;    // Lectura de sensores
const long DISPLAY_INTERVAL = 1000;   // Actualización LCD
const long MQTT_INTERVAL = 5000;      // Publicación MQTT
const long STORAGE_INTERVAL = 60000;  // Almacenamiento SD

// Variables globales
unsigned long lastSensorRead = 0;
unsigned long lastDisplay = 0;
unsigned long lastMqttPublish = 0;
unsigned long lastStorage = 0;

// Objetos para sensores y comunicación
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085 bmp;
LiquidCrystal_I2C lcd(0x27, 16, 2);
WiFiClient espClient;
PubSubClient client(espClient);

// Estructura para datos meteorológicos
struct WeatherData {
    float temperature;
    float humidity;
    float pressure;
    int light;
    bool isRaining;
    unsigned long timestamp;
} weatherData;

void setup() {
    // Iniciar comunicación serial
    Serial.begin(115200);
    Serial.println("\nIniciando Estación Meteorológica...");
    
    // Configurar pines
    pinMode(LED_PIN, OUTPUT);
    pinMode(LDR_PIN, INPUT);
    pinMode(RAIN_PIN, INPUT);
    
    // Iniciar sensores
    dht.begin();
    if (!bmp.begin()) {
        Serial.println("Error: BMP180 no encontrado!");
        while (1);
    }
    
    // Iniciar LCD
    lcd.init();
    lcd.backlight();
    lcd.print("Iniciando...");
    
    // Iniciar SD
    if (!SD.begin(SD_CS_PIN)) {
        Serial.println("Error: SD Card no encontrada!");
        while (1);
    }
    
    // Conectar a WiFi
    setup_wifi();
    
    // Configurar MQTT
    client.setServer(mqtt_server, mqtt_port);
    
    Serial.println("Inicialización completada!");
    lcd.clear();
}

void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Conectando a ");
    Serial.println(ssid);
    
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("");
    Serial.println("WiFi conectado");
    Serial.println("IP: " + WiFi.localIP().toString());
}

// Función para leer todos los sensores y actualizar los datos
void readSensors() {
    // Guardar el momento actual
    weatherData.timestamp = millis();
    
    // Leer temperatura y humedad del sensor DHT11
    weatherData.temperature = dht.readTemperature();
    weatherData.humidity = dht.readHumidity();
    
    // Leer presión atmosférica del BMP180 y convertir a hectopascales
    weatherData.pressure = bmp.readPressure() / 100.0F;  // hPa
    
    // Leer sensor de luz y convertir a porcentaje (0-100%)
    int ldr_value = analogRead(LDR_PIN);
    weatherData.light = map(ldr_value, 0, 1023, 0, 100);
    
    // Leer sensor de lluvia (true si detecta lluvia)
    weatherData.isRaining = analogRead(RAIN_PIN) < 500;
}

// Función para mostrar los datos en la pantalla LCD
void updateDisplay() {
    // Limpiar la pantalla
    lcd.clear();
    
    // Primera línea: Temperatura, Humedad y Estado de lluvia
    lcd.setCursor(0, 0);
    lcd.print(String(weatherData.temperature, 1));  // 1 decimal
    lcd.print("C ");
    lcd.print(String(weatherData.humidity, 0));     // Sin decimales
    lcd.print("% ");
    lcd.print(weatherData.isRaining ? "LLUVIA" : "SECO");
    
    // Segunda línea: Presión y Luz
    lcd.setCursor(0, 1);
    lcd.print(String(weatherData.pressure, 0));     // Sin decimales
    lcd.print("hPa ");
    lcd.print("L:");
    lcd.print(String(weatherData.light));
    lcd.print("%");
}

// Función para publicar datos en MQTT
void publishMQTT() {
    // Verificar conexión MQTT
    if (!client.connected()) {
        reconnectMQTT();
    }
    
    // Crear objeto JSON para los datos
    StaticJsonDocument<200> doc;
    doc["temp"] = weatherData.temperature;
    doc["hum"] = weatherData.humidity;
    doc["press"] = weatherData.pressure;
    doc["light"] = weatherData.light;
    doc["rain"] = weatherData.isRaining;
    
    // Convertir a string y publicar
    char buffer[200];
    serializeJson(doc, buffer);
    client.publish(mqtt_topic, buffer);
}

// Función para guardar datos en la tarjeta SD
void saveToSD() {
    // Abrir archivo en modo escritura
    File dataFile = SD.open("weather.csv", FILE_WRITE);
    
    if (dataFile) {
        // Escribir datos separados por comas
        dataFile.print(weatherData.timestamp);
        dataFile.print(",");
        dataFile.print(weatherData.temperature);
        dataFile.print(",");
        dataFile.print(weatherData.humidity);
        dataFile.print(",");
        dataFile.print(weatherData.pressure);
        dataFile.print(",");
        dataFile.print(weatherData.light);
        dataFile.print(",");
        dataFile.println(weatherData.isRaining);
        
        // Cerrar archivo
        dataFile.close();
    }
}

// Función para reconectar al servidor MQTT
void reconnectMQTT() {
    // Intentar hasta conectar
    while (!client.connected()) {
        // Intentar conexión
        if (client.connect("ArduinoWeather")) {
            Serial.println("Conectado a MQTT");
        } else {
            Serial.print("Error MQTT, rc=");
            Serial.println(client.state());
            // Esperar 5 segundos antes de reintentar
            delay(5000);
        }
    }
}

void loop() {
    // Obtener tiempo actual
    unsigned long currentMillis = millis();
    
    // Leer sensores cada SENSOR_INTERVAL milisegundos
    if (currentMillis - lastSensorRead >= SENSOR_INTERVAL) {
        lastSensorRead = currentMillis;
        readSensors();
        // Cambiar estado del LED para indicar actividad
        digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    }
    
    // Actualizar pantalla cada DISPLAY_INTERVAL milisegundos
    if (currentMillis - lastDisplay >= DISPLAY_INTERVAL) {
        lastDisplay = currentMillis;
        updateDisplay();
    }
    
    // Publicar datos MQTT cada MQTT_INTERVAL milisegundos
    if (currentMillis - lastMqttPublish >= MQTT_INTERVAL) {
        lastMqttPublish = currentMillis;
        publishMQTT();
    }
    
    // Guardar datos en SD cada STORAGE_INTERVAL milisegundos
    if (currentMillis - lastStorage >= STORAGE_INTERVAL) {
        lastStorage = currentMillis;
        saveToSD();
    }
    
    // Mantener la conexión MQTT activa
    client.loop();
} 