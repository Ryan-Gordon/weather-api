Feature: Query sensor data

  Scenario: Query average temperature and humidity for a specific sensor over the last week
    Given the sensor data for the last week is available
    When I request the average temperature and humidity for "sensor-1"
    Then I should receive the average temperature and humidity values for "sensor-1"
