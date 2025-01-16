#include <Servo.h>
#define numOfValsRec 5
#define digitsPerValRec 1

Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;

int valsRec[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1; //$00000
int counter = 0;

bool counterStart = false;

String receivedString;

void setup() {
  Serial.begin(9600);
  servoThumb.attach(7);
  servoIndex.attach(6);
  servoMiddle.attach(5);
  servoRing.attach(4);
  servoPinky.attach(3);

  servoThumb.write(180);
  servoIndex.write(180);
  servoMiddle.write(180);
  servoRing.write(180);
  servoPinky.write(180);
}

void receivedData(){
  while(Serial.available()){
    char caracter = Serial.read();

    if(caracter == '$'){
      counterStart = true;
    }

    if(counterStart){
      if(counter < stringLength){
        receivedString = String(receivedString + caracter);
        counter++;
      }

      if(counter >= stringLength){
        //$00000
        for (int i = 0; i < numOfValsRec; i++) {
          int num = (i * digitsPerValRec) + 1;
          valsRec[i] = receivedString.substring(num, num + digitsPerValRec).toInt();
          Serial.print(valsRec[i]);
        }
        receivedString = "";
        counter = 0;
        counterStart = false;
        Serial.println("");
      }
    }
  }
}

void loop() {
  receivedData();
  if(valsRec[0] == 1){servoThumb.write(180);} else{servoThumb.write(0);}
  if(valsRec[1] == 1){servoIndex.write(180);} else{servoIndex.write(0);}
  if(valsRec[2] == 1){servoMiddle.write(180);} else{servoMiddle.write(0);}
  if(valsRec[3] == 1){servoRing.write(180);} else{servoRing.write(0);}
  if(valsRec[4] == 1){servoPinky.write(180);} else{servoPinky.write(0);}
}
