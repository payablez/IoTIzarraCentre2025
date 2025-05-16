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


## Conclusión

Este proyecto ha representado una valiosa oportunidad para explorar nuevas tecnologías y comprender su aplicación en un entorno real. A lo largo del desarrollo, se han adquirido conocimientos clave sobre plataformas como ChirpStack, Node-RED, InfluxDB y Grafana, así como sobre el tratamiento de datos provenientes de sensores IoT, específicamente un sensor de CO₂.

A pesar de los avances alcanzados, el proyecto también presentó una serie de desafíos:

- Limitaciones de tiempo: El calendario ajustado dificultó una implementación más completa y robusta de todas las funcionalidades previstas.

- Uso de nuevas tecnologías: El trabajo implicó un proceso constante de aprendizaje, ya que muchas de las herramientas empleadas eran desconocidas previamente para el equipo.

- Implementación en entorno real: Integrar los sensores y servicios en una infraestructura funcional planteó problemas reales de conexión, compatibilidad y estabilidad que no siempre pudieron resolverse de forma inmediata.

- Investigación del sensor de CO₂: Se dedicó tiempo significativo a entender el funcionamiento y la integración del sensor de dióxido de carbono, lo que enriqueció el aprendizaje pero también retrasó otras tareas.

- Trabajo en varios grupos: El hecho de que el proyecto estuviera dividido entre varios equipos dificultó la coordinación y el acceso equitativo a herramientas compartidas, generando algunas complicaciones logísticas y técnicas.

En conjunto, el proyecto ha permitido desarrollar una base funcional sobre la cual se pueden construir soluciones IoT más avanzadas, y ha servido como experiencia práctica para enfrentar los retos comunes en proyectos colaborativos y tecnológicos
