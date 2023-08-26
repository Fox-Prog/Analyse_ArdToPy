
/* Fonctionnement :
Envoie les données directement lorsqu'il y a une 
variation d'au moins 0,1 point */



#include <Arduino.h>

byte comm;

#define msr A0
int msrValue;
float data;
float dataMax;
float dataGo;


void setup() {
  Serial.begin(9600);
}

void loop() {

  if(Serial.available() > 0){
    comm = Serial.read();
    if(comm == '1'){
        msrValue = analogRead(msr);
        data = ((float)(msrValue - 512) * 5 / 0.195) / 1024;

        if(data < 0){
          data = 0.00;
        }

        if(data > dataMax){
          dataMax = data;
          dataGo = data;
        }
        else if(abs(data-dataGo) > 0.15){
          dataGo = data;
        }
        Serial.println(String(dataGo));
        Serial.flush();
      }
    }
  }



