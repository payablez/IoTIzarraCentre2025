// PLACA TTGO LORA32-OLED

// #include <U8g2lib.h>
#include <SPI.h>
#include <SoftwareSerial.h>

// Definición de pines para el ZH03
#define ZH03_RX 7  // Serial2 RX
#define ZH03_TX 8  // Serial2 TX

// Comandos para el ZH03
const uint8_t setQAMode[] = {0xFF, 0x01, 0x78, 0x41, 0x00, 0x00, 0x00, 0x00, 0x46};  // Comando para poner en modo Q&A
const uint8_t readCommand[] = {0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79}; // Comando para leer datos

//Inicialización de la pantalla U8g2
// // // U8G2_SSD1306_128X64_NONAME_F_SW_I2C u8g2(U8G2_R0, /* clock=*/ 22, /* data=*/ 21, /* reset=*/ 0);

// Inicialización del puerto serie para el ZH03
SoftwareSerial zh03Serial(ZH03_RX, ZH03_TX);

// Buffer para los datos del sensor
uint8_t buffer[9];
uint8_t data[9];

void setup() {
  // Inicialización del puerto serie para debug
  Serial.begin(115200);
  Serial.println("Iniciando sistema...");
  
  // Inicialización del puerto serie para el ZH03
  zh03Serial.begin(9600);
  Serial.println("ZH03 Serial iniciado");
  
  // Configurar ZH03 en modo Q&A
  Serial.println("Configurando ZH03 en modo Q&A...");
  zh03Serial.write(setQAMode, sizeof(setQAMode));
  delay(100);
  
  // Inicialización de la pantalla
  // u8g2.begin();
  // u8g2.enableUTF8Print(); // Habilitar soporte para caracteres UTF8
  Serial.println("Pantalla OLED iniciada");
  
 
  
  Serial.println("Setup completado");
  delay(1000);
}

void loop() {
  // Enviar comando de lectura
  zh03Serial.write(readCommand, sizeof(readCommand));
  Serial.println("Comando de lectura enviado");
  
  // Esperar respuesta
  delay(100);
  
  if (zh03Serial.available() >= 9) {
    Serial.println("Datos recibidos del ZH03");
    
    // Leer los datos del sensor
    for (int i = 0; i < 9; i++) {
      buffer[i] = zh03Serial.read();
    }
    
    // Verificar el checksum
    // if (verifyChecksum(buffer)) {
      Serial.println("Checksum correcto");
      // Procesar los datos
      processData(buffer);
      
      // Mostrar los datos en la pantalla
      displayData();
    // } else {
    //   Serial.println("Error en checksum");
    // }
  } else {
    Serial.println("No hay datos disponibles");
  }
  
  delay(1000); // Esperar 1 segundo entre lecturas
}

bool verifyChecksum(uint8_t *data) {
  uint16_t sum = 0;
  for (int i = 0; i < 8; i++) {
    sum += data[i];
  }
  return (sum == data[8]);
}

void processData(uint8_t *data) {
  // Extraer los valores de PM1.0, PM2.5 y PM10
  uint16_t pm2_5 = (data[2] << 8) | data[3];
  uint16_t pm10 = (data[4] << 8) | data[5];
  uint16_t pm1_0 = (data[6] << 8) | data[7];
  
  // Guardar los datos para mostrar
  data[2] = pm1_0 >> 8;
  data[3] = pm1_0 & 0xFF;
  data[4] = pm2_5 >> 8;
  data[5] = pm2_5 & 0xFF;
  data[6] = pm10 >> 8;
  data[7] = pm10 & 0xFF;
  
  // Mostrar valores en el monitor serie
  Serial.print("PM1.0: "); Serial.print(pm1_0); Serial.println(" ug/m3");
  Serial.print("PM2.5: "); Serial.print(pm2_5); Serial.println(" ug/m3");
  Serial.print("PM10: "); Serial.print(pm10); Serial.println(" ug/m3");
}

void displayData() {
  char buf[32];
  
  // u8g2.clearBuffer();
  // // u8g2.setFont(u8g2_font_6x10_tf);
  
  // Mostrar título
  // u8g2.drawStr(0, 10, "ZH03 Sensor");
  
  // Mostrar PM1.0
  sprintf(buf, "PM1.0: %d ug/m3", (data[0] << 8) | data[1]);
  // u8g2.drawStr(0, 25, buf);
  
  // Mostrar PM2.5
  sprintf(buf, "PM2.5: %d ug/m3", (data[2] << 8) | data[3]);
  
  // Mostrar PM10
  sprintf(buf, "PM10: %d ug/m3", (data[4] << 8) | data[5]);
  
  
}
