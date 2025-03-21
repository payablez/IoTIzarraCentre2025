
var payload = msg.payload;

// Identificar el tipo de dispositivo según el nombre o devEUI
var deviceName = payload.deviceInfo.deviceName;
var deviceType = payload.deviceInfo.deviceProfileName;

var data = {
    dispositivo: deviceName,
    devEUI: payload.deviceInfo.devEui,
    timestamp: payload.time
};

// Extraer datos según el tipo de sensor
if (deviceType === "Dragino PB01") {
    // Sensor de Botón
    data.tipo = "Botón";
    data.temperatura = payload.object.TempC_SHT41;
    data.humedad = payload.object.Hum_SHT41;
    data.bateria = payload.object.BatV;
    data.alarma = payload.object.Alarm;
    data.sonido = payload.object.Sound_ACK;
} else if (deviceType === "Puerta") {
    // Sensor de Puerta
    data.tipo = "Puerta";
    data.aperturas = payload.object.DOOR_OPEN_TIMES;
    data.duracion_ultima_apertura = payload.object.LAST_DOOR_OPEN_DURATION;
} else if (deviceType === "Sensor de agua") {
    // Sensor de Fugas de Agua
    data.tipo = "Sensor de Agua";
    data.estado_fuga = payload.object.WATER_LEAK_STATUS;
    data.veces_fuga = payload.object.WATER_LEAK_TIMES;
    data.duracion_ultima_fuga = payload.object.LAST_WATER_LEAK_DURATION;
    data.alarma = payload.object.ALARM;
}

// Extraer datos de señal y ubicación del primer gateway disponible
if (payload.rxInfo.length > 0) {
    data.rssi = payload.rxInfo[0].rssi;
    data.snr = payload.rxInfo[0].snr;
    data.latitud = payload.rxInfo[0].location.latitude;
    data.longitud = payload.rxInfo[0].location.longitude;
}

// Devolver datos procesados
msg.payload = data;
return msg;
