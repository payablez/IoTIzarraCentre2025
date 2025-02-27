/*
 * Ejemplo de sensor de luz (LDR) en Arduino
 * 
 * Conexiones:
 * - LDR: un pin a 5V, otro pin a PIN_LDR (A0) y a GND con resistencia 10kΩ
 * - LED: ánodo a PIN_LED (9) con resistencia 220Ω, cátodo a GND
 * 
 * Este ejemplo muestra:
 * 1. Lectura de entrada analógica
 * 2. Control de brillo LED por PWM
 * 3. Mapeo de valores
 * 4. Filtrado de lecturas
 */

// Definición de pines
const int PIN_LDR = A0;  // Pin analógico para el LDR
const int PIN_LED = 9;   // Pin PWM para el LED

// Configuración del sensor
const int NUM_SAMPLES = 10;     // Número de muestras para promediar
const int SAMPLE_DELAY = 10;    // Delay entre muestras (ms)
const int PRINT_DELAY = 1000;   // Delay entre impresiones (ms)

// Variables para el filtrado
int samples[NUM_SAMPLES];
int sampleIndex = 0;
unsigned long lastPrintTime = 0;

void setup() {
  // Configurar pin del LED como salida
  pinMode(PIN_LED, OUTPUT);
  
  // Iniciar comunicación serial
  Serial.begin(9600);
  Serial.println("Iniciando sensor de luz...");
  
  // Inicializar array de muestras
  for (int i = 0; i < NUM_SAMPLES; i++) {
    samples[i] = 0;
  }
}

int getLightLevel() {
  // Tomar una nueva muestra
  samples[sampleIndex] = analogRead(PIN_LDR);
  sampleIndex = (sampleIndex + 1) % NUM_SAMPLES;
  
  // Calcular promedio
  long sum = 0;
  for (int i = 0; i < NUM_SAMPLES; i++) {
    sum += samples[i];
  }
  return sum / NUM_SAMPLES;
}

void loop() {
  // Leer nivel de luz (promediado)
  int lightLevel = getLightLevel();
  
  // Mapear el valor de luz a brillo del LED (invertido)
  // Más luz = LED más tenue
  int brightness = map(lightLevel, 0, 1023, 255, 0);
  analogWrite(PIN_LED, brightness);
  
  // Imprimir valores cada PRINT_DELAY ms
  unsigned long currentTime = millis();
  if (currentTime - lastPrintTime >= PRINT_DELAY) {
    lastPrintTime = currentTime;
    
    // Calcular porcentaje de luz
    int lightPercent = map(lightLevel, 0, 1023, 0, 100);
    
    Serial.print("Nivel de luz: ");
    Serial.print(lightPercent);
    Serial.print("% (raw: ");
    Serial.print(lightLevel);
    Serial.print(", LED: ");
    Serial.print(map(brightness, 0, 255, 0, 100));
    Serial.println("%)");
  }
  
  // Pequeño delay entre lecturas
  delay(SAMPLE_DELAY);
} 