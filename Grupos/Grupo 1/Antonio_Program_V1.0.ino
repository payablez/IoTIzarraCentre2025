#include <Servo.h>
Servo myservo;
int pos=0;

void setup() {
  myservo.attach(7);  // servo en el pin 2
  myservo.write(pos);
}

void loop() {
  delay (1000);
  for (pos = 0; pos <= 180; pos += 15) {
    myservo.write(pos);
    delay(15);
  }

  for (pos = 180; pos >= 0; pos -= 15) {
    myservo.write(pos);
    delay(15);
  }
}
