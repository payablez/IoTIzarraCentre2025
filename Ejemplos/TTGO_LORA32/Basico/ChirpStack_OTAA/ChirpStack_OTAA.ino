// Define para evitar tener que modificar el config.h de la librería LMIC
// Sino, se puede usar el config.h de la librería LMIC y borrar el siguiente bloque de código, para que se comparta en el resto de proyectos.
#ifndef _lmic_config_h_
#define _lmic_config_h_
// Definiciones iniciales en la librería LMIC
#define USE_IDEETRON_AES
#define LMIC_FAILURE_TO Serial
#define LMIC_DEBUG_LEVEL 0
#define US_PER_OSTICK_EXPONENT 4
#define US_PER_OSTICK (1 << US_PER_OSTICK_EXPONENT)
#define OSTICKS_PER_SEC (1000000 / US_PER_OSTICK)
// Configuración de la radio para LILYGO V1.6.1 
#define CFG_sx1276_radio 1
#define CFG_eu868 1
#endif // _lmic_config_h_


// Seleccionar el modelo de placa
#define T3_V1_6_SX1276

#include <SPI.h>
#include <Wire.h>
#include <lmic.h>
#include <hal/hal.h>
#include "SSD1306.h"
#include <U8x8lib.h>
#include "LoRaBoards.h"

// OTAA parameters - LSB mode
static const u1_t PROGMEM APPEUI[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

// DEVEUI - En Chirpstack se copia al revés, 70b3d57ed0066f8d
static const u1_t PROGMEM DEVEUI[8] = {0x8D, 0x6F, 0x06, 0xD0, 0x7E, 0xD5, 0xB3, 0x70};
// APPKEY - En Chirsptack se mantiene igual, 757fe4b5d0bb39038d6f06d07ed5b370
static const u1_t PROGMEM APPKEY[16] = {0x75, 0x7F, 0xE4, 0xB5, 0xD0, 0xBB, 0x39, 0x03, 0x8D, 0x6F, 0x06, 0xD0, 0x7E, 0xD5, 0xB3, 0x70};

// Pin mapping for LMIC
const lmic_pinmap lmic_pins = {
    .nss = RADIO_CS_PIN,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = RADIO_RST_PIN,
    .dio = {RADIO_DIO0_PIN, RADIO_DIO1_PIN, RADIO_DIO2_PIN}
};

// LMIC variables
static osjob_t sendjob;
static int spreadFactor = DR_SF7;
static int joinStatus = EV_JOINING;
static const unsigned TX_INTERVAL = 120; // Intervalo de envío de prueba en segundos
static String lora_msg = "";
static uint8_t counter = 0;

// Callbacks for LMIC
void os_getArtEui(u1_t* buf) { memcpy_P(buf, APPEUI, 8); }
void os_getDevEui(u1_t* buf) { memcpy_P(buf, DEVEUI, 8); }
void os_getDevKey(u1_t* buf) { memcpy_P(buf, APPKEY, 16); }

void onEvent(ev_t ev) {
    Serial.print(os_getTime());
    Serial.print(": ");
    switch (ev) {
        case EV_TXCOMPLETE:
            Serial.println(F("EV_TXCOMPLETE (includes waiting for RX windows)"));
            
            if (LMIC.txrxFlags & TXRX_ACK) {
                Serial.println(F("Received ack"));
                lora_msg = "Received ACK.";
            }
            
            lora_msg = "rssi:" + String(LMIC.rssi) + " snr: " + String(LMIC.snr);
            
            if (LMIC.dataLen) {
                // data received in rx slot after tx
                Serial.print(F("Data Received: "));
                Serial.println(LMIC.dataLen);
                Serial.println(F(" bytes of payload"));
            }
            
            // Update display
            if (u8g2) {
                u8g2->clearBuffer();
                u8g2->setFont(u8g2_font_6x10_tr);
                u8g2->drawStr(0, 10, "Packet sent: ");
                u8g2->drawStr(0, 20, lora_msg.c_str());
                u8g2->sendBuffer();
            }
            
            // Schedule next transmission
            os_setTimedCallback(&sendjob, os_getTime() + sec2osticks(TX_INTERVAL), do_send);
            break;
            
        case EV_JOINING:
            Serial.println(F("EV_JOINING: -> Joining..."));
            lora_msg = "OTAA joining....";
            joinStatus = EV_JOINING;
            
            // Update display
            if (u8g2) {
                u8g2->clearBuffer();
                u8g2->setFont(u8g2_font_6x10_tr);
                u8g2->drawStr(0, 10, "Joining network...");
                u8g2->sendBuffer();
            }
            break;
            
        case EV_JOIN_FAILED:
            Serial.println(F("EV_JOIN_FAILED: -> Joining failed"));
            lora_msg = "OTAA Joining failed";
            
            // Update display
            if (u8g2) {
                u8g2->clearBuffer();
                u8g2->setFont(u8g2_font_6x10_tr);
                u8g2->drawStr(0, 10, "Join failed!");
                u8g2->sendBuffer();
            }
            break;
            
        case EV_JOINED:
            Serial.println(F("EV_JOINED"));
            lora_msg = "Joined!";
            joinStatus = EV_JOINED;
            
            // Update display
            if (u8g2) {
                u8g2->clearBuffer();
                u8g2->setFont(u8g2_font_6x10_tr);
                u8g2->drawStr(0, 10, "Joined network!");
                u8g2->sendBuffer();
            }
            
            // Disable link check validation
            LMIC_setLinkCheckMode(0);
            break;
            
        case EV_RXCOMPLETE:
            // data received in ping slot
            Serial.println(F("EV_RXCOMPLETE"));
            break;
            
        case EV_LINK_DEAD:
            Serial.println(F("EV_LINK_DEAD"));
            break;
            
        case EV_LINK_ALIVE:
            Serial.println(F("EV_LINK_ALIVE"));
            break;
            
        default:
            Serial.println(F("Unknown event"));
            break;
    }
}

void do_send(osjob_t* j) {
    if (joinStatus == EV_JOINING) {
        Serial.println(F("Aún haciendo join"));
        // Check if there is not a current TX/RX job running
        os_setTimedCallback(&sendjob, os_getTime() + sec2osticks(TX_INTERVAL), do_send);
    } else if (LMIC.opmode & OP_TXRXPEND) {
        Serial.println(F("OP_TXRXPEND, not sending"));
    } else {
        Serial.println(F("Enviamos dato de prueba"));
        
        // Prepare data to send
        char data[32];
        snprintf(data, sizeof(data), "%d", counter++);
        
        // Prepare upstream data transmission at the next possible time
        LMIC_setTxData2(1, (uint8_t*)data, strlen(data), 0);
        
        // Schedule next transmission
        os_setTimedCallback(&sendjob, os_getTime() + sec2osticks(TX_INTERVAL), do_send);
        
        // Update display
        if (u8g2) {
            u8g2->clearBuffer();
            u8g2->setFont(u8g2_font_6x10_tr);
            u8g2->drawStr(0, 10, "Envío: ");
            u8g2->drawStr(0, 20, data);
            u8g2->sendBuffer();
        }
    }
}

void setupLMIC() {
    // LMIC init
    os_init();
    
    // Reset the MAC state. Session and pending data transfers will be discarded.
    LMIC_reset();
    
    // Set clock error
    LMIC_setClockError(MAX_CLOCK_ERROR * 1 / 100);
    
    // Set up the channels used by the Things Network
    LMIC_setupChannel(0, 868100000, DR_RANGE_MAP(DR_SF12, DR_SF7), BAND_CENTI);
    LMIC_setupChannel(1, 868300000, DR_RANGE_MAP(DR_SF12, DR_SF7B), BAND_CENTI);
    LMIC_setupChannel(2, 868500000, DR_RANGE_MAP(DR_SF12, DR_SF7), BAND_CENTI);
    LMIC_setupChannel(3, 867100000, DR_RANGE_MAP(DR_SF12, DR_SF7), BAND_CENTI);
    LMIC_setupChannel(4, 867300000, DR_RANGE_MAP(DR_SF12, DR_SF7), BAND_CENTI);
    LMIC_setupChannel(5, 867500000, DR_RANGE_MAP(DR_SF12, DR_SF7), BAND_CENTI);
    LMIC_setupChannel(6, 867700000, DR_RANGE_MAP(DR_SF12, DR_SF7), BAND_CENTI);
    LMIC_setupChannel(7, 867900000, DR_RANGE_MAP(DR_SF12, DR_SF7), BAND_CENTI);
    LMIC_setupChannel(8, 868800000, DR_RANGE_MAP(DR_FSK, DR_FSK), BAND_MILLI);
    
    // Disable link check validation
    LMIC_setLinkCheckMode(0);
    
    // TTN uses SF9 for its RX2 window
    LMIC.dn2Dr = DR_SF9;
    
    // Set data rate and transmit power for uplink
    LMIC_setDrTxpow(spreadFactor, 14);
    
    Serial.println("Iniciando OTAA join...");
    
    // Start job
    LMIC_startJoining();
    
    // Will fire up also the join
    do_send(&sendjob);
}

void setup() {
    // Initialize board using LoRaBoards setup
    setupBoards();
    
    // Initialize serial
    Serial.println("TTGO LoRa32 OTAA Test");
    
    // Initialize LMIC
    setupLMIC();
}

void loop() {
    // Run LMIC loop
    os_runloop_once();
}
