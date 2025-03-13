# Configuración Inicial ChirpStack Ermua

## Acceso al Sistema

1. Accede al portal de ChirpStack Ermua https://lorawan.ermua.eus
2. Utiliza las credenciales proporcionadas por el administrador

## Registro de un perfil de dispositivo (device profile)

1. En el menú lateral, selecciona "Device-profiles"
2. Haz clic en "+ CREATE"
3. Completa los campos:
   - **Name**: Grupo N - Nombre descriptivo del perfil
   - **Description**: Breve descripción del propósito
   - **LoRaWAN MAC version**: 1.0.3
   - **Join (OTAA/ABP)**: OTAA
   - **Class**: Selecciona la clase del dispositivo (A, B o C)

## Configuración de Decodificación de Payload

1. En el perfil del dispositivo, ve a la pestaña Codec
2. Selecciona "Javascript functions"
3. Añade tus funciones de decodificación y codificación:

```javascript
// Decode uplink function.
//
// Input is an object with the following fields:
// - bytes = Byte array containing the uplink payload, e.g. [255, 230, 255, 0]
// - fPort = Uplink fPort.
// - variables = Object containing the configured device variables.
//
// Output must be an object with the following fields:
// - data = Object representing the decoded payload.
function decodeUplink(input) {
  return {
    data: {
      temp: 22.5
    }
  };
}

// Encode downlink function.
//
// Input is an object with the following fields:
// - data = Object representing the payload that must be encoded.
// - variables = Object containing the configured device variables.
//
// Output must be an object with the following fields:
// - bytes = Byte array containing the downlink payload.
function encodeDownlink(input) {
  return {
    bytes: [225, 230, 255, 0]
  };
}

```

## Registro de una Nueva Aplicación

1. En el menú lateral, selecciona "Applications"
2. Haz clic en "+ CREATE"
3. Completa los campos:
   - **Name**: Nombre descriptivo de tu aplicación
   - **Description**: Breve descripción del propósito
   - **Service-profile**: Selecciona el perfil proporcionado para Ermua

## Registro de un Dispositivo TTGO LORA32

1. Dentro de tu aplicación, selecciona "DEVICES"
2. Haz clic en "+ CREATE"
3. Completa los campos:
   - **Device name**: Nombre único para tu dispositivo
   - **Device description**: Descripción del dispositivo
   - **Device EUI**: Genera uno nuevo o usa el del dispositivo
   - **Device-profile**: Selecciona "TTGO_LORA32_PROFILE" (o el proporcionado)
   - **Disable frame-counter validation**: No marcar

### Configuración OTAA

1. En la pestaña "KEYS (OTAA)", encontrarás:
   - **Application key**: Se genera automáticamente
   - **Device EUI**: El que especificaste antes
   - **Application EUI**: Se genera automáticamente

2. Copia estos valores al código del dispositivo:
   ```cpp
   static const u1_t PROGMEM DEVEUI[8] = { 0x00, ... };  // Copiar en orden inverso (LSB)
   static const u1_t PROGMEM APPEUI[8] = { 0x00, ... };  // Copiar en orden inverso (LSB)
   static const u1_t PROGMEM APPKEY[16] = { 0x00, ... }; // Copiar en orden normal (MSB)
   ```

### Configuración ABP (Alternativa)

Si prefieres usar ABP en lugar de OTAA:

1. En el Device-profile, cambia "LoRaWAN MAC version" a 1.0.3
2. Cambia "Join (OTAA/ABP)" a ABP
3. En la pestaña "ACTIVATION", encontrarás:
   - **Device address**
   - **Network session key**
   - **Application session key**

## Verificación

1. Una vez que el dispositivo se une correctamente:
   - Verás "JOINED" en la pantalla OLED del TTGO
   - El dispositivo aparecerá como "Active" en ChirpStack
   - Podrás ver los datos recibidos en "DEVICE DATA"

## Solución de Problemas

### El dispositivo no se une
- Verifica que los keys estén correctamente copiados
- Confirma que estás en rango del gateway
- Comprueba que los canales configurados coinciden con los de Ermua

### No se reciben datos
- Verifica que el dispositivo esté activo
- Comprueba el contador de frames
- Revisa la configuración de ADR (Adaptive Data Rate)

## Recursos Adicionales

- [Documentación ChirpStack](https://www.chirpstack.io/docs/)
- [Especificación LoRaWAN Regional EU868](https://lora-alliance.org/resource_hub/rp2-1-0-3-lorawan-regional-parameters/) 