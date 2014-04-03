import smtplib
import threading
import time
import datetime
import subprocess
from email.mime.text import MIMEText

class LabMember:
    present = False
    water = 0
    
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

andy = LabMember("Andy", "Andy", "DeSoto", "DeSoto", "Mister", "5A", "@kadesoto")
adam = LabMember("Adam", "Adam", "Putnam", "Putnam", "Mister", "D8", "@adamlputnam")
jason = LabMember("Jason", "Jason", "Finley", "Finley", "Doctor", "5C", "@jasonrfinley")
john = LabMember("John", "John", "Nestojko", "Nestoyko", "Doctor", "E7", "")
victor = LabMember("Victor", "Victor", "Sungkhasettee", "Sung Ka Settee", "Mister", "85", "")
julie = LabMember("Julie", "Julie", "Gray", "Gray", "Miss", "CE", "@joule")
pooja = LabMember("Pooja", "Pooja", "Agarwal", "Agarwal", "Doctor", "27" , "@poojaagarwal")
meghan = LabMember("Meghan", "Megan", "McDoniel", "McDoniel", "Miss", "08", "")
allison = LabMember("Allison", "Allison", "Obenhaus", "Obenhaus", "Miss", "B8", "@allisonobenhaus")
roddy = LabMember("Roddy", "Roddy", "Roediger", "Roediger", "Doctor", "XX", "")

lab = [andy, adam, jason, john, victor, julie, pooja, meghan, allison, roddy]

def main():
    print("In main.")

def swipe(swipeCode):
    print("Swiping... " + swipeCode)
    
    for x in lab:
      if x.RFIDCode == swipeCode and x.present == False:
         if x.twitterHandle != "":
            temporaryTwitterHandle = " (" + x.twitterHandle + ") "
         else:
            temporaryTwitterHandle = ""
         sendIFTTTEmail("Tweet #tweet", x.firstName + temporaryTwitterHandle + "has checked into the Memory Lab.")
         print("Welcome to the Memory Lab, " + x.title + " " + x.firstNamePhonetic + " " + x.lastNamePhonetic)
         x.timeIn = datetime.datetime.now()
         x.present = True
         
      elif x.RFIDCode == swipeCode and x.present == True:
         if x.twitterHandle != "":
            temporaryTwitterHandle = " (" + x.twitterHandle + ") "
         else:
            temporaryTwitterHandle = ""
         sendIFTTTEmail("Tweet #tweet", x.firstName + temporaryTwitterHandle + "has checked out of the Memory Lab.")
         print("Farewell, " + x.title + " " + x.lastNamePhonetic)
         x.timeOut = datetime.datetime.now()
         x.present = False
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
    print("Ready.")
    s.close()
    
def BBCAlert():
    print("The BBC colloquium is about to start.")
    
def labMeetingAlert():
    print("The Roediger lab meeting is about to start.")    

reportIP()
main()
swipe("5A")
time.sleep(10)
swipe("5A")
