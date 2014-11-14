import serial
import smtplib
import threading
import time
import datetime
import subprocess
from apscheduler.scheduler import Scheduler
from email.mime.text import MIMEText

class LabMember:
    present = False
    
    def __init__(self, firstName, firstNamePhonetic, lastName, lastNamePhonetic, title, RFIDCode, twitterHandle):
        self.firstName = firstName
        self.firstNamePhonetic = firstNamePhonetic
        self.lastName = lastName
        self.lastNamePhonetic = lastNamePhonetic
        self.title = title
        self.RFIDCode = RFIDCode
        self.twitterHandle = twitterHandle
    
USERNAME = "skulving@technimentis.com"
PASSWORD = "tulvingtulving"

ser = serial.Serial('/dev/ttyACM0', 2400)

andy = LabMember("Andy", "Andy", "DeSoto", "DeSoto", "Mister", "27", "@kadesoto")
adam = LabMember("Adam", "Adam", "Putnam", "Putnam", "Mister", "D8", "@adamlputnam")
jason = LabMember("Jason", "Jason", "Finley", "Finley", "Doctor", "5C", "@jasonrfinley")
john = LabMember("John", "John", "Nestojko", "Nestoyko", "Doctor", "E7", "")
victor = LabMember("Victor", "Victor", "Sungkhasettee", "Sung Ka Settee", "Mister", "85", "")
lena = LabMember("Lena", "Leena", "Abel", "Awbel", "Doctor", "D6" , "")
roddy = LabMember("Roddy", "Roddy", "Roediger", "Roediger", "Doctor", "43", "")

julie = LabMember("Julie", "Julie", "Gray", "Gray", "Miss", "CE", "@joule")
pooja = LabMember("Pooja", "Pooja", "Agarwal", "Agarwal", "Doctor", "XX" , "@poojaagarwal")
meghan = LabMember("Meghan", "Megan", "McDoniel", "McDoniel", "Miss", "08", "")
allison = LabMember("Allison", "Allison", "Obenhaus", "Obenhaus", "Miss", "B8", "@allisonobenhaus")

# Andy's was 5A, Pooja's was 27

lab = [andy, adam, jason, john, victor, lena, roddy]
alllab = [lab, julie, pooja, meghan, allison]

def main():    
    sched = Scheduler()
    sched.start()
    
    sched.add_cron_job(BBCAlert, day_of_week='wed', hour = '15', minute = '55') # BBC Alert should go off at 3:55 PM Wednesdays
    sched.add_cron_job(labMeetingAlert, day_of_week='wed', hour = '10', minute = '25') # lab meeting alert should go off at 10:25 AM Mondays
    sched.add_cron_job(checkoutEveryone, hour = '23', minute = '55') # reset daily variables at 11:55 PM every day
    
    while 1 :
        #print("Listening for serial input...") # for debug
        serialInput = ser.readline()
        serialInput = serialInput.strip()
        if len(serialInput) == 10:
            #print ("Found serial input! Trimming it...") # for debug
            swipe(serialInput[-2:]) # get the last 2 characters of the serial input (i.e., RFID tag)
                                         

def swipe(swipeCode):
    print("Swiping... " + swipeCode)
    
    for x in lab:
      if x.RFIDCode == swipeCode and x.present == False:
         if x.twitterHandle != "":
            temporaryTwitterHandle = " (" + x.twitterHandle + ")"
         else:
            temporaryTwitterHandle = ""
         sendIFTTTEmail("Tweet #tweet", x.firstName + temporaryTwitterHandle + " has checked into the Memory Lab.")
         
         if x == lena:
            speakGerman("Willkommen im Labor, Frau Doktor Abel")
         else:
            speak("Welcome to the Memory Lab, " + x.title + " " + x.firstNamePhonetic + " " + x.lastNamePhonetic)
         
         x.timeIn = datetime.datetime.now()
         x.present = True
         
      elif x.RFIDCode == swipeCode and x.present == True:
         if x.twitterHandle != "":
            temporaryTwitterHandle = " (" + x.twitterHandle + ")"
         else:
            temporaryTwitterHandle = ""
         sendIFTTTEmail("Tweet #tweet", x.firstName + temporaryTwitterHandle + " has checked out of the Memory Lab.")
         
         if x == lena:
            speakGerman("Auf Wiedersehen, Frau Doktor Abel")
         else:   
            speak("Farewell, " + x.title + " " + x.lastNamePhonetic)
         
         x.timeOut = datetime.datetime.now()
         x.present = False
         time.sleep(5)
         sendIFTTTEmail(x.firstName + " " + x.lastName + " #loghours", str(x.timeOut - x.timeIn))

def checkoutEveryone():
    for x in lab:
      x.present = False  

def sendIFTTTEmail(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = USERNAME
    msg["To"] = "trigger@ifttt.com"
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(USERNAME, PASSWORD)
    server.sendmail(USERNAME, "trigger@recipe.ifttt.com", msg.as_string())
    server.quit()
    print("Email hopefully sent...")

def reportIP():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    msg = MIMEText("")
    msg["Subject"] = "Skulving running at: " + s.getsockname()[0]
    msg["From"] = USERNAME
    msg["To"] = "kadesoto@gmail.com"
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(USERNAME, PASSWORD)
    server.sendmail(USERNAME, "kadesoto@gmail.com", msg.as_string())
    server.quit()
    print("Email hopefully sent...")
    speak("Ready.")
    s.close()

def speak(speechString):
    subprocess.call(["/home/pi/git/skulving/speech.sh", speechString])
    
def speakGerman(speechString):
    subprocess.call(["/home/pi/git/skulving/speech_de.sh", speechString])
    
def BBCAlert():
    speak("The BBC colloquium is about to start.")
    
def labMeetingAlert():
    speak("The Roediger lab meeting is about to start.")    

reportIP()
main()
