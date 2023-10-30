## Weather API 

## Overview 

Imagine that we are building a service that receives weather data from various sensors that report metrics such as temperature, humidity, wind speed, etc. Your task in this coding challenge is building an application that solves part of this problem:
• The application can receive new metric values as the weather changes around the sensor via an API call.
• The application must allow querying sensor data. A query should define:
• One or more (or all sensors) to include in results.
• The metrics (e.g. temperature and humidity); the application should return
the average value for these metrics.
• The statistic for the metric: min, max, sum or average.
• A date range (between one day and a month, if not specified, the latest data
should be queried).
• Example query: Give me the average temperature and humidity for sensor 1
in the last week.

### Design Decisions 

I opted to use the library `connexion` so I can take a design or 'spec-first' approach to building the API. This allows me to define the API in a yaml file and focus on the design of the API before writing any code. Each route in the API is linked to an implementation using the operationId field meaning I can write the implementation in a separate file and ensure each route has a corresponding implementation.

For persistence, to save time I opted to use SQLAlchemy and SQLite. The connexion library has an optional `flask` extension which will use Flask. Both Flask and SQLAlchemy play nicely. 

### Setup 

#### Optional Configs 
You can specify the port the service runs on or the location of the database file. If you don't specify these, the defaults will be used. 

```
export WEATHER_API_PORT=8080
export SQLLITE_DB_LOCATION=/tmp/weather.db
```

#### Running the service 

> Its advisable to setup a virtual environment before installing the dependencies. I use `pyenv` and `pyenv-virtualenv` to manage my python versions and virtual environments. 


Install the dependencies
```

pip install -r requirements.txt
```

Run the service
```
python app.py
```

### Testing and CI 

There are 3 types of tests located in the `tests` directory.
+ The first type are parameterised tests which test the API routes against expected responses or results. 
+ The second type are behaviour driven tests. I took the example query from the spec and used it to define a 'feature' to test against
+ The third type is load testing with locust. This is a very simple test file that will shoot twice as many posts to `metric` as it does queries to `query`

To run the tests just run 
```
pytest tests
```

The load test file will not be included in this. 
To use, install locust, run the API locally and then run 
```
locust -f tests/test_locust.py --host http://127.0.0.1:2020
```

If you don't want to run it in the UI, use the following to run it for 20 seconds with 10 users and a hatch rate of 1 user per second.

```
locust -f tests/test_locust.py --host http://127.0.0.1:2020 --headless -u 10 -r 1 --run-time 20s

```

