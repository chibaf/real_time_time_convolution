// analog-plot
// 
// Read analog values from A0 and A1 and print them to serial port.
//
// electronut.in
 
#include "Arduino.h"
 
void setup()
{
  // initialize serial comms
  Serial.begin(9600); 
}

int i=0,j=0;
float x,y;
float pi=3.1415927; 
void loop()
{
  // read A0
  if (i==99) i=0;
  x=pi*float(i)/50.0;
  y=pi*float(i+30)/50.0;
  float val1 = sin(x);
  float val2 = cos(y);
  if (val1 < 0.0) {val1=0;}
  if (val2 < 0.0) {val2=0;}
  i=i+1;j=j+1;
  // read A1
  //int val2 = random(100)/100.0;
  // print to serial
//  Serial.flush();
  delay(100);
  Serial.print(j*0.1);
  Serial.print(" ");
  Serial.print(val1);
  Serial.print(" ");
  Serial.println(val2);
//  Serial.println(" ");
//  Serial.print(val2);
  // wait 
}
