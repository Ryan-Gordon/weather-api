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