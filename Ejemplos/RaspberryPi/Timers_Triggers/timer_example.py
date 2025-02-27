#!/usr/bin/env python3
"""
Ejemplo de uso de timers en Raspberry Pi
Este script demuestra diferentes formas de implementar temporizadores
"""

import time
import threading
from datetime import datetime
import schedule

def simple_timer():
    """Timer simple usando time.sleep()"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Timer simple ejecutado")

def threaded_timer():
    """Timer usando threading"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Timer con threading ejecutado")

def scheduled_task():
    """Tarea programada usando schedule"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Tarea programada ejecutada")

def start_threaded_timer():
    """Inicia un timer usando threading"""
    timer = threading.Timer(5.0, threaded_timer)
    timer.start()
    return timer

def main():
    """Función principal del programa"""
    print("Iniciando ejemplo de timers...")
    print("Presiona Ctrl+C para terminar")
    
    # Configurar tareas programadas
    schedule.every(10).seconds.do(scheduled_task)
    schedule.every().minute.at(":00").do(lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Es el inicio de un nuevo minuto"))
    schedule.every().hour.at(":00").do(lambda: print(f"[{datetime.now().strftime('%H:%M:%S')}] Es el inicio de una nueva hora"))
    
    try:
        # Iniciar timer con threading
        timer = start_threaded_timer()
        
        while True:
            # Ejecutar timer simple
            simple_timer()
            
            # Ejecutar tareas programadas
            schedule.run_pending()
            
            # Esperar antes del siguiente ciclo
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario")
        if timer.is_alive():
            timer.cancel()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 