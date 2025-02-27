#!/usr/bin/env python3
"""
Ejemplo de envío de datos usando LoRa en Raspberry Pi
Requiere un módulo LoRa conectado por SPI

Conexiones para módulo LoRa Ra-02:
- NSS/CS -> GPIO8 (CE0)
- SCK -> GPIO11 (SCLK)
- MOSI -> GPIO10 (MOSI)
- MISO -> GPIO9 (MISO)
- RST -> GPIO22
- DIO0 -> GPIO4
"""

import time
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()
BOARD.reset()

class LoRaSender(LoRa):
    def __init__(self, verbose=False):
        super(LoRaSender, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        
    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        
        # Configurar parámetros LoRa
        self.set_freq(433.0)  # Frecuencia en MHz
        self.set_pa_config(pa_select=1)  # PA_BOOST
        self.set_spreading_factor(7)
        self.set_bw(125.0)  # 125 kHz
        self.set_coding_rate(CODING_RATE.CR4_5)
        self.set_sync_word(0x34)  # Palabra de sincronización
        
        print("Configuración LoRa completada")
        
    def send_data(self, data):
        """Envía datos por LoRa"""
        self.write_payload([ord(c) for c in data])
        self.set_mode(MODE.TX)
        while (self.get_irq_flags()['tx_done'] == 0):
            pass
        self.clear_irq_flags(TxDone=1)
        print(f"Mensaje enviado: {data}")

def main():
    """Función principal del programa"""
    try:
        print("Iniciando LoRa Sender...")
        lora = LoRaSender(verbose=False)
        lora.start()
        
        counter = 0
        print("Presiona Ctrl+C para terminar")
        
        while True:
            message = f"Mensaje #{counter} desde Raspberry Pi"
            lora.send_data(message)
            counter += 1
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario")
    finally:
        BOARD.teardown()
        print("Limpieza completada")

if __name__ == "__main__":
    main() 