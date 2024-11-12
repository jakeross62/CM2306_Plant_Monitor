#include <DHT.h>
#include <Wire.h>
#include "rgb_lcd.h"

#define DHTTYPE DHT11 
#define DHTPIN A0
rgb_lcd lcd;
const int ledPin = 4;
const int lcdPin = 3;
int colorR = 0;
int colorG = 255;
int colorB = 0;

DHT dht(DHTPIN, DHTTYPE);  
#if defined(ARDUINO_ARCH_AVR)
    #define debug  Serial

#elif defined(ARDUINO_ARCH_SAMD) ||  defined(ARDUINO_ARCH_SAM)
    #define debug  SerialUSB
#else
    #define debug  Serial
#endif

void setup() {
  // put your setup code here, to run once:
  lcd.begin(16, 2);
  lcd.setRGB(colorR, colorG, colorB);
  Serial.begin(30000);
  Wire.begin();
  dht.begin();
}

void loop() {
  int light = analogRead(A2);
  lcd.setCursor(0, 0);
  float temp_hum_val[2] = {0};
  light = map(light, 0, 800, 0, 10);

  for (int i = 0; i <= 255; i++){
    analogWrite(ledPin, i);
  }

  if (!dht.readTempAndHumidity(temp_hum_val)){
    
    Serial.println(temp_hum_val[0]); // Humidity
    Serial.println(temp_hum_val[1]); // Temperature
    Serial.println(light);

    lcd.clear();
    lcd.print("Temp: ");
    lcd.print(temp_hum_val[1]);
    lcd.print(" *C");

    if (temp_hum_val[1] > 40 || temp_hum_val[1] < 0){
      lcd.setRGB(255,0,0);
    }
    else{
      lcd.setRGB(0,255,0);
    }

    delay(10000);
    lcd.clear();
    lcd.print("Humidity: ");
    lcd.print(temp_hum_val[0]);
    lcd.print("%");
  
    if (temp_hum_val[0] < 20 || temp_hum_val[0] > 80){
      lcd.setRGB(255,0,0);
    }

    else{
      lcd.setRGB(0,255,0);
    }
    delay(10000);
    if (light <= 5){
      lcd.clear();
      lcd.print("Plant is dark!");
      lcd.setRGB(255, 0, 0);
    }
    else{
      lcd.clear();
      lcd.print("Plant is light!");
      lcd.setRGB(0, 255, 0);
    }
    delay(10000);
  }
  else{
    lcd.clear();
    lcd.println("Failed to get values, please check sensors.");
  }
}
