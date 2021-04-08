import os

from flask import Flask, send_from_directory


def create_app():
    # /client/build should hold the built react frontend (npm build)
    app = Flask(__name__, instance_relative_config=True,
                static_folder='./front-end-files', static_url_path='/')

    # Check that the instance folder exists. It should hold the config.py file.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_pyfile('config.py', silent=True)

    from flask_api import db
    db.init_app(app)

    from flask_api import all_paths
    app.register_blueprint(all_paths.bp)

    from flask_api import db_export
    app.register_blueprint(db_export.bp)

    # Serves the single page react app from the build folder
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app
