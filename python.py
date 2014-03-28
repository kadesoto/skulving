import serial
import smtplib
import threading
import time
from datetime import datetime
from apscheduler.scheduler import Scheduler
from email.mime.text import MIMEText

USERNAME = "skulving@technimentis.com"
PASSWORD = "tulvingtulving"

ser = serial.Serial('/dev/ttyACM0', 2400)

andyCode = "5X" # changed in order to test the water functionality
adamCode = "D8"
jasonCode = "5C"
johnCode = "E7"
victorCode = "85"
julieCode = "CE"
poojaCode = "27"
meghanCode = "08"
allisonCode = "B8"

andyWaterCode = "5A"

andyPresent = False
adamPresent = False
jasonPresent = False
johnPresent = False
victorPresent = False
juliePresent = False
poojaPresent = False
meghanPresent = False
allisonPresent = False

andyWater = 0;

def main():    
    sched = Scheduler()
    sched.start()
    
    sched.add_cron_job(BBCAlert, day_of_week='wed', hour = '15', minute = '55') # BBC Alert should go off at 3:55 PM Wednesdays
    sched.add_cron_job(labMeetingAlert, day_of_week='mon', hour = '10', minute = '25') # lab meeting alert should go off at 10:25 AM Mondays
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
    global andyPresent # apparently doing this is awful practice, but we'll do it anyway
    global adamPresent
    global jasonPresent
    global johnPresent
    global victorPresent
    global juliePresent
    global poojaPresent
    global meghanPresent
    global allisonPresent
    
    global andyWater
    
    andywater = 0

    if (swipeCode == andyCode) and (andyPresent == False):
        sendIFTTTEmail("Andy (@kadesoto) has checked in to the Memory Lab.")
        speak("Identity authorized. Welcome to the Memory Lab, Mister Andy DeSoto.")
        andyPresent = True
    elif (swipeCode == adamCode) and (adamPresent == False):
        sendIFTTTEmail("Adam (@adamlputnam) has checked in to the Memory Lab.")
        speak("Identity authorized. Welcome to the Memory Lab, Mister Adam Putnam.")
        adamPresent = True
    elif (swipeCode == jasonCode) and (jasonPresent == False):
        sendIFTTTEmail("Jason has checked in to the Memory Lab.")
        speak("Identity authorized. Welcome to the Memory Lab, Doctor Jason Finley.")
        jasonPresent = True
    elif (swipeCode == johnCode) and (johnPresent == False):
        sendIFTTTEmail("John has checked in to the Memory Lab.")
        speak("Identity authorized. Welcome to the Memory Lab, Doctor John Nestoyko.")
        johnPresent = True
    elif (swipeCode == victorCode) and (victorPresent == False):
        sendIFTTTEmail("Victor has checked in to the Memory Lab.")
        speak("Identity authorized. Welcome to the Memory Lab, Mister Victor Sunkasetty.")
        victorPresent = True
    elif (swipeCode == julieCode) and (juliePresent == False):
        sendIFTTTEmail("Julie has checked in to the Memory Lab.")
        speak("Identity authorized. Welcome to the Memory Lab, Miss Julie Gray.")
        juliePresent = True
    elif (swipeCode == poojaCode) and (poojaPresent == False):
        sendIFTTTEmail("Pooja (@poojaagarwal) has checked in to the Memory Lab.")
        speak("Identity authorized. Welcome to the Memory Lab, Doctor Pooja Agarwal.")
        poojaPresent = True
    elif (swipeCode == meghanCode) and (meghanPresent == False):
        sendIFTTTEmail("Meghan has checked in to the Memory Lab.")
        speak("Identity authorized. Welcome to the Memory Lab, Miss Megan McDonyel.")
        meghanPresent = True
    elif (swipeCode == allisonCode) and (allisonPresent == False):
        sendIFTTTEmail("Allison (@allisonobenhaus) has checked in to the Memory Lab.")
        speak("Identity authorized. Welcome to the Memory Lab, Miss Allison Obenhaus.")
        allisonPresent = True
    elif (swipeCode == andyCode) and (andyPresent == True):
        sendIFTTTEmail("Andy (@kadesoto) has checked out of the Memory Lab.")
        speak("Goodbye, Mister DeSoto. You have checked out.")
        andyPresent = False
    elif (swipeCode == adamCode) and (adamPresent == True):
        sendIFTTTEmail("Adam (@adamlputnam) has checked out of the Memory Lab.")
        speak("Goodbye, Mister Putnam. You have checked out.")
        adamPresent = False
    elif (swipeCode == jasonCode) and (jasonPresent == True):
        sendIFTTTEmail("Jason has checked out of the Memory Lab.")
        speak("Goodbye, Doctor Finley. You have checked out.")
        jasonPresent = False
    elif (swipeCode == johnCode) and (johnPresent == True):
        sendIFTTTEmail("John has checked out of the Memory Lab.")
        speak("Goodbye, Doctor Nestoyko. You have checked out.")
        johnPresent = False
    elif (swipeCode == victorCode) and (victorPresent == True):
        sendIFTTTEmail("Victor has checked out of the Memory Lab.")
        speak("Goodbye, Mister Sunkasetty. You have checked out.")
        victorPresent = False
    elif (swipeCode == julieCode) and (juliePresent == True):
        sendIFTTTEmail("Julie has checked out of the Memory Lab.")
        speak("Goodbye, Miss Gray. You have checked out.")
        juliePresent = False
    elif (swipeCode == poojaCode) and (poojaPresent == True):
        sendIFTTTEmail("Pooja (@poojaagarwal) has checked out of the Memory Lab.")
        speak("Goodbye, Doctor Agarwal. You have checked out.")
        poojaPresent = False
    elif (swipeCode == meghanCode) and (meghanPresent == True):
        sendIFTTTEmail("Meghan has checked out of the Memory Lab.")
        speak("Goodbye, Miss McDonyel. You have checked out.")
        meghanPresent = False
    elif (swipeCode == allisonCode) and (allisonPresent == True):
        sendIFTTTEmail("Allison (@allisonobenhaus) has checked out of the Memory Lab.")
        speak("Goodbye, Miss Obenhaus. You have checked out.")
        allisonPresent = False
        
    elif (swipeCode == andyWaterCode):
        if (andyWater == 1):
            speak("Andy, you have had 1 bottle of water today.")
            sendIFTTTEmail("Andy (@kadesoto) has filled up his water bottle (1 time today).")
        else:
            speak("Andy, you have had " + str(andyWater) + " bottles of water today.")
            sendIFTTTEmail("Andy (@kadesoto) has filled up his water bottle (" + str(andyWater) + " times today).")
        andyWater = andyWater + 1
           

def checkoutEveryone():
    global andyPresent
    global adamPresent
    global jasonPresent
    global johnPresent
    global victorPresent
    global juliePresent
    global poojaPresent
    global meghanPresent
    global allisonPresent
    
    global andyWater
    
    andyPresent = False
    adamPresent = False
    jasonPresent = False
    johnPresent = False
    victorPresent = False
    juliePresent = False
    poojaPresent = False
    meghanPresent = False
    allisonPresent = False

def sendIFTTTEmail(subject):
    msg = MIMEText("")
    msg["Subject"] = subject
    msg["From"] = USERNAME
    msg["To"] = "trigger@ifttt.com"
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(USERNAME, PASSWORD)
    server.sendmail(USERNAME, "trigger@ifttt.com", msg.as_string())
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
    speak("Ready for action.")
    s.close()

def speak(speechString):
    subprocess.call(["./Speech.sh", speechString])
    
def BBCAlert():
    speak("The BBC colloquium is about to start.")
    
def labMeetingAlert():
    speak("The Roediger lab meeting is about to start.")    

reportIP()
main()
