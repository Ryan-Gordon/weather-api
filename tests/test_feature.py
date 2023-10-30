import random
import datetime
from pytest_bdd import scenarios, given, when, then, parsers
from app import app as connex_app
from weather_api.model import SensorData, db
# Import your app specific things here

scenarios('./features/query_sensor.feature')


@given("the sensor data for the last week is available")
def populate_sensor_data():
    with connex_app.app.app_context():
        for i in range(10):
            # Randomly generate temperature and humidity values
            # random values between 18 and 28
            temp_value = round(random.uniform(18.0, 28.0), 2)
            # random values between 40% and 60%
            humidity_value = round(random.uniform(40, 60), 2)

            # Get a date within the last week
            days_before = random.randint(1, 7)
            date = datetime.datetime.now() - datetime.timedelta(days=days_before)

            # Create data entries
            temp_data = SensorData(sensor_id="sensor-1", metric="temperature",
                                   value=temp_value, unit_of_measurement="degrees:celsius", timestamp=date)
            humidity_data = SensorData(sensor_id="sensor-1", metric="humidity",
                                       value=humidity_value, unit_of_measurement="percent", timestamp=date)

            # Add to the database
            db.session.add(temp_data)
            db.session.add(humidity_data)

        # Commit the data to the database
        db.session.commit()


@when(parsers.parse('I request the average temperature and humidity for "{sensor_id}"'), target_fixture="sensor_data")
def request_sensor_data(client_fixture, sensor_id):
    # Make the query to the service to get the data for the given sensor_id
    response = client_fixture.get(
        f"/api/query?sensor_ids={sensor_id}&metrics=temperature,humidity&statistic=average")
    return response


@then(parsers.parse('I should receive the average temperature and humidity values for "{sensor_id}"'))
def verify_sensor_data(sensor_data, sensor_id):
    # Verify the response has the average temperature and humidity values for the given sensor_id
    data = sensor_data.json
    print(data)
    assert "temperature" in data['sensors']
    assert "humidity" in data['sensors']
    # Add more verification as needed
