import pytest
from app import app as connex_app

@pytest.fixture
def client():
    with connex_app.app.test_client() as client:
        with connex_app.app.app_context():
            yield client


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
def test_add_metric(client, input_data, expected_status):
    response = client.post("/api/metric", json=input_data)
    print(response.json)
    assert response.status_code == expected_status
