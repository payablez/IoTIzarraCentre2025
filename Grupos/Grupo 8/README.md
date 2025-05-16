# 🌿 Sistema de Riego Automático – Grupo 8

## 👥 Integrantes

- Alluitz Ortiz de Barron  
- Ibone Zubiate  
- Iker Nistal  
- Jehangir Hayat  
- Julen Galindo  

---

## 📌 Descripción del Proyecto

Este proyecto tiene como objetivo implementar un **sistema de riego automático** utilizando una placa **Arduino LilyGO LoRa32**. El sistema controla el nivel de humedad del sustrato de una planta mediante un **sensor de humedad del suelo**. Si detecta que el nivel de humedad es bajo, activa una **bomba de agua eléctrica** de forma automática para regar la planta.

Este sistema está pensado como una solución **de bajo coste, eficiente y autónoma**, ideal para pequeños huertos, plantas de interior o jardinería urbana.

---

## ⚙️ Funcionamiento

1. El **sensor de humedad** mide la cantidad de agua en el suelo.
2. La placa Arduino analiza el valor recibido.
3. Si la humedad está por debajo del umbral definido, se activa el **relé**.
4. El relé enciende la **bomba de agua**.
5. Al alcanzarse la humedad deseada, el sistema apaga la bomba automáticamente.

---

## 🔧 Componentes Utilizados

| Componente                     | Descripción                                                              |
|-------------------------------|--------------------------------------------------------------------------|
| Arduino LilyGO LoRa32         | Placa base con ESP32 y conectividad LoRa                                |
| Sensor de humedad del suelo   | Sensor analógico para medir la humedad del sustrato                     |
| Bomba de agua eléctrica       | Riega la planta automáticamente cuando se activa                        |
| Módulo relé                   | Permite al Arduino encender o apagar la bomba                           |
| Fuente de alimentación 5V–12V | Suministra energía al sistema                                           |
| Cables jumper                 | Utilizados para las conexiones entre los componentes                    |

---

## 🧠 Código y Visualización

A continuación, se muestra la lógica implementada en **Node-RED** y la consulta utilizada en **InfluxDB/Grafana** para la visualización de los datos:

```javascript
// 📍 Node-RED: Function Node
// Extrae temperatura y humedad desde un mensaje JSON
let temperatura = msg.payload.temperatura;
let humedad = msg.payload.humedad;

// Hora actual para posibles registros o visualización
let horaActual = new Date().toLocaleString();

// Mostrar los valores en el debug del flujo
node.warn(`Temperatura: ${temperatura}, Humedad: ${humedad}`);

// Devuelve el mensaje para los siguientes nodos
return msg;

// 📍 Consulta Flux en Grafana para visualizar la temperatura
from(bucket: "grupo8")
  |> range(start: -3mo)
  |> filter(fn: (r) =>
    r._measurement == "probaa" and
    r._field == "temperatura"
  )
  |> map(fn: (r) => ({ r with _value: float(v: r._value) }))
  |> aggregateWindow(every: 1m, fn: sum, createEmpty: false)

// 📍 Consulta Flux en Grafana para visualizar la humedad
from(bucket: "grupo8")
  |> range(start: -3mo)
  |> filter(fn: (r) =>
    r._measurement == "probaa" and
    r._field == "humedad"
  )
  |> map(fn: (r) => ({ r with _value: float(v: r._value) }))
  |> aggregateWindow(every: 1m, fn: sum, createEmpty: false)





