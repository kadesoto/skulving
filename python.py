import serial
import smtplib
import subprocess
from email.mime.text import MIMEText
from time import strftime

USERNAME = "skulving@technimentis.com"
PASSWORD = "password"

andyCode = "5A"
adamCode = "D8"
jasonCode = "5C"
johnCode = "E7"
victorCode = "85"
julieCode = "CE"
poojaCode = "27"

andyPresent = False
adamPresent = False
jasonPresent = False
johnPresent = False
victorPresent = False
juliePresent = False
poojaPresent = False

def main():
   while 1: waitForSerial()

def swipe(swipeCode):
   print "Beginning swipe..."
   
   if (swipeCode == andyCode) and (andyPresent == False): checkIn("ANDY")
   elif (swipeCode == adamCode) and (adamPresent == False): checkIn("ADAM")
   elif (swipeCode == jasonCode) and (jasonPresent == False): checkIn("JASON")
   elif (swipeCode == johnCode) and (johnPresent == False): checkIn("JOHN")
   elif (swipeCode == victorCode) and (victorPresent == False): checkIn("VICTOR")
   elif (swipeCode == julieCode) and (juliePresent == False): checkIn("JULIE")
   elif (swipeCode == poojaCode) and (poojaPresent == False): checkIn("POOJA")
   elif (swipeCode == andyCode) and (andyPresent == True): checkOut("ANDY")
   elif (swipeCode == adamCode) and (adamPresent == True): checkOut("ADAM")
   elif (swipeCode == jasonCode) and (jasonPresent == True): checkOut("JASON")
   elif (swipeCode == johnCode) and (johnPresent == True): checkOut("JOHN")
   elif (swipeCode == victorCode) and (victorPresent == True): checkOut("VICTOR")
   elif (swipeCode == julieCode) and (juliePresent == True): checkOut("JULIE")
   elif (swipeCode == poojaCode) and (poojaPresent == True): checkOut("POOJA")

def checkIn(name):
   global andyPresent
   global adamPresent
   global jasonPresent
   global johnPresent
   global victorPresent
   global juliePresent
   global poojaPresent
   
   if name == "ANDY":
      sendIFTTTEmail("Andy (@kadesoto) has checked in to the #memorylab.")
      andyPresent = True
      andyTimeIn = strftime("%H:%M:%S")
   elif name == "ADAM":
      sendIFTTTEmail("Adam (@adamlputnam) has checked in to the #memorylab.")
      adamPresent = True
   elif name == "JASON":
      sendIFTTTEmail("Jason has checked in to the #memorylab.")
      jasonPresent = True
   elif name == "JOHN":
      sendIFTTTEmail("John has checked in to the #memorylab.")
      johnPresent = True
   elif name == "VICTOR":
      sendIFTTTEmail("Victor has checked in to the #memorylab.")
      victorPresent = True
   elif name == "JULIE":
      sendIFTTTEmail("Julie has checked in to the #memorylab.")
      juliePresent = True
   elif name == "POOJA":
      sendIFTTTEmail("Pooja (@poojaagarwal) has checked in to the #memorylab.")
      poojaPresent = True
   
def checkOut(name):
   global andyPresent
   global adamPresent
   global jasonPresent
   global johnPresent
   global victorPresent
   global juliePresent
   global poojaPresent
   
   if name == "ANDY":
      sendIFTTTEmail("Andy (@kadesoto) has checked out of the #memorylab.")
      andyPresent = False
   elif name == "ADAM":
      sendIFTTTEmail("Adam (@adamlputnam) has checked out of the #memorylab.")
      adamPresent = False
   elif name == "JASON":
      sendIFTTTEmail("Jason has checked out of the #memorylab.")
      jasonPresent = False
   elif name == "JOHN":
      sendIFTTTEmail("John has checked out of the #memorylab.")
      johnPresent = False
   elif name == "VICTOR":
      sendIFTTTEmail("Victor has checked out of the #memorylab.")
      victorPresent = False
   elif name == "JULIE":
      sendIFTTTEmail("Julie has checked out of the #memorylab.")
      juliePresent = False
   elif name == "POOJA":
      sendIFTTTEmail("Pooja (@poojaagarwal) has checked out of the #memorylab.")
      poojaPresent = False

def sendIFTTTEmail(subject):
   print("Preparing to send email...")
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
   print("Email sent successfully!")

def reportIP():
   import socket
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.connect(("8.8.8.8", 80))

   print("Preparing to send email...")
   msg = MIMEText("")
   msg["Subject"] = "Skulving's local IP address: " + s.getsockname()[0] + "."
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
   print("Email sent successfully!")
   
   s.close()
   
def openSerial():
   ser = serial.Serial("/dev/ttyACM0", 2400)
   
def waitForSerial():
   print "Reading serial input..."
   serialInput = ser.readline()
   serialInput = serialInput.strip()
   print "Serial input is: " + serialInput
   if len(serialInput) == 10:
      print "RFID card read. Initializing swipe."
      swipe(serialInput[-2:])
      
def speak(string):
   subprocess.call["./Speech.sh", string]

openSerial()
reportIP()
main()