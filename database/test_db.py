#!/usr/bin/env python
import db

# Create basic code objects.
info_code = db.Code(code = "I001", value = "System Acquired Sentience.")
error_code = db.Code(code = "E001", value = "Heisenbug. System borked.")

# Create basic device model objects.
basic_wired_device = db.DeviceModel(
    model_number = 1, number_of_sensors = 3,
    description = "Black Mesa Basic Wired Device", wireless=False
)
basic_wireless_device = db.DeviceModel(
    model_number = 2, number_of_sensors = 3,
    description = "Aperture Science, Inc. Basic Wireless Device", wireless=True
)

# Create basic sensor model objects.
basic_wired_door_sensor = db.SensorModel(
    model_number = 1, minimum_value = 0, maximum_value = 1,
    description = "Black Mesa Basic Wired Door Sensor", wireless = False
)
basic_wired_temp_sensor = db.SensorModel(
    model_number = 3, minimum_value = 0, maximum_value = 511,
    description = "Black Mesa Basic Wired Temperature Sensor", wireless = False
)
basic_wired_light_sensor = db.SensorModel(
    model_number = 5, minimum_value = 0, maximum_value = 1023,
    description = "Black Mesa Basic Wired Light Sensor", wireless = False
)
basic_wireless_door_sensor = db.SensorModel(
    model_number = 2, minimum_value = 0, maximum_value = 1,
    description = "Aperture Science, Inc. Basic Wireless Door Sensor",
    wireless = True
)
basic_wireless_temp_sensor = db.SensorModel(
    model_number = 4, minimum_value = 0, maximum_value = 511,
    description = "Aperture Science, Inc. Basic Wireless Temperature Sensor",
    wireless = True
)
basic_wireless_light_sensor = db.SensorModel(
    model_number = 6, minimum_value = 0, maximum_value = 1023,
    description = "Aperture Science, Inc. Basic Wireless Light Sensor",
    wireless = True
)

# Add objects to the session and commit to the database.
db.session.add_all([
    info_code, error_code, basic_wired_device, basic_wireless_device,
    basic_wired_door_sensor, basic_wired_temp_sensor, basic_wired_light_sensor,
    basic_wireless_door_sensor, basic_wireless_temp_sensor,
    basic_wireless_light_sensor
])
db.session.commit()
print("DB: Device models, sensor models, and codes added to the database.")

# Create device objects.
wired_device = db.Device(
    serial_port = "/dev/ttyUSB0", description = "Black Mesa Wired Device",
    model = basic_wired_device, serial_number = 12007933
)
wireless_device = db.Device(
    serial_port = "/dev/ttyUSB1",
    description = "Aperture Science, Inc. Wireless Device",
    model = basic_wired_device, serial_number = 13434331
)

# Create sensor objects.
wired_door_sensor = db.Sensor(
    device = wired_device, description = "Black Mesa Wired Door Sensor",
    model = basic_wired_door_sensor, serial_number = 25660623
)
wired_temp_sensor = db.Sensor(
    device = wired_device, description = "Black Mesa Wired Temperature Sensor",
    model = basic_wired_temp_sensor, serial_number = 53132324
)
wired_light_sensor = db.Sensor(
    device = wired_device, description = "Black Mesa Wired Light Sensor",
    model = basic_wired_light_sensor, serial_number = 13032343
)
wireless_door_sensor = db.Sensor(
    device = wireless_device,
    description = "Aperture Science, Inc. Wireless Door Sensor",
    model = basic_wireless_door_sensor, serial_number = 20481414
)
wireless_temp_sensor = db.Sensor(
    device = wireless_device,
    description = "Aperture Science, Inc. Wireless Temperature Sensor",
    model = basic_wireless_temp_sensor, serial_number = 40961919
)
wireless_light_sensor = db.Sensor(
    device = wireless_device,
    description = "Aperture Science, Inc. Wireless Light Sensor",
    model = basic_wireless_light_sensor, serial_number = 80921919
)

# Add objects to the session and commit to the database.
db.session.add_all([
    wired_door_sensor, wired_temp_sensor, wired_light_sensor,
    wireless_door_sensor, wireless_temp_sensor, wireless_light_sensor,
    wired_device, wireless_device
])
db.session.commit()
print("DB: Devices and sensors added to the database.")

# Create a few data events with some time in between them.
data_event_one = db.DataEvent(
    device = wired_device, sensor = wired_door_sensor, value = 0
)
data_event_two = db.DataEvent(
    device = wireless_device, sensor = wireless_temp_sensor, value = 128
)
data_event_three = db.DataEvent(
    device = wireless_device, sensor = wireless_light_sensor, value = 512
)
data_event_four = db.DataEvent(
    device = wired_device, sensor = wired_door_sensor, value = 1
)

# Create a code events.
code_event_one = db.CodeEvent(
    device = wireless_device, code = info_code
)
code_event_two = db.CodeEvent(
    device = wired_device, code = error_code
)

# Add objects to the session and commit to the database.
db.session.add_all([
    data_event_one, data_event_two, data_event_three, data_event_four,
    code_event_one, code_event_two
])
db.session.commit()
print("DB: Data and code events have been added to the database.")

print("DB: The database has been initialized and populated with test data.")
