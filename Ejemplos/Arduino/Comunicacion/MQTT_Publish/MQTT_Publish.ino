/*
 * Ejemplo de publicación MQTT usando ESP8266
 * 
 * Conexiones:
 * - ESP8266 conectado via USB
 * 
 * Requiere:
 * - ESP8266WiFi library
 * - PubSubClient library
 */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Configuración de WiFi
const char* ssid = "TU_SSID";
const char* password = "TU_PASSWORD";

// Configuración de MQTT
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "iot/sensor/temperatura";
const char* client_id = "ESP8266Client";

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
char msg[50];
float temperatura = 0;

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
  Serial.println("Dirección IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Intentando conexión MQTT...");
    if (client.connect(client_id)) {
      Serial.println("conectado");
    } else {
      Serial.print("falló, rc=");
      Serial.print(client.state());
      Serial.println(" intentando de nuevo en 5 segundos");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;
    
    // Simula una lectura de temperatura
    temperatura = random(20, 30);
    
    // Convierte el float a string
    snprintf(msg, 50, "%.1f", temperatura);
    
    Serial.print("Publicando temperatura: ");
    Serial.println(msg);
    
    // Publica el mensaje
    client.publish(mqtt_topic, msg);
  }
} 