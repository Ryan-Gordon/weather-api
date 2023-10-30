"""
This file contains the fixtures that will be used by the tests.
"""
import csv
import datetime
import pytest

from app import app as connex_app
from weather_api.model import db, SensorData

@pytest.fixture
def client_fixture():
    with connex_app.app.test_client() as client:
        with connex_app.app.app_context():
            yield client

"""
Setup the database with some test data for the tests.
Cleanup after the tests are done.
"""
@pytest.fixture(scope="function")
def setup_db_fixture():
    # Load data from the CSV and add to the database
    with open('tests/test_sensor_data.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_data = SensorData(
                sensor_id=row['sensor_id'],
                metric=row['metric'],
                value=float(row['value']),
                unit_of_measurement=row['unit_of_measurement'],
                # Ensure the timestamp is converted to a datetime object
                timestamp=datetime.datetime.strptime(
                    row['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
            )
            db.session.add(new_data)
        db.session.commit()

    yield   # This will allow the test to run

    # Cleanup - remove all the entries after the test is done
    SensorData.query.delete()
    db.session.commit()
