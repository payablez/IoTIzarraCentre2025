# Grupo 2

## Integrantes
- Gorka García
- Gorka Cereza
- Moisés Justiniano
- Mikel Martínez
- Markel López

## Descripción del Proyecto
El proyecto consiste en un sistema de control para el edificio Izarra Centre, utilizando una red de sensores para mejorar la seguridad y eficiencia del edificio. Los sensores monitorean diversos aspectos clave:

- **Sensores de fugas de agua** en el garaje subterráneo para detectar y prevenir inundaciones.
- **Botón** de recepción para alertar en caso de ausencia del portero.
- **Sensor de puertas** para asegurar que los frigoríficos permanezcan cerrados y evitar pérdidas de alimentos.
- **Sensor de CO2 y humedad** para monitorear la calidad del aire en la sala de reuniones.

Este sistema permitirá una mejor gestión y control del edificio, proporcionando datos en tiempo real y mejorando la respuesta ante incidentes.
## Estructura
- `Chirpstack/`: Contiene los archivos de codificación/decodificación para ChirpStack
- `Aplicacion/`: Contiene el código de la aplicación principal

## Estructura del sistema
### Chirpstack

Los sensores se registran en ChirpStack, donde también se desarrollan los decoders personalizados para cada tipo de dispositivo. Estos decoders permiten interpretar correctamente los datos entrantes y asegurar que la plataforma reciba la información en un formato comprensible.

### Node-RED

Node-RED se encarga de recibir los datos desde ChirpStack mediante solicitudes HTTP. Una vez recibidos, se procesan a través de funciones personalizadas que formatean la información y la adaptan a la estructura requerida por el sistema.
Posteriormente, los datos se dividen en dos flujos:

- Se almacenan en la base de datos InfluxDB.
- Se genera una alerta por correo electrónico en caso de que se cumplan ciertas condiciones definidas.

### InfluxDB

InfluxDB actúa como la base de datos principal del sistema, donde se almacenan todos los datos recopilados por los sensores. Su modelo orientado a series temporales permite un almacenamiento eficiente y consultas optimizadas para datos en tiempo real.

### Grafana

Grafana se utiliza para visualizar los datos almacenados en InfluxDB. Permite representar la información de los dispositivos en tiempo real de forma clara e intuitiva, mediante paneles y gráficos personalizables. Esto facilita el monitoreo y análisis de los datos de forma dinámica y eficiente.

