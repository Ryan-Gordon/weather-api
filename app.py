from connexion import FlaskApp
import connexion
import os
from model import db, SensorData

app = connexion.FlaskApp(__name__, specification_dir='api-docs/')  # Provide the app and the directory of the docs

# TODO: might make more sense to move to a config file
connex_app = app.app
# SQLite setup
connex_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db.init_app(connex_app)
# Create the database tables if they don't exist
with connex_app.app_context():
    db.create_all()
# Hook up the openapi file 
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 2020)))  # os.environ is handy if you intend to launch on a Cloud platform
