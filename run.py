from model import db, SensorData
import datetime


def post_greeting(name: str):
    return f"Hello {name}", 200


def add_metric(body):

    # Validate the input data, ideally this is also done via the API docs marking fields as required
    if not all(key in body for key in ("sensor_id", "metric", "value", "unit_of_measurement", "timestamp")):
        return {'message': 'Missing a key'}, 400

    # Validate the timestamp
    try:
        datetime.datetime.strptime(body['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        return {'message': 'Incorrect timestamp format, should be YYYY-MM-DDTHH:MM:SS.mmmZ'}, 400

    #  Add the data to the database
    new_data = SensorData(
        sensor_id=body['sensor_id'],
        metric=body['metric'],
        value=body['value'],
        unit_of_measurement=body['unit_of_measurement'],
        timestamp=datetime.datetime.strptime(
            body['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
    )
    db.session.add(new_data)
    db.session.commit()
    return {'message': 'Data added successfully!'}, 201


def query_metric(sensor_ids: list, metrics: list, statistic='average', date_range='latest'):
    # Date range parsing, if latest then use the last 24 hours
    if date_range == 'latest':
        start_date = datetime.datetime.now() - datetime.timedelta(days=1)
        end_date = datetime.datetime.now()
    else:
        start_date, end_date = map(lambda x: datetime.datetime.strptime(
            x, '%Y-%m-%d'), date_range.split(':'))

    # Query the database, the reason I used SQLAlchemy shines here as I can use the ORM to query the database
    #  without having to write any SQL myself
    data = SensorData.query.filter(
        SensorData.sensor_id.in_(sensor_ids),
        SensorData.metric.in_(metrics),
        SensorData.timestamp.between(start_date, end_date)
    ).all()
    # Prepare the results based on the statistic requested
    result = {
        "sensors": {}
    }
    # Add metrics to the result
    for m in metrics:
        #  Gather all values for the given metric m as a list so we can do sums,avgs,mins and maxs on them
        values = [d.value for d in data if d.metric == m]
        if values:
            if statistic == 'min':
                result["sensors"][m] = {
                    "statistic": "min", "value": min(values)}
            elif statistic == 'max':
                result["sensors"][m] = {
                    "statistic": "max", "value": max(values)}
            elif statistic == 'sum':
                result["sensors"][m] = {
                    "statistic": "sum", "value": sum(values)}
            else:
                result["sensors"][m] = {
                    "statistic": "average", "value": sum(values) / len(values)}
        else:
            # or some default value indicating no data found
            result["sensors"][m] = {"value": None}

    return result
