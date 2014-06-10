#!/usr/bin/env python


import sys
import time
import serial
import queue
import threading
import re
from ..database import db



class Bridge():

    
        def __init__(self, from_hw_queue, device):

            self.device = device;


            self.from_hw = from_hw_queue
            
            self.to_hw = queue.Queue()
            self.running = True
            self.serialport = '/dev/ttyUSB0'
            self.serialrate = 9600
            self.myserial = None
            self.stopped = True
            self.test = False
            
            self.output = True
            
            if self.test:
                self.fromhwtest = queue.Queue()
            if self.output:
                self.f = open('bridge_file.txt', 'a')
                
            self.start()

        #stop, send the kill message to the thread
        def stop(self):
            self.to_hw.put_nowait("kill")


        def start(self):
            if self.output:
                self.f.write("starting\n")
            #check that required information is set
            if ((self.from_hw != None) and (self.serialport != None) and (self.serialrate != None) and self.stopped):
                if (self.test):#testing
                        mythread = threading.Thread(target=self.theprocess)
                        if self.output:
                            self.f.write("starting process\n")
                        mythread.start()
                else:
                        #setup serial and start thread
                        self.myserial = serial.Serial(self.serialport, self.serialrate, timeout=1)
                        if (self.myserial.isOpen()):
                                if self.output:
                                    self.f.write("serial is open\n")
                                mythread = threading.Thread(target=self.theprocess)
                                mythread.start()
            else:
                #kick and scream
                
                if (self.from_hw == None):
                    print("from Hardware queue not yet set")
                if (self.serialport == None):
                    print("Serial Port not set")
                if (self.serialrate == None):
                    print("Serial Rate not set")
                if not(self.stopped):
                    print("Already running");
                    
        
                    
        def theprocess(self):
                self.stopped = False
                self.running = True
                while self.running:
                                        
                    #message for hardware
                    if (not(self.to_hw.empty())):
                        msg = str(self.to_hw.get_nowait())
                        if self.output:
                            self.f.write(" [*] Writing message to hardware: " + msg + "\n")
                        if (msg == 'kill'):
                            self.running = False
                            if self.output:
                                self.f.write(" Got a kill command\n")
                        else:
                            if (not(self.test)):
                                self.myserial.write(bytes(msg, 'UTF-8'))
                            if self.output:
                                self.f.write(" [*] Wrote message to hardware: " + msg + "\n")
                            
                            
                    if (not(self.test)):#not a test
                        hw_msg = self.myserial.readline().decode('utf8')                        
#                        if (hw_msg != b''):#got a message from the hardward
                        if self.output:
                            self.f.write(" [x] Got message from hardware: " + hw_msg + "\n")
                            print(" [x] Got message from hardware: " + hw_msg + "\n")
                        if (hw_msg!=""):#got a message from the hardward
                                
                                self.from_hw.put_nowait(self.translate_message_fromhw(hw_msg))
                                
                    else:#is a test
                        if (not( self.fromhwtest.empty())):
                            hw_msg = self.fromhwtest.get()            
                            if self.output:                
                                print (" [x] Got test message from hardware: " + hw_msg)
                            self.from_hw.put_nowait(self.translate_message_fromhw(hw_msg))                    
                            

                if (not(self.test)):#not a test, clean up
                        self.myserial.close()
                self.stopped = True
                
                
        def send_message(self, themessage):
            #translated_message = translate_message_tohw(themessage)
            print ("message from hardware")
            if self.output:
                print (" [x] Got message to pass to hardware: " + themessage)
            
            if themessage == "kill":
                to_hw.to_hw.put_nowait("kill")
            else:
                #default behavior get all
                for somesensor in self.device.sensors:
                    print(somesensor.pin)
                    if re.match("[A-Z][A-Z0-9]",somesensor.pin):
                        self.to_hw.put_nowait(somesensor.pin);
                    else:
                        print("Bad sensor ID: "+somesensor.pin)
        
        
        #place holding for message translation
        def translate_message_tohw (themessage):
            print ("message to hardware")
            #do some translating eventually
            outmessage = themessage
            return outmessage

        def translate_message_fromhw (self,themessage):
            #do some translating            
            outmessage = ""
            if themessage[0] == "V":
                print("sensor: "+themessage[1:4])
                #get appropriate sensor object
                #db.session.commit()
                #thesensors = db.session.query(db.Sensor).filter(db.Sensor.device_id==self.device.id).filter(db.Sensor.pin==themessage[1:4])
                #db.session.commit()

                #create dataeven object and return
                if db.session.query(db.Sensor).filter(db.Sensor.device_id==self.device.id).filter(db.Sensor.pin==themessage[1:4]).count()>0:
                    thesensor = db.session.query(db.Sensor).filter(db.Sensor.device_id==self.device.id).filter(db.Sensor.pin==themessage[1:4]).all()[0]
                    #db.session.commit()
                    outmessage = db.DataEvent(device = self.device, sensor = thesensor, value =int(themessage[3:6]))
                   # db.session.commit()
                    if self.output:
                        print("created data event")
                
            return outmessage

        def __del__(self):
            #if self.output:
            #    self.f.close()
            pass
