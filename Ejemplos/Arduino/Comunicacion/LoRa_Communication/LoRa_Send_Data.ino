/*
 * Ejemplo de envío de datos usando LoRa
 * 
 * Conexiones para módulo LoRa Ra-02:
 * - NSS/CS -> 10
 * - RESET -> 9
 * - DIO0 -> 2
 * - MOSI -> 11
 * - MISO -> 12
 * - SCK -> 13
 * 
 * Requiere:
 * - LoRa library de Sandeep Mistry
 */

#include <SPI.h>
#include <LoRa.h>

// Pines para LoRa
#define SS_PIN 10
#define RST_PIN 9
#define DIO0_PIN 2

// Contador de mensajes
int counter = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("Iniciando LoRa Sender");

  // Configurar pines
  LoRa.setPins(SS_PIN, RST_PIN, DIO0_PIN);

  // Iniciar LoRa a 433 MHz
  if (!LoRa.begin(433E6)) {
    Serial.println("Error iniciando LoRa!");
    while (1);
  }

  // Configurar parámetros LoRa
  LoRa.setTxPower(20); // Máxima potencia
  LoRa.setSpreadingFactor(7); // Rango: 6-12, menor = más rápido
  LoRa.setSignalBandwidth(125E3); // 125 kHz
  LoRa.setCodingRate4(5); // 4/5 coding rate

  Serial.println("LoRa inicializado correctamente!");
}

void loop() {
  Serial.print("Enviando paquete: ");
  Serial.println(counter);

  // Comenzar paquete LoRa
  LoRa.beginPacket();
  
  // Datos a enviar
  String message = "Mensaje #" + String(counter);
  LoRa.print(message);
  
  // Finalizar y enviar paquete
  LoRa.endPacket();

  counter++;

  delay(5000); // Esperar 5 segundos entre envíos
} 