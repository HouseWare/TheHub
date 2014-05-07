#!/usr/bin/env python
import db

# Instantiate code object for info code.
info_code = db.Code(code = "I001", value = "System Boot")

# Instantiate severities to use in notifications.
notification = db.Severity(value = "Notification")
warning = db.Severity(value = "Warning")
alert = db.Severity(value = "Alert")

# Instantiate the project's device model class.
cf412_device_model = db.DeviceModel(
    model_number = 1, number_of_sensors = 4,
    description = "CF412 Device Model", wireless = False
)

# Instantiate an object for each sensor model belonging to the device.
door_sensor_model = db.SensorModel(    
    model_number = 1, minimum_value = 0, maximum_value = 1,
    description = "Door Sensor Model", wireless = False
)

light_sensor_model = db.SensorModel(    
    model_number = 2, minimum_value = 0, maximum_value = 255,
    description = "Light Sensor Model", wireless = False
)

temperature_sensor_model = db.SensorModel(    
    model_number = 3, minimum_value = 0, maximum_value = 255,
    description = "Temperature Sensor Model", wireless = False
)

voltage_sensor_model = db.SensorModel(    
    model_number = 4, minimum_value = 0, maximum_value = 255,
    description = "Voltage Sensor Model", wireless = False
)

# Add all of the currently instantiated objects to the session.
db.session.add_all([
    info_code, notification, warning, alert, cf412_device_model,
    door_sensor_model, light_sensor_model, temperature_sensor_model,
    voltage_sensor_model
])

# Commit the session to the database and log that we have done so.
db.session.commit()
print("DB: Device models, sensor models, and codes added to the database.")

# Instantiate the project's device using our previous device model.
cf412_device = db.Device(
    serial_port = "/dev/ttyUSB0", description = "CF412 Device",
    model = cf412_device_model, serial_number = 10000000
)

# Create a sensor object for each sensor model that we have.
door_sensor = db.Sensor(
    device = cf412_device, description = "Door Sensor",
    model = door_sensor_model, pin = "D04", serial_number = 10000000
)

light_sensor = db.Sensor(
    device = cf412_device, description = "Light Sensor",
    model = light_sensor_model, pin = "A00", serial_number = 10000001
)

temperature_sensor = db.Sensor(
    device = cf412_device, description = "Temperature Sensor",
    model = temperature_sensor_model, pin = "A01", serial_number = 10000002
)

voltage_sensor = db.Sensor(
    device = cf412_device, description = "Voltage Sensor",
    model = voltage_sensor_model, pin = "A02", serial_number = 10000003
)

# Add all the newly instantiated objects to the session.
db.session.add_all([
    cf412_device, door_sensor, light_sensor, temperature_sensor, voltage_sensor
])

# Commit the session to the database and log that we have done so.
db.session.commit()
print("DB: Devices and sensors added to the database.")

print("DB: The database has been initialized.")
