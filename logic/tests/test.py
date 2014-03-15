import queue
import bridge
fromhardware = queue.Queue()

#Bridge.Bridge( fromhardware(queue), deviceID, list of sensorIDs)

bridges = [bridge.Bridge(fromhardware, 0,["A0","A1","D1"]),
           bridge.Bridge(fromhardware, 1,["A4","A6","D4"]),
           bridge.Bridge(fromhardware, 2,["A4","A6","D4"])]


for thisbridge in bridges:
    print("pressing start on: "+ str(thisbridge.device_id))
    thisbridge.start()

    #all messages currently send a get all values to device
    thisbridge.send_message("testmsg1")
    thisbridge.send_message("testmsg2")
    for sensor in thisbridge.sensor_ids:
        thisbridge.fromhwtest.put_nowait("V"+sensor+"999")
    
print("checking queue")
while not fromhardware.empty():
    themessage = fromhardware.get()

    #for return values from sensor message:
    #[message commmand(string), deviceID(int), sensor(string), value(int)]
    print(themessage[0]+str(themessage[1])+themessage[2]+str(themessage[3]))

for thisbridge in bridges:    
    thisbridge.stop()
print("stoppped")
