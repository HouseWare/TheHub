#!/usr/bin/env python

# Using this module to invesigate solutions to concurrency issues.
import time

import serial
import json

# Open a serial connection.
print("[Bridge] Opening a serial connection to the package...")
ser = serial.Serial('/dev/ttyUSB0', 9600)

#ser.write(bytes('{"sys":"rst"}', "ascii"))
#print("Sent reset request.")

#print(bytes.decode(ser.readline()).rstrip("\n"))

# write a request for the system firmware version.
#ser.write(bytes('{"sys":"ver"}', "ascii"))
#print("Sent version request.")

# Read the response from the system. Display the result.
#version_value = bytes.decode(ser.readline()).rstrip("\n")
#print(version_value)

print("[Bridge] Entering request/response loop...\n")

while True:

    # Write a request to the door sensor.
    ser.write(bytes('{"req":04}', "ascii"))

    # Read the response from the door sensor. Display the result.
    door_value = json.loads(bytes.decode(ser.readline()).rstrip("\n"))['dat'].split(":")[1]
    print("\tDoor: {}".format(door_value))

    # Write a request to the light sensor.
    ser.write(bytes('{"req":50}', "ascii"))

    # Read the response from the light sensor. Display the result.
    luminosity_value = json.loads(bytes.decode(ser.readline()).rstrip("\n"))['dat'].split(":")[1]
    print("\tLuminosity: {}".format(luminosity_value))

    # Write a request to the temperature sensor.
    ser.write(bytes('{"req":51}', "ascii"))

    # Read the response from the temperature sensor. Display the result.
    temperature_value = json.loads(bytes.decode(ser.readline()).rstrip("\n"))['dat'].split(":")[1]
    print("\tTemperature: {}\n".format(temperature_value))

    sensor_dict = {'door': door_value, 'luminosity': luminosity_value, 'temperature': temperature_value}

    # Open the sensor log for appending, write to it, close the file.
    sensorlog = open("sensor.log", "a")
    #sensorlog.write('{"door":' + door_value + ',"luminosity":' + luminosity_value + ',"temperature":' + temperature_value + '}')
    sensorlog.write(str(json.dumps(sensor_dict)) + "\n")
    sensorlog.close()
    print("[Bridge] Wrote data to file\n")

    # Wait one second in an attempt to prevent reading wrong values next loop.
    time.sleep(1)

# Close the serial connection.
ser.close()
