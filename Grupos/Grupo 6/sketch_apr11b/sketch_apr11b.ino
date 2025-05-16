#include <esp_task_wdt.h>
#include <WiFi.h>
#include <HTTPClient.h>

int PIN_PIR = 19;        // Motion sensor pin
int PIN_LED = 21;        // LED pin
int PIN_TRIGGER = 17;    // Ultrasonic sensor trigger pin
int PIN_ECHO = 16;       // Ultrasonic sensor echo pin
int PIN_LDR = 34;        // LDR (light sensor) pin

// Wi-Fi credentials
const char* ssid = "IzarraCentre"; // (Wi-Fi name)
const char* password = "Enter Password"; // (Wi-Fi password)

// Server endpoint
const char* serverUrl = "http://formacioniot2025.devlon.es/grupo6";

// Variables for ultrasonic sensor
long duration;
float distance;

void setup() {
  pinMode(PIN_PIR, INPUT);
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_TRIGGER, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  pinMode(PIN_LDR, INPUT);
 
  digitalWrite(PIN_TRIGGER, LOW);
  digitalWrite(PIN_LED, LOW);
 
  Serial.begin(115200);
  Serial.println("Iniciando sistema...");
 
  // Watchdog Timer Configuration
  esp_task_wdt_config_t wdt_config = {
    .timeout_ms = 5000,    
    .idle_core_mask = 0,  
    .trigger_panic = true  
  };
  esp_task_wdt_init(&wdt_config);
 
  // Connect to a Wi-Fi network
  Serial.print("Conectando a WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid); // Change it to (ssid, password) if password required.
 
  int attempts = 0;
  const int maxAttempts = 20; // Try for 10s maxAttempts * delay
  while (WiFi.status() != WL_CONNECTED && attempts < maxAttempts) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
 
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n¡Conectado a WiFi!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nError: No se pudo conectar a WiFi. Verifica la red.");
    ESP.restart(); // Restart if it fails
  }
 
  Serial.println("Calibrando sensor PIR (30 segundos)...");
  delay(30000); // 30 seconds for PIR calibration
  Serial.println("¡Sensores listos!");
}

// Function to measure distance with ultrasonic sensor
float measureDistance() {
  // Clear the trigger pin
  digitalWrite(PIN_TRIGGER, LOW);
  delayMicroseconds(2);
  
  // Set the trigger pin high for 10 microseconds
  digitalWrite(PIN_TRIGGER, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIGGER, LOW);
  
  // Read the echo pin (time in microseconds)
  duration = pulseIn(PIN_ECHO, HIGH);
  
  // Calculate the distance
  // Sound speed = 343m/s = 0.0343cm/µs
  // Distance = (time * speed of sound) / 2 (round trip)
  distance = (duration * 0.0343) / 2;
  
  return distance;
}

void loop() {
  // Read motion sensor with debouncing (avoid excesive execution of a function being called way too many times)
  int movimiento = 0;
  for (int i = 0; i < 10; i++) {
    movimiento += digitalRead(PIN_PIR);
    delay(10);
  }
  movimiento = (movimiento >= 2) ? HIGH : LOW;
 
  Serial.print("PIR estado: ");
  Serial.println(movimiento == HIGH ? "HIGH" : "LOW");
 
  // Read light sensor and convert to percentage
  int ldrValue = analogRead(PIN_LDR);
  int lightPercent = map(ldrValue, 4095, 0, 0, 100);
 
  Serial.print("Nivel de luz: ");
  Serial.print(lightPercent);
  Serial.println("%");
  
  // Measure distance with ultrasonic sensor
  float distanceCm = measureDistance();
  
  Serial.print("Distancia: ");
  Serial.print(distanceCm);
  Serial.println(" cm");
 
  // Control LED based on movement and light level
  if (movimiento == HIGH && lightPercent <= 80) {
    digitalWrite(PIN_LED, HIGH);
    Serial.println("Movimiento detectado y luz baja, LED encendido");
  } else {
    digitalWrite(PIN_LED, LOW);
    if (movimiento == HIGH && lightPercent > 80) {
      Serial.println("Movimiento detectado pero luz alta (>80%), LED se mantiene apagado");
    } else if (movimiento == LOW) {
      Serial.println("Sin movimiento, LED apagado");
    }
  }
 
  // Send data via GET request
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
   
    // Params to send the data (now including distance)
    String url = String(serverUrl) + "?motion=" + String(movimiento) + 
                 "&light=" + String(lightPercent) + 
                 "&distance=" + String(distanceCm);
   
    Serial.println("Enviando GET: " + url);
    http.begin(url);
    int httpCode = http.GET();
   
    if (httpCode > 0) {
      Serial.printf("Código de respuesta: %d\n", httpCode);
      if (httpCode == HTTP_CODE_OK) {
        String payload = http.getString();
        Serial.println("Respuesta: " + payload);
      }
    } else {
      Serial.printf("Error en GET: %s\n", http.errorToString(httpCode).c_str());
    }
   
    http.end();
  } else {
    Serial.println("WiFi desconectado, no se puede enviar datos");
  }
 
  delay(5000); // Send data every 5 seconds
}