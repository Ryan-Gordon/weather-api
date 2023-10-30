from connexion import FlaskApp
import connexion
import os

app = connexion.FlaskApp(__name__, specification_dir='api-docs/')  # Provide the app and the directory of the docs
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 2020)))  # os.environ is handy if you intend to launch on a Cloud platform
