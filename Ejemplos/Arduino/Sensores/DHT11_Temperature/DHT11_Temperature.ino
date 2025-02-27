/*
 * Ejemplo de lectura de temperatura y humedad con sensor DHT11
 * 
 * Conexiones:
 * - Pin de datos del DHT11 -> Pin Digital 2
 * - VCC del DHT11 -> 5V
 * - GND del DHT11 -> GND
 * 
 * Requiere la biblioteca DHT sensor library de Adafruit
 */

#include <DHT.h>

#define DHTPIN 2          // Pin donde está conectado el sensor
#define DHTTYPE DHT11     // Tipo de sensor DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  
  Serial.println("Iniciando sensor DHT11...");
  delay(2000); // Espera para que el sensor se estabilice
}

void loop() {
  // Lectura de humedad
  float humedad = dht.readHumidity();
  // Lectura de temperatura en Celsius
  float temperatura = dht.readTemperature();

  // Verifica si las lecturas son válidas
  if (isnan(humedad) || isnan(temperatura)) {
    Serial.println("Error al leer el sensor DHT11!");
    return;
  }

  // Imprime los resultados
  Serial.print("Humedad: ");
  Serial.print(humedad);
  Serial.print("%  Temperatura: ");
  Serial.print(temperatura);
  Serial.println("°C");

  delay(2000); // Espera 2 segundos entre lecturas
} 