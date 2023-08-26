
/* Fonctionnement :
Attends l'instructionde la part du programme python 
pour déclencher une mesure et l'envoi des données
Applique un filtre pour que les données envoyées aient 
une différence d'au moins 0,1 point */

#include <Arduino.h>

byte comm;

#define msr A0
int msrValue;
float data;
float data_max;
float dataGo;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() >0){
    comm = Serial.read();
    if(comm == '1'){
      msrValue = analogRead(msr);
      data = ((float)(msrValue - 512) * 5 / 0.195) / 1024;
      if (data < 0){
        data = 0.00;
      }

      if (data > data_max){
        data_max = data;
      }

      if (abs(dataGo - data) > 0.1 || data == data_max){
        dataGo = data;
      }

      Serial.print(String(dataGo));
      Serial.flush();
    }
  }
}
