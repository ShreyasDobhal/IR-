
#include <IRremote.h>
//#include <IRremoteInt.h>

int RECV_PIN = 3;
int LED_PIN = 2;

// Create a new receiver object that would decode signals to key codes
IRrecv receiver(RECV_PIN);  
decode_results results;

int state = 0;
int timer = 0;

void setup() {
  Serial.begin(9600);
  receiver.enableIRIn();
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  if(receiver.decode(&results)) {
    Serial.println(results.value, HEX);
    receiver.resume();
    digitalWrite(LED_PIN, HIGH);
    timer = 1000;
    state = 1;
  }

  if (timer > 0) {
    timer -= 1;
  }

  if (timer <= 0 && state != 0) {
    digitalWrite(LED_PIN, LOW);
    state = 0;
  }
}
