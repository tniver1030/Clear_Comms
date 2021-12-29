
#include <Bounce.h>
// constants won't change. They're used here to set pin numbers:
const int buttonPin = 23;         // the number of the pushbutton pin
int buttonState = 0;         // variable for reading the pushbutton status
Bounce pushbutton = Bounce(buttonPin, 50);

void setup() {
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT_PULLUP);
  digitalWrite(buttonPin, HIGH);
  Serial.begin(9600);
}

void loop() {
  // read the state of the pushbutton value:
  pushbutton.update();  
  if(pushbutton.fallingEdge()){
    Keyboard.press(MODIFIERKEY_RIGHT_CTRL); 
    
  }
  if(pushbutton.risingEdge()){
    Keyboard.release(MODIFIERKEY_RIGHT_CTRL); 
  }
}
