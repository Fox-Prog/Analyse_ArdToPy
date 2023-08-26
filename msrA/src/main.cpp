#include <Arduino.h>

// ___________________________________________________ VARIABLES ___________________________________________________ //

byte comm;

#define msr A0
int msrValue;
float data;

#define relay 2
#define DP 10
#define DM 9

float R1_value = 0;
float R2_value = 0;

const int bufferSize = 32;
char buffer[32];
float receivedValue;
float rValuePython;

// ___________________________________________________ FONCTIONS ___________________________________________________ //

void listen(){
  if (Serial.available()>0){
    int bytesRead = Serial.readBytesUntil('\n', buffer, bufferSize - 1);
    buffer[bytesRead] = '\0';  // Ajout d'un caractère de fin de chaîne
    receivedValue = atof(buffer);
    rValuePython = receivedValue;
    memset(buffer, 0, bufferSize);
  }
  else {
    listen();
  }
}

void send(String data){
  Serial.print(data);
  Serial.flush();
}

void send_result(){
  Serial.print(String(5/(255/R1_value))+"/"+String(5/(255/R2_value))+"/"+String(data));
  Serial.flush();
}

// ___________________________________________________ PROTOCOL ___________________________________________________ //

void protocol(char x) {
  if (Serial.available()>0){
    comm = Serial.read();
    if(comm == x){
      analogWrite(DP, R1_value);
      analogWrite(DM, R2_value);

      delay(1000);

      digitalWrite(relay, HIGH);
      delay(20000);

      msrValue = analogRead(msr);
      data = ((float)(msrValue - 512) * 5 / 0.195) / 1024;

      send_result();
      
      digitalWrite(relay, LOW);
    }
  }
  else {
    protocol(x);
  }
}

// ___________________________________________________ MODE AUTO ___________________________________________________ //

void mode_auto(){
  for (int c1=0; c1<32; c1++){
    for (int c2=0; c2<32; c2++){
      R1_value = (c1*5);
      R2_value = (c2*5);

      protocol('1');
    }
  }
  Serial.print("Mode auto termine");
}

// ___________________________________________________ MODE MANU ___________________________________________________ //

void mode_manu(){
  while(true){
    listen();
    R1_value = round(255/(5/rValuePython));
    send("received");
    listen();
    R2_value = round(255/(5/rValuePython));
    send("received");
    protocol('2');
  }
}

// ___________________________________________________ SETUP // LOOP ___________________________________________________ //

void setup() {
  pinMode(msr, INPUT);
  pinMode(relay, OUTPUT);
  pinMode(DP, OUTPUT);
  pinMode(DM, OUTPUT);

  Serial.begin(9600);
}

void loop() {

  if(Serial.available() > 0){
    comm = Serial.read();
    if(comm == '1'){
      mode_auto();
    }

    if(comm == '2'){
      delay(500);
      send("Arduino : Mode manuel activé");
      mode_manu();
    }

    if(comm == '3'){
      delay(500);
      send("Arduino : Mode test activé");
      int v = 0;
      while(true){
        if (Serial.available()>0){
          comm = Serial.read();
          if(comm == '2'){
            v++;
          }
          if(comm == '1'){
            v--;
          }
          Serial.print("Valeur DP: ");
          Serial.print(v);

          float R = (5/(1024/v));

          Serial.print(" Converti: ");
          Serial.println(R);
          analogWrite(DP, v);
        }
      }
    }
  }
}
