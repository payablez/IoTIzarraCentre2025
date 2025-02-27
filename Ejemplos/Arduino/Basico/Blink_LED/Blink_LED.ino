/*
 * Ejemplo básico de parpadeo de LED
 * Este ejemplo muestra cómo hacer parpadear el LED integrado de Arduino
 * 
 * Conexiones:
 * - No se necesitan conexiones externas, usa el LED_BUILTIN
 */

void setup() {
  // Inicializa el pin del LED como salida
  pinMode(LED_BUILTIN, OUTPUT);
  
  // Inicializa la comunicación serial para depuración
  Serial.begin(9600);
  Serial.println("Iniciando programa de parpadeo de LED...");
}

void loop() {
  // Enciende el LED
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println("LED encendido");
  delay(1000);  // Espera 1 segundo
  
  // Apaga el LED
  digitalWrite(LED_BUILTIN, LOW);
  Serial.println("LED apagado");
  delay(1000);  // Espera 1 segundo
} 