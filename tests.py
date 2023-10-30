import pytest
from app import app as connex_app
from model import db, SensorData
import csv
import datetime


@pytest.fixture
def client_fixture():
    with connex_app.app.test_client() as client:
        with connex_app.app.app_context():
            yield client


@pytest.fixture(scope="function")
def setup_db_fixture():
    # Load data from the CSV and add to the database
    with open('test_sensor_data.csv', 'r') as f:
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


@pytest.mark.parametrize(
    "input_data, expected_status",
    [
        # Happy path: Valid data for temperature
        ({
            "sensor_id": "sensor-temperature-1",
            "metric": "temperature",
            "value": 23.5,
            "unit_of_measurement": "degrees:celsius",
            "timestamp": "2023-10-30T08:45:59.056Z"
        }, 201),

        # sad path: Missing a key (e.g. "value")
        ({
            "sensor_id": "sensor-temperature-1",
            "metric": "temperature",
            "unit_of_measurement": "degrees:celsius",
            "timestamp": "2023-10-30T08:45:59.056Z"
        }, 400),

        # sad path: Incorrect timestamp format
        ({
            "sensor_id": "sensor-temperature-1",
            "metric": "temperature",
            "value": 23.5,
            "unit_of_measurement": "degrees:celsius",
            "timestamp": "2023/10/30 08:45:59"
        }, 400),
        # Happy path; humidity
        ({
            "sensor_id": "sensor-humidity-1",
            "metric": "humidity",
            "value": 70.5,
            "unit_of_measurement": "percent",
            "timestamp": "2023-10-30T10:45:59.056Z"
        }, 201),
    ]
)
def test_add_metric(client_fixture, input_data, expected_status):
    response = client_fixture.post("/api/metric", json=input_data)
    print(response.json)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "query_params, expected_response",
    [
        # 1. Querying temperature sensors of temperature-1 and temperature-2
        (
            "sensor_ids=temperature-1&sensor_ids=temperature-2&metrics=temperature&statistic=average",
            {'sensors': {'temperature': {'statistic': 'average', 'value': 22.75}}}
        ),

        # 2. Querying humidity sensors of humidity-1 and humidity-2
        (
            "sensor_ids=humidity-1&sensor_ids=humidity-2&metrics=humidity&statistic=average",
            {'sensors': {'humidity': {'statistic': 'average', 'value': 55.5}}}
        ),

        # 3. Querying the min value of temperature-1 sensor_id
        (
            "sensor_ids=temperature-1&metrics=temperature&statistic=min",
            {'sensors': {'temperature': {'statistic': 'min', 'value': 23.5}}}
        ),

        # 4. Querying the average of both humidity and temperature for humidity-1 and temperature-1
        (
            "sensor_ids=humidity-1&sensor_ids=temperature-1&metrics=humidity&metric=temperature&statistic=average",
            {'sensors': {'humidity': {'statistic': 'average', 'value': 55.5}}}
        )
    ]
)
def test_query_metric(client_fixture, setup_db_fixture, query_params, expected_response):
    response = client_fixture.get(f"/api/query?{query_params}")
    data = response.json
    print(data)
    assert data == expected_response
