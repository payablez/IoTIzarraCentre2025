/*
 * Ejemplo de lectura de botón en Arduino
 * 
 * Conexiones:
 * - Botón: un pin a GND, otro pin a PIN_BUTTON (2) con resistencia pull-up interna
 * - LED: ánodo a PIN_LED (13), cátodo a GND con resistencia 220Ω
 * 
 * Este ejemplo muestra:
 * 1. Lectura de entrada digital
 * 2. Uso de resistencia pull-up interna
 * 3. Detección de cambios de estado
 * 4. Debouncing por software
 */

// Definición de pines
const int PIN_BUTTON = 2;  // Pin para el botón
const int PIN_LED = 13;    // Pin para el LED (LED_BUILTIN)

// Variables para el estado del botón
int buttonState = HIGH;         // Estado actual del botón
int lastButtonState = HIGH;     // Estado anterior del botón
bool ledState = false;         // Estado del LED

// Variables para debouncing
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;  // Tiempo de debounce en ms

void setup() {
  // Configurar pin del botón como entrada con pull-up
  pinMode(PIN_BUTTON, INPUT_PULLUP);
  
  // Configurar pin del LED como salida
  pinMode(PIN_LED, OUTPUT);
  
  // Iniciar comunicación serial
  Serial.begin(9600);
  Serial.println("Iniciando ejemplo de botón...");
}

void loop() {
  // Leer el estado actual del botón
  int reading = digitalRead(PIN_BUTTON);

  // Si el estado ha cambiado, reiniciar el timer de debounce
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  // Si ha pasado suficiente tiempo desde el último cambio
  if ((millis() - lastDebounceTime) > debounceDelay) {
    // Si el estado ha cambiado realmente
    if (reading != buttonState) {
      buttonState = reading;

      // Si el botón está presionado (LOW debido al pull-up)
      if (buttonState == LOW) {
        // Cambiar estado del LED
        ledState = !ledState;
        digitalWrite(PIN_LED, ledState);
        
        // Imprimir estado
        Serial.print("LED: ");
        Serial.println(ledState ? "Encendido" : "Apagado");
      }
    }
  }

  // Guardar la lectura para la próxima vez
  lastButtonState = reading;
} 