#TODO: Fully comment, constrain imports.

import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://thehub:cas0iWur@localhost:3306/hubdb_test')
Base = declarative_base()

class Code(Base):
    __tablename__ = 'codes'
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(CHAR(4), nullable=False)
    value = Column(String(256), nullable=False)

    def to_dictionary(self):
        """
        Returns a dictionary indexed by error table fields.
        """
        return { 'id' : self.id, 'value' : self.value }

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True, nullable=False)
    serial_port = Column(String(256), unique=True, nullable=False)
    description = Column(String(256), nullable=False)
    model_number = Column(
        Integer, ForeignKey('device_models.model_number'), nullable=False
    )
    model = relationship("DeviceModel", foreign_keys=[model_number])
    serial_number = Column(Integer, nullable=False)
    sensors = relationship("Sensor")

    def to_dictionary(self):
        """
        Returns a dictionary indexed by device table fields.
        """
        return { 'id' : self.id,
                 'description' : self.description }

class DeviceModel(Base):
    __tablename__ = 'device_models'
    model_number = Column(
        Integer, primary_key=True, unique=True,
        autoincrement=False, nullable=False
    )
    number_of_sensors = Column(Integer, nullable=False)
    description = Column(String(256), nullable=False)
    wireless = Column(Boolean(create_constraint=False), nullable=False)

    def to_dictionary(self):
        """
        Returns a dictionary indexed by device model fields.
        """
        return { 'model_number' : self.model_number,
                 'number_of_sensors' : self.number_of_sensors,
                 'description' : self.description,
                 'wireless' : self.wireless }

class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True, nullable=False)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    device = relationship("Device", foreign_keys=[device_id])
    description = Column(String(256), nullable=False)
    model_number = Column(
        Integer, ForeignKey('sensor_models.model_number'), nullable=False
    )
    model = relationship("SensorModel", foreign_keys=[model_number])
    pin = Column(String(3), nullable=False)
    serial_number = Column(Integer, nullable=False)

    def to_dictionary(self):
        """
        Returns a dictionary indexed by sensor table fields.
        """
        return { 'id' : self.id,
                 'description' : self.description }

class SensorModel(Base):
    __tablename__ = 'sensor_models'
    model_number = Column(
        Integer, primary_key=True, unique=True,
        autoincrement=False, nullable=False
    )
    minimum_value = Column(Integer, nullable=False)
    maximum_value = Column(Integer, nullable=False)
    description = Column(String(256), nullable=False)
    wireless = Column(Boolean(create_constraint=False), nullable=False)

    def to_dictionary(self):
        """
        Returns a dictionary indexed by sensor model fields.
        """
        return { 'id' : self.id,
                 'minimum_value' : self.minimum_value,
                 'maximum_value' : self.maximum_value,
                 'description' : self.description,
                 'wireless' : self.wireless }

class DataEvent(Base):
    __tablename__ = 'data_events'
    id = Column(Integer, primary_key=True, nullable=False)
    timestamp = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    device = relationship("Device", foreign_keys=[device_id])
    sensor_id = Column(Integer, ForeignKey('sensors.id'), nullable=False)
    sensor = relationship("Sensor", foreign_keys=[sensor_id])
    value = Column(Integer, nullable=False)

    def to_dictionary(self):
        """
        Returns a dictionary indexed by event table fields.
        """
        return { 'timestamp' : self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                 'value' : self.value }

class CodeEvent(Base):
    __tablename__ = 'code_events'
    id = Column(Integer, primary_key=True, nullable=False)
    timestamp = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    device = relationship("Device", foreign_keys=[device_id])
    code_id = Column(Integer, ForeignKey('codes.id'), nullable=False)
    code = relationship("Code", foreign_keys=[code_id])

    def to_dictionary(self):
        """
        Returns a dictionary indexed by code log fields.
        """
        return { 'id' : self.id,
                 'timestamp' : self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                 'device' : self.device.id,
                 'code' : self.code.code }

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, nullable=False)
    timestamp = Column(
            DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    read = Column(Boolean(create_constraint=False), nullable=False)
    value = Column(String(256), nullable=False)
    severity_id = Column(Integer, ForeignKey('severities.id'), nullable=False)
    severity = relationship("Severity", foreign_keys=[severity_id])

class Severity(Base):
    __tablename__ = 'severities'
    id = Column(Integer, primary_key=True, nullable=False)
    value = Column(String(256), nullable=False)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session=Session()
