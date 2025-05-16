Grupo 6 - Sistema de Monitoreo Ambiental
Integrantes

    Sergio Lopez
    Erik Montero
    Mikel Perez
    Ignacio Arrizabalaga

Descripción del Proyecto

Sistema de monitoreo basado en ESP32 que integra múltiples sensores (PIR, LDR, ultrasónico) para detectar movimiento, medir niveles de luz y calcular distancias. El sistema envía los datos recopilados a un servidor web mediante solicitudes HTTP y controla automáticamente un LED basado en las condiciones del entorno.

En este proyecto hemos utilizado la placa ESP32-WROOM-32D para captar datos y enviarlos mediante peticiones HTTP hacia un servidor local donde empleamos Node-RED como intermediario. Node-RED recibe las solicitudes a través de una ruta específica (/grupo6) y redirige los datos a una base de datos InfluxDB, donde se almacenan con marcas de tiempo para su posterior análisis. En la captura de pantalla de Node-RED se puede observar un flujo en el que el nodo [GET] /grupo6 recibe las peticiones del ESP32, las envía a un nodo denominado localhost (que representa la conexión o tratamiento local de los datos), y finalmente se responde al dispositivo con un estado HTTP 200 mediante el nodo http response.

Una vez almacenados los datos en InfluxDB, utilizamos Grafana para visualizarlos gráficamente mediante paneles personalizados, lo que nos permite monitorear en tiempo real las variables enviadas por el ESP32.
Hardware Utilizado

    ESP32 Development Board
    Sensor PIR (movimiento)
    Sensor LDR (luz)
    Sensor ultrasónico HC-SR04 (distancia)
    LED

Estructura

    Chirpstack/: Contiene los archivos de codificación/decodificación para ChirpStack
    Aplicacion/: Contiene el código de la aplicación principal
        main.ino: Código principal para el ESP32

Arquitectura del Sistema

    Capa de Adquisición de Datos (ESP32)
        Sensores conectados al ESP32-WROOM-32D
        Envío de datos mediante peticiones HTTP GET
    Capa de Procesamiento (Node-RED)
        Recepción de solicitudes en la ruta /grupo6
        Procesamiento y redirección de datos
        Respuesta al dispositivo con estado HTTP 200
    Capa de Almacenamiento (InfluxDB)
        Base de datos de series temporales
        Almacenamiento de datos con marcas de tiempo
    Capa de Visualización (Grafana)
        Paneles personalizados para visualización en tiempo real
        Consultas a InfluxDB para representar gráficamente los datos
        Monitoreo de variables de entorno (luz, movimiento, distancia)

Instrucciones de Instalación
Requisitos Previos

    Arduino IDE instalado
    Biblioteca ESP32 para Arduino
    Bibliotecas adicionales:
        WiFi
        HTTPClient
        esp_task_wdt

Conexiones de Hardware

    Conectar el sensor PIR al pin 19
    Conectar el LED al pin 21
    Conectar el sensor ultrasónico:
        Pin TRIGGER al pin 17
        Pin ECHO al pin 16
    Conectar el sensor LDR al pin 34

Configuración WiFi

    Modificar las credenciales WiFi en el archivo main.ino:

    cpp

    const char* ssid = "IzarraCentre";
    const char* password = "Tu_Contraseña"; // Cambiar si es necesario

    Configurar la URL del servidor:

    cpp

    const char* serverUrl = "http://formacioniot2025.devlon.es/grupo6";

Uso

    Cargar el código al ESP32 utilizando Arduino IDE
    El sistema se iniciará automáticamente y calibrará el sensor PIR (30 segundos)
    El dispositivo realizará las siguientes funciones:
        Detección de movimiento con el sensor PIR
        Medición de niveles de luz con el sensor LDR
        Medición de distancia con el sensor ultrasónico
        Control automático del LED basado en movimiento y niveles de luz
        Envío de datos al servidor cada 5 segundos

Comportamiento del LED

    El LED se encenderá cuando:
        Se detecte movimiento Y
        El nivel de luz sea menor o igual al 80%

Monitoreo

    Los datos se pueden visualizar en la consola serial (115200 baudios)
    Los datos se envían al servidor: http://formacioniot2025.devlon.es/grupo6
    Parámetros enviados:
        motion: Estado del sensor de movimiento (0/1)
        light: Porcentaje de luz (0-100%)
        distance: Distancia medida en centímetros

En este proyecto recibimos datos procedentes de un sensor de luz conectado a una placa ESP32-WROOM-32D. Estos datos se envían de forma periódica al servidor, donde son gestionados por Node-RED y almacenados en una base de datos InfluxDB. Desde allí, realizamos consultas (querys) directamente en Grafana para representar de manera simulada los valores del sensor de luz en tiempo real. Gracias a las capacidades de visualización de Grafana y la estructura temporal de InfluxDB, podemos observar cómo varía la intensidad lumínica a lo largo del tiempo mediante gráficas dinámicas, simulando así el comportamiento del entorno captado por el sensor.
Solución de Problemas

> [!WARNING]  
> Si la conexión WiFi falla, el dispositivo se reiniciará automáticamente, El sistema utiliza un watchdog timer para recuperarse de posibles bloqueos.
    

