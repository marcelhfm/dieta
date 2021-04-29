from flask import Flask
import os

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

        
    #ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    
    #Authorization
    from . import auth
    app.register_blueprint(auth.bp)
    
    #Configure
    from . import configure
    app.register_blueprint(configure.bp)
    
    
    return app