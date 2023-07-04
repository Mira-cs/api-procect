from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

print(app.config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://renovations_app_dev:codernewapp2023@localhost:5432/renovation_materials'

db = SQLAlchemy(app)
print(db.__dict__)

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30))
  last_name = db.Column(db.String(30))
  email = db.Column
  password = 
  phone_number = db.Column(db.Integer)
  
class Review(db.Model):
  __tablename__ = 'reviews'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(30))
  comment = db.Column(db.Text())
  rating = db.Column(db.Integer())
  material_id
  shop_id
  user_id
  
class Material(db.Model):
  __tablename__ = 'reviews'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(30))
  comment = db.Column(db.Text())
  rating = db.Column(db.Integer())
  material_id
  shop_id
  user_id
  
class Shop(db.Model):
  __tablename__ = 'reviews'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(30))
  comment = db.Column(db.Text())
  rating = db.Column(db.Integer())
  material_id
  shop_id
  user_id

class Address(db.Model):
  __tablename__ = 'reviews'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(30))
  comment = db.Column(db.Text())
  rating = db.Column(db.Integer())
  material_id
  shop_id
  user_id

@app.cli.command('create')
def create_db():
  db.drop_all()
  db.create_all()
  print('Tables created successfully')

@app.cli.command('seed')
def seed_db():
  # Create an instance of the User model in memory
  users = [
    User(
    name = 'Celeste'
    last_name = 'Adams'
   )
  ]
# Truncate the User table (deleting rows of data)
  db.session.query(User).delete

# Add the card to the session (transaction)
  db.session.add_all(users)
  
# Commit the transaction to the database
  db.session.commit()
  print("Models seeded")

@app.route('/users')
def all_users():  
# select * from users;
  stmt = db.select(User).where(User.name != "Celeste", User.id > 2).order_by(User.name)
  users = db.session.scalars(stmt).all()
  return users.dumps(users)
  

@app.route('/')
def index():
 return 'Hello World'

if __name__ == '__main__':
  app.run(debug=True)