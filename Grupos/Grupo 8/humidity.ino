#include <SPI.h>
#include <LoRa.h>
#include <DHT.h>

// Definir el pin donde se conecta el sensor DHT
#define DHTPIN 4          // Puedes cambiar este pin si lo requieres
#define DHTTYPE DHT22     // Define el tipo de sensor (DHT11 o DHT22)

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Inicio del transmisor LoRa con sensor de humedad");

  // Inicializa el sensor DHT
  dht.begin();

  // Inicializa el módulo LoRa (ajusta la frecuencia según tu región, ej. 915E6 para América o 868E6 para Europa)
  if (!LoRa.begin(915E6)) {
    Serial.println("Error al iniciar LoRa");
    while (1);
  }
}

void loop() {
  // Leer los valores de humedad y temperatura del sensor DHT
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Verifica si la lectura fue exitosa
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Error al leer del sensor DHT");
    delay(2000);
    return;
  }

  // Mostrar datos por el monitor serial
  Serial.print("Humedad: ");
  Serial.print(humidity);
  Serial.print(" %\tTemperatura: ");
  Serial.print(temperature);
  Serial.println(" *C");

  // Enviar datos por LoRa
  LoRa.beginPacket();
  LoRa.print("Humedad: ");
  LoRa.print(humidity);
  LoRa.print(" %, Temp: ");
  LoRa.print(temperature);
  LoRa.print(" *C");
  LoRa.endPacket();

  delay(5000);  // Enviar cada 5 segundos
}
