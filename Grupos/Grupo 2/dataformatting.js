var payload = msg.payload;

var deviceName = payload.deviceInfo.deviceName;
var deviceType = payload.deviceInfo.deviceProfileName;

// Inicializar 'fields' SIN timestamp
var data = {
    dispositivo: deviceName,
    devEUI: payload.deviceInfo.devEui
};

// Obtener timestamp en nanosegundos
var timestamp = new Date(payload.time).getTime() * 1000000;

var measurement = "";

// Verificar que payload.object existe
if (payload.object && typeof payload.object === 'object') {

    if (deviceType === "Dragino PB01") {
        measurement = "sensor_boton";

        if ("TempC_SHT41" in payload.object) {
            data.temperatura = payload.object.TempC_SHT41;
        }
        if ("Hum_SHT41" in payload.object) {
            data.humedad = payload.object.Hum_SHT41;
        }
        if ("BatV" in payload.object) {
            data.bateria = payload.object.BatV;
        }
        if ("Alarm" in payload.object) {
            data.alarma = payload.object.Alarm;
        }
        if ("Sound_ACK" in payload.object) {
            data.sonido = payload.object.Sound_ACK;
        }

    } else if (deviceType === "Puerta") {
        measurement = "sensor_puerta";

        if ("DOOR_OPEN_TIMES" in payload.object) {
            data.aperturas = payload.object.DOOR_OPEN_TIMES;
        }
        if ("LAST_DOOR_OPEN_DURATION" in payload.object) {
            data.duracion_ultima_apertura = payload.object.LAST_DOOR_OPEN_DURATION;
        }

    } else if (deviceType === "Sensor de agua") {
        measurement = "sensor_agua";

        if ("WATER_LEAK_STATUS" in payload.object) {
            data.estado_fuga = payload.object.WATER_LEAK_STATUS;
        }
        if ("WATER_LEAK_TIMES" in payload.object) {
            data.veces_fuga = payload.object.WATER_LEAK_TIMES;
        }
        if ("LAST_WATER_LEAK_DURATION" in payload.object) {
            data.duracion_ultima_fuga = payload.object.LAST_WATER_LEAK_DURATION;
        }
        if ("ALARM" in payload.object) {
            data.alarma = payload.object.ALARM;
        }
    }
}

// Señal y ubicación (opcional)
if (payload.rxInfo && payload.rxInfo.length > 0) {
    if (payload.rxInfo[0].rssi !== undefined) {
        data.rssi = payload.rxInfo[0].rssi;
    }
    if (payload.rxInfo[0].snr !== undefined) {
        data.snr = payload.rxInfo[0].snr;
    }
    if (payload.rxInfo[0].location) {
        data.latitud = payload.rxInfo[0].location.latitude;
        data.longitud = payload.rxInfo[0].location.longitude;
    }
}

// Asegurarse que 'timestamp' NO esté dentro de 'fields'
delete data.timestamp;

// Construir mensaje final
msg.measurement = measurement;
msg.payload = data;
/*msg.payload = {
    fields: data,
    tags: {
        dispositivo: deviceName,
        devEUI: payload.deviceInfo.devEui,
        tipo: deviceType
    },
    timestamp: timestamp
};*/

return msg;
