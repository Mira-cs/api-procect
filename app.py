from flask import Flask
from os import environ
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from blueprints.materials_bp import materials_bp
from blueprints.reviews_bp import reviews_bp
from blueprints.stores_bp import stores_bp
from marshmallow.exceptions import ValidationError

def create_app():
  app = Flask(__name__)

  app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
  app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

  db.init_app(app)
  ma.init_app(app)
  jwt.init_app(app)
  bcrypt.init_app(app)

  app.register_blueprint(cli_bp)
  app.register_blueprint(auth_bp)
  app.register_blueprint(materials_bp)
  app.register_blueprint(reviews_bp)
  app.register_blueprint(stores_bp)
  
  @app.errorhandler(ValidationError)
  def validation_error(err):
    return {'error': err.__dict__["messages"]}, 400

  @app.errorhandler(401)
  def unauthorized_error(err):
    return {'error': str(err)}, 401
  
  @app.errorhandler(403)
  def unauthorized_errorr(err):
    return {'error': str(err)}, 403

  return app