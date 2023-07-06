from flask import Flask
from os import environ
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from blueprints.materials_bp import materials_bp
from blueprints.reviews_bp import reviews_bp
from blueprints.stores_bp import stores_bp

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

  @app.errorhandler(401)
  def unauthorized(err):
    return {'error': 'You are not authorized to perform this action'}, 401

  return app