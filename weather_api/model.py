"""
Models used by the API to represent the data in the database.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SensorData(db.Model):
    """
    A class used to represent a sensor data entry in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(50), nullable=False) # The ID of the given sensor
    metric = db.Column(db.String(50), nullable=False) # The type of metric recorded by the sensor; e.g. temperature, humidity, etc.
    value = db.Column(db.Float, nullable=False) # The value of the metric recorded by the sensor
    unit_of_measurement = db.Column(db.String(50), nullable=False) # The unit of measurement of the metric recorded by the sensor; e.g. degrees Celsius, KM/H, etc.
    timestamp = db.Column(db.DateTime, nullable=False) # The timestamp of the metric recorded by the sensor
