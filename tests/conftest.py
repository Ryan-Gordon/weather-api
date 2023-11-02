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
    print("Setting up test database")

    # Load data from the CSV and add to the database
    mock_timestamp = datetime.datetime.now()
    with open('tests/test_sensor_data.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_data = SensorData(
                sensor_id=row['sensor_id'],
                metric=row['metric'],
                value=float(row['value']),
                unit_of_measurement=row['unit_of_measurement'],
                timestamp=mock_timestamp
            )
            db.session.add(new_data)
        db.session.commit()

    # # Debug: Print out the contents of the database
    # print("Contents of test database:")
    # for data in SensorData.query.all():
    #     print(data)

    yield  # This will allow the test to run

    # Cleanup - remove all the entries after the test is done
    db.session.query(SensorData).delete()
    db.session.commit()
    print("Cleaned up test database")

    # Debug: Ensure cleanup is working
    if SensorData.query.count() == 0:
        print("Test database is clean")
    else:
        print("Test database still has data, cleanup may not be working as expected")
