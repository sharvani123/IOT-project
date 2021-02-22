import RPi.GPIO as GPIO
import time
import cv2
import serial
import decimal
import os
import subprocess
import sys
import httplib, urllib

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1.0)
gps = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1.0)

key = 'XY8QS7ILSZ8YZZAI'  # Thingspeak channel to update

motor = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor,GPIO.OUT)

GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_UP)
DEBUG = 1

servoPIN = 17
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(0) # Initialization
def servo():
    
    p.ChangeDutyCycle(2)
    time.sleep(0.5)
    p.ChangeDutyCycle(7)
    time.sleep(5)
    p.ChangeDutyCycle(2)
    time.sleep(0.5)




# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)       

cam = cv2.VideoCapture(0)


ID=["2600A0075FDE"]
p1_money= 10000

def main():


        a=1
        #value=True
        GPIO.output(motor, True) 
        MEMS = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        GAS = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        temp= readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        temp = int(temp*0.35828125)

        print "--------------------------------------------"

        data = ("MEMS: {} ".format(MEMS))+ (" GAS: {} ".format(GAS)) +(" temperature: {} ".format(temp)) 
        print data
        f=open('/home/pi/data.txt','w')
        f.write(data)
        f.close()

        params = urllib.urlencode({'field1': MEMS,'field2' : GAS,'field3' : temp, 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
                conn.request("POST", "/update", params, headers)
                response = conn.getresponse()
                #print response.status, response.reason
                data = response.read()
                conn.close()
        except:
                print "connection failed" 
       
        if( MEMS > 400):  # MEMS < 100 or MEMS > 300

            cv2.imwrite('image.jpg',img)            
            print('*** MEMS DETECTED ***')
           
            
            time.sleep(2)
            
                   
            while(a):
        
                    rcv = gps.readline()
                    p=rcv.find("$GPGGA,")                                    
                    if(p==0):
                            
                            a=rcv[18:28]
                            b=rcv[31:40]
                            lat="lat:"+str(a)
                            lon="lon:"+str(b)
                            print lat
                            print lon
                            file = open("/home/pi/log.txt" , "w")
                            file.write("*** MEMS DETECTED ***")
                            file.write(lat)
                            file.write(lon)
                            file.close()
                            a=0
                            subprocess.Popen("sudo python sms1.py", shell=True)
                            subprocess.Popen("sudo python mail.py", shell=True)
                            
        if( GAS > 300):

            cv2.imwrite('image.jpg',img)   
            print('*** ALCHOCAL EXCEEDS ***')
          
            GPIO.output(motor, False) 
            time.sleep(2)
            
            while(a):
        
                    rcv = gps.readline()
                    p=rcv.find("$GPGGA,")                                    
                    if(p==0):
                            
                            a=rcv[18:28]
                            b=rcv[31:40]
                            lat="lat:"+str(a)
                            lon="lon:"+str(b)
                            print lat
                            print lon
                            file = open("/home/pi/log.txt" , "w")
                            file.write("*** ALCHOCAL EXCEEDS ***")
                            file.write(lat)
                            file.write(lon)
                            file.close()
                            a=0
                            subprocess.Popen("sudo python sms1.py", shell=True)
                            subprocess.Popen("sudo python mail.py", shell=True)
        if( temp > 25):

            cv2.imwrite('image.jpg',img)   
            print('***HIGH TEMPERATURE ***')
          
            GPIO.output(motor, False) 
            time.sleep(2)
            
            while(a):
        
                    rcv = gps.readline()
                    p=rcv.find("$GPGGA,")                                    
                    if(p==0):
                            
                            a=rcv[18:28]
                            b=rcv[31:40]
                            lat="lat:"+str(a)
                            lon="lon:"+str(b)
                            print lat
                            print lon
                            file = open("/home/pi/log.txt" , "w")
                            file.write("*** HIGH TEMPERATURE  ***")
                            file.write(lat)
                            file.write(lon)
                            file.close()
                            a=0
                            GPIO.output(buzzer, False)
                            subprocess.Popen("sudo python sms1.py", shell=True)
                            subprocess.Popen("sudo python mail.py", shell=True)

        time.sleep(1) 

          
try:
    
        
    while True:
        main()
        ret,img = cam.read()
        cv2.imwrite('/var/www/html/image.jpg',img)
        rcv1 = port.read(12)
        print rcv1
        print"Wait for RFID Card...."
        time.sleep(2)
        if (len(rcv1) == 12):                    
            
            #value=False
            
            if rcv1 == ID[0]:
                
                print("--------------------------------------------------------")
                print("--------------------------------------------------------")
                print("**** Person-1 ****")
                print("Vehicle number: AP 10 N 8055 ")
                time.sleep(1)
                
                if(p1_money < 500):
                    print("Low Balance!!!!!")
                    file = open("/home/pi/log1.txt" , "w")
                    file.write("*** LOW BALANCE PLEASE RECHARGE YOUR CARD ***")
                    file.close()
                    subprocess.Popen("sudo python sms1.py", shell=True)
                    #subprocess.call(['sudo','python','sms.py',"Person-1","Plz Recharge..."])
                    
                else:
                    p1_money = p1_money -100                        
                    print("Tollgate chared RS.100\n ","Remaing Balance Amt:",p1_money)
                    money=str(p1_money)
                    file = open("/home/pi/log1.txt" , "w")
                    file.write("*** REMANING BALANCE IN THE ACCOUNT ***")
                    file.write(money)
                    file.close()
                    subprocess.Popen("sudo python sms1.py", shell=True)
                    #subprocess.call(['sudo','python','sms.py',"Person-1 Tollgate chared RS.100 \n Remaing Balance Amt:",str(p1_money)])
                servo()
                
            else:
                   print("****  Alert    ***")
                   print("****  unauthorized vechicle!!!!!  ***")
                 

        cv2.imshow('Frame',img)
        key = cv2.waitKey(5) & 0xff
        if key == ord('q'):
                break
                cv2.destroyAllWindows()
                
        time.sleep(1)
              
except:
    
    KeyboardInterrupt()
    cv2.destroyAllWindows()
