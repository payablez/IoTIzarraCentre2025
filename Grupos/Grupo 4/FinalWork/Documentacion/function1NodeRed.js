var payload = msg.payload;

// Etiquetas opcionales (puedes eliminarlas si no quieres)
var tags = {
    fuente: "sensorPIR"
};

// Campos numéricos
var fields = {
    detections: Number(payload.detections),
    detected: payload.detected ? 1 : 0
};

// Timestamp en nanosegundos
let time = new Date().toLocaleString();  // Esto te dará la fecha y hora en formato local


// Construcción del objeto para InfluxDB
msg.payload = {
    measurement: "detecciones",
    detections: Number(payload.detections),
    detected: payload.detected ? 1 : 0,
    String : time
};

return msg;
