from locust import HttpUser, between, task

class ApiUser(HttpUser):
    wait_time = between(1, 3)  # Wait time between requests for each user

    @task
    def query_data(self):
        self.client.get("/api/query?sensor_ids=temperature-1&metrics=temperature")

    @task(2)  # This task will be executed twice as often as the one above
    def post_metric_data(self):
        self.client.post("/api/metric", json={
            "sensor_id": "sensor-temperature-1",
            "metric": "temperature",
            "value": 23.5,
            "unit_of_measurement": "degrees:celsius",
            "timestamp": "2023-10-30T08:45:59.056Z"
        })
