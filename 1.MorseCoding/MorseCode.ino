const int buttonPin = 2;
const int greenLedPin = 12;
const int redLedPin =  13;

const float T = 500;
const float dotTime = T;  //Endre disse til noe som passer
const float dashTime = 3*T;
const float letterPauseTime = 3*T;
const float wordPauseTime = 7*T;

const int dotSignal = 0;
const int dashSignal = 1;
const int letterPauseSignal = 2;
const int wordPauseSignal = 3;

int previousButtonState = LOW;

long previousButtonChangeTime = millis();
long lastSentMessageTime = millis();

boolean hasSentLetterPauseSinceLastMessage = true;
boolean hasSentWordPauseSinceLastMessage = true;

void setup() {
    Serial.begin(9600);
    
    // initialize the LED pin as an output:
    pinMode(greenLedPin, OUTPUT);
    pinMode(redLedPin, OUTPUT);
    
    // initialize the pushbutton pin as an input:
    pinMode(buttonPin, INPUT);   
}

void loop() {
    int buttonState = digitalRead(buttonPin);

    //Sjekker aktive press
    if (previousButtonState == HIGH && buttonState == LOW) {
        long deltaSinceButtonChange = millis() - previousButtonChangeTime;
        
        if (deltaSinceButtonChange > dotTime) {
            digitalWrite(greenLedPin, HIGH);
            digitalWrite(redLedPin, LOW);
            Serial.print(dashSignal);
        } else {
            digitalWrite(redLedPin, HIGH);
            digitalWrite(greenLedPin, LOW);
            Serial.print(dotSignal);
        }
        lastSentMessageTime = millis();
        hasSentLetterPauseSinceLastMessage = false;
        hasSentWordPauseSinceLastMessage = false;
    }


    //Sjekker pausene
    long deltaSinceLastMessage = millis() - lastSentMessageTime;
    if(deltaSinceLastMessage > 700){
      digitalWrite(redLedPin,LOW);
      digitalWrite(greenLedPin,LOW);
    }
    if (deltaSinceLastMessage > letterPauseTime && deltaSinceLastMessage < wordPauseTime && !hasSentLetterPauseSinceLastMessage) {
        
        Serial.print(letterPauseSignal);
        hasSentLetterPauseSinceLastMessage = true;
    
    } else if (deltaSinceLastMessage > wordPauseTime && !hasSentWordPauseSinceLastMessage) {
        
        Serial.print(wordPauseSignal);
        hasSentWordPauseSinceLastMessage = true;
    
    }
    

    if (previousButtonState != buttonState) {
        previousButtonState = buttonState;
        previousButtonChangeTime = millis();
    }

    // A tiny delay to remove some latency issues
    delay(20);
}
