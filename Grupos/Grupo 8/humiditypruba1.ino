#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

// Configuración de pantalla OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Configuración del sensor DHT
#define DHTPIN 4  // Pin donde está conectado el DHT
#define DHTTYPE DHT22  // Cambiar a DHT11 si usas ese modelo
DHT dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(115200);
    dht.begin();

    // Inicializar pantalla OLED
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println("No se encontró pantalla OLED");
        while (1);
    }

    display.clearDisplay();
    display.setTextSize(1,3);
    display.setTextColor(WHITE);
    display.setCursor(0, 0);
    display.println("Inicializando...");
    display.display();
    delay(2000);
}

void loop() {
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
        Serial.println("Error leyendo el sensor DHT");
        return;
    }

    // Mostrar en la pantalla OLED
    display.clearDisplay();
    display.setTextSize(1,4);
    display.setCursor(0, 10);
    display.println("Temp: " + String(t) + "C");
    display.setCursor(0, 35);
    display.println("Humedad: " + String(h) + "%");
    display.display();

    // Mostrar en el puerto serie
    Serial.print("Temperatura: ");
    Serial.print(t);
    Serial.print(" °C  |  Humedad: ");
    Serial.print(h);
    Serial.println(" %");

    delay(2000);
}