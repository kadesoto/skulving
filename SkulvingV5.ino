#include <MemoryFree.h>
#include <TimeAlarms.h>
#include <Time.h>
#include <FatReader.h>
#include <SdReader.h>
#include <WaveHC.h>
#include <WaveUtil.h>

SdReader memcard;
FatVolume vol;
FatReader root;
FatReader file;
WaveHC wave;

#define ENABLE 7      // Set the pin number for enabling the RFID reader. The Audio Shield uses pins 2-5.

int  val = 0; 
char code[10];
int bytesread = 0; 
String filename = "";
String codeString = "";
char *filenameChar;

#define roddyCode "DD6"
#define andyCode "D5A"
#define adamCode "8D8"
#define jasonCode "F5C"
#define johnCode "6E7"
#define victorCode "285"
#define julieCode "6CE"
#define poojaCode "227"
#define maryCode "251"
#define guest1Code "608"
#define guest2Code "67E"
#define guest3Code "CB8"

#define theKingCode "AB1"

String wav  = ".wav"; // here's the wave suffix we add on to save SRAM

boolean andyPresent = false;
boolean adamPresent = false;
boolean jasonPresent = false;
boolean johnPresent = false;
boolean victorPresent = false;
boolean juliePresent = false;
boolean poojaPresent = false;

byte andyTimeIn = 0;
byte adamTimeIn = 0;
byte jasonTimeIn = 0;
byte johnTimeIn = 0;
byte victorTimeIn = 0;
byte julieTimeIn = 0;
byte poojaTimeIn = 0;

byte userTimeIn = 0;

void setup() { 
  Serial.begin(2400);        
  pinMode(ENABLE, OUTPUT);     
  digitalWrite(ENABLE, LOW);  // activate the RFID reader

  pinMode(2, OUTPUT); 
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);

  if (!memcard.init()) {
    //putstring_nl("Card initialization failed!"); 
    cardErrorCheck();
    return;
  }
  
  //memcard.partialBlockRead(true);
 
  uint8_t partition;
  for (partition = 0; partition < 5; partition++) {
    if (vol.init(memcard, partition))
      break;
  }
  if (partition == 5)
  {
    //putstring_nl("No valid FAT partition");
    cardErrorCheck();
    while(1); 
  }

  if (!root.openRoot(vol))
  {
    //putstring_nl("Can't open root directory");
    while(1); 
  }
  //putstring_nl("Ready to go");
  
  playFile("I" + wav); 
  
  setTime(8,30,0,1,7,13); // sets time for 9 AM June 11 2013... I think
  
  Alarm.timerRepeat(3600, newHourAlert); 
  Alarm.timerOnce(300, emoteEffect);
  Alarm.alarmRepeat(dowMonday, 13, 20, 0, labMeetingAlert); // lab meeting
  Alarm.alarmRepeat(dowWednesday, 12, 50, 0, coreLabMeetingAlert); // core lab meeting
  Alarm.alarmRepeat(dowWednesday, 15, 50, 0, BBCAlert); // BBC colloquium
}

void cardErrorCheck(void)
{
  if(!memcard.errorCode()) return;
  //putstring("\n\rSD I/O error:");
  //Serial.print(memcard.errorCode());
  //putstring(", ");
  //Serial.print(memcard.errorData());
  while(1); // Stick here if there is an error
}

void loop() { 
  
  //Serial.print(F("freeMemory()="));
  //Serial.println(freeMemory());

  delay(1000);
  
  Alarm.delay(1000);
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
    Serial.end();
    digitalWrite(ENABLE, HIGH);

    String identity = swipeCode.substring(7);   

    if (identity == andyCode && andyPresent == false) checkin(1); 
    else if (identity == andyCode && andyPresent == true) checkout(1);
    else if (identity == adamCode && adamPresent == false) checkin(2);
    else if (identity == adamCode && adamPresent == true) checkout(2);
    else if (identity == jasonCode && jasonPresent == false) checkin(3);
    else if (identity == jasonCode && jasonPresent == true) checkout(3);
    else if (identity == johnCode && johnPresent == false) checkin(4);
    else if (identity == johnCode && johnPresent == true) checkout(4);
    else if (identity == victorCode && victorPresent == false) checkin(5);
    else if (identity == victorCode && victorPresent == true) checkout(5);    
    else if (identity == julieCode && juliePresent == false) checkin(6);
    else if (identity == julieCode && juliePresent == true) checkout(6);
    else if (identity == poojaCode && poojaPresent == false) checkin(7);
    else if (identity == poojaCode && poojaPresent == true) checkout(7);
    
    else if (identity == maryCode) checkin(8);
    else if (identity == guest1Code) checkin(9);
    else if (identity == guest2Code) checkin(10);
    else if (identity == guest3Code) checkin(11);
    else if (identity == roddyCode) checkin(0);
    
    else if (anyonePresent() && (identity == theKingCode)) playFile("HCTK" + wav);
    
    delay(5000);
    digitalWrite(ENABLE, LOW);
    Serial.begin(2400);
}

void checkin(byte name) {
  
  playFile("H" + String(name) + wav);
  
  if (name <= 7 && name > 0) {
  
    delay(6000);
    
    if (anyonePresent() == false) {
      playFile("A" + wav);
    }
    else playFile("NA" + wav);
    
    switch (name) {
      case 1:
        andyPresent = true;
        andyTimeIn = hour();
        break;
      case 2:
        adamPresent = true;
        adamTimeIn = hour();  
        break;
      case 3:
        jasonPresent = true;
        jasonTimeIn = hour();
        break;
      case 4:
        johnPresent = true;
        johnTimeIn = hour();
        break;
      case 5:
        victorPresent = true;
        victorTimeIn = hour();
        break;
      case 6:
        juliePresent = true;
        julieTimeIn = hour();
        break;
      case 7:
        poojaPresent = true;
        poojaTimeIn = hour();
        break;
      default: 
        // do this stuff
        break;
      }
    }
}

void checkout(byte name) {
  
  if (name <= 7 && name > 0) {
  
    playFile("B" + String(name) + wav);

    switch (name) {
      case 1:
        userTimeIn = andyTimeIn;
        andyPresent = false;
        break;
      case 2:
        userTimeIn = adamTimeIn;
        adamPresent = false;
        break;
      case 3:
        userTimeIn = jasonTimeIn;
        jasonPresent = false;
        break;
      case 4:
        userTimeIn = johnTimeIn;
        johnPresent = false;
        break;
      case 5:
        userTimeIn = victorTimeIn;
        victorPresent = false;
        break;
      case 6:
        userTimeIn = julieTimeIn;
        juliePresent = false;
        break;
      case 7:
        userTimeIn = poojaTimeIn;
        poojaPresent = false;
        break;
      default: 
        // do this stuff
        break;
      }
   
      delay(6000);
      
      if ((hour() - userTimeIn) >= 10) playFile ("10H" + wav);
      else playFile(String(hour() - userTimeIn) + "H" + wav);
   }
}
    
void playFile(String name) {
  if (wave.isplaying == false) {
    filenameChar = &name[0];
    if (!file.open(root, filenameChar)) {
        return;
     }
     if (!wave.create(file)) {
       return;
     }
     wave.play();
  }
}

void silence() {
  if(wave.isplaying) {
    wave.stop();
  }
}

void coreLabMeetingAlert() {
   if (anyonePresent()) playFile("M1" + wav);
}

void labMeetingAlert() {
  if (anyonePresent()) playFile("M2" + wav);
}

void BBCAlert() {
   if (anyonePresent()) playFile("M3" + wav);
}

void newHourAlert() {
   if (anyonePresent()) playFile("T" + wav);
}

void emoteEffect() {
  if (anyonePresent()) {
    playFile("F" + String(byte(random(1, 10))) + wav);
  }
  
  Alarm.timerOnce(random(900, 2700), emoteEffect);
}

boolean anyonePresent() {
  if (andyPresent || adamPresent || jasonPresent || johnPresent || juliePresent || victorPresent || poojaPresent) return true;
  else return false;
}

