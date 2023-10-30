from model import db, SensorData
import datetime


def post_greeting(name: str):
    return f"Hello {name}", 200

def add_metric(body):
    new_data = SensorData(
        sensor_id=body['sensor_id'],
        metric=body['metric'],
        value=body['value'],
        unit_of_measurement=body['unit_of_measurement'],
        timestamp=datetime.datetime.strptime(body['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
    )
    db.session.add(new_data)
    db.session.commit()
    return {'message': 'Data added successfully!'}, 201