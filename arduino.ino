#include <MemoryFree.h>

#define ENABLE 7      // Set the pin number for enabling the RFID reader. The Audio Shield uses pins 2-5.

int  val = 0; 
char code[10];
int bytesread = 0; 
String filename = "";
String codeString = "";
char *filenameChar;

void setup() { 
  Serial.begin(2400);
  digitalWrite(9, HIGH);
  digitalWrite(10, HIGH);  
  pinMode(ENABLE, OUTPUT);     
  digitalWrite(ENABLE, LOW);  // activate the RFID reader

  pinMode(2, OUTPUT); 
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
}

void loop() { 
  
  //Serial.print(F("freeMemory()="));
  //Serial.println(freeMemory());

  delay(1000);
  
  if(Serial.available() > 0) {          // if data available from reader  
    if((val = Serial.read()) == 10) {   // check for header 
      bytesread = 0; 
      while(bytesread<10) {              // read 10 digit code 
        if( Serial.available() > 0) { 
          val = Serial.read(); 
          if((val == 10)||(val == 13)) { // if header or stop bytes before the 10 digit reading 
            break;                       // stop reading 
          } 
          code[bytesread] = val;         // add the digit           
          bytesread++;                   // ready to read next digit  
        } 
      } 
      if(bytesread == 10) {              // if 10 digit read is complete 
        
        codeString = (String)code;
        codeString.trim();              // trims the code to one line (for some reason it was longer)
        
        swipe(codeString);
        //Serial.print("Swiping TAG code: ");   // possibly a good TAG 
        //Serial.println(codeString);            // print the TAG code 
        Serial.flush();                  // Flush the serial buffer before trying to read a new code
      } 
      bytesread = 0; 
    }
  }
} 

void swipe(String swipeCode) {
    Serial.println(swipeCode);
    Serial.end();
    digitalWrite(ENABLE, HIGH);    
    delay(5000);
    digitalWrite(ENABLE, LOW);
    Serial.begin(2400);
}
