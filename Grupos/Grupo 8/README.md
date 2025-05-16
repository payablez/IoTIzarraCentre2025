# Grupo 8

# 🌿 Sistema de Riego Automático

**Integrantes**  
- [Alluitz Ortiz de Barron]  
- [Ibone Zubiate]  
- [Iker Nistal]  
- [Jehangir Hayat]
- [Julen Galindo]    

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
|--------------------------------|--------------------------------------------------------------------------|
| Arduino LilyGO LoRa32          | Placa base con ESP32 y conectividad LoRa                                |
| Sensor de humedad del suelo    | Sensor analógico para medir la humedad del sustrato                     |
| Bomba de agua eléctrica        | Riega la planta automáticamente cuando se activa                        |
| Módulo relé                    | Permite al Arduino encender o apagar la bomba                           |
| Fuente de alimentación 5V–12V  | Suministra energía al sistema                                           |
| Cables jumper                  | Utilizados para las conexiones entre los componentes                    |

---

## 🗂️ Estructura del Proyecto

