from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config[
  'SQLALCHEMY_DATABASE_URI'
  ] = 'postgresql+psycopg2://renovations_app_dev:codernewapp2023@localhost:5432/renovation_materials'

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)


class User(db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30))
  last_name = db.Column(db.String(30))
  email = db.Column(db.String, nullable=False, unique=True)
  password = db.Column(db.String, nullable=False)
  is_shop_owner = db.Column(db.Boolean, default=False)
  
class UserSchema(ma.Schema):
  class Meta:
    # listing the fields we want to include 
    fields = ('name','last_name', 'email','password','is_shop_owner')
  
    
# class Review(db.Model):
#   __tablename__ = 'reviews'
  
#   id = db.Column(db.Integer, primary_key=True)
#   title = db.Column(db.String(30))
#   comment = db.Column(db.Text())
#   rating = 
#   material_id
#   shop_id
#   user_id
  
# class Material(db.Model):
#   __tablename__ = 'materials'
  
#   id = 
#   name = 
#   description = 
#   price = 
#   shop_id = 

  
# class Shop(db.Model):
#   __tablename__ = 'shops'
  
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(30))
#   contact_info = 
#   address_id

# class Address(db.Model):
#   __tablename__ = 'addresses'
  
#   id = db.Column(db.Integer, primary_key=True)
#   street_number =  
#   street_name = 
#   suburb = 
#   city  = 
#   state = 
#   zip_code = 
  

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
    name = 'Celeste',
    last_name = 'Adams',
    email = 'celeste_adams@gmail.com',
    password = bcrypt.generate_password_hash('password1').decode('utf-8')
   ), 
    User(
    name = 'Caroline',
    last_name = 'Neally',
    email = 'caroline_oneal@gmail.com',
    password = bcrypt.generate_password_hash('password2').decode('utf-8')
   ), 
    User(
    name = 'Mark',
    last_name = 'Johnson',
    email = 'mark_shop@gmail.com',
    password = bcrypt.generate_password_hash('password3').decode('utf-8'),
    is_shop_owner = True
   )
  ]
# Truncate the User table (deleting rows of data)
  db.session.query(User).delete()

# Add the card to the session (transaction)
  db.session.add_all(users)
  
# Commit the transaction to the database
  db.session.commit()
  print("Models seeded")

@app.route('/register', methods=['POST'])
def register(): 
  # to validate and sanitize all the incoming data via Marshmallow schema
  # Parse, sanitize and validate the incoming JSON data
  # via schema
  user_info = UserSchema().load(request.json)
  # Create a new User instance with the schema data
  user = User(
    email=user_info['email'],
    password=bcrypt.generate_password_hash(user_info['password']).decode('utf8'),
    name=user_info['name'],
    last_name=user_info['last_name']
  )
  # Add and commit the new user
  db.session.add(user)
  db.session.commit()
  # Return the new user, excluding the password
  return UserSchema(exclude=['password']).dump(user), 201
  
  
   
# # select * from users;
#   stmt = db.select(User).order_by(User.name)
#   users = db.session.scalars(stmt).all()
#   return UserSchema(many=True).dumps(users)
 

@app.route('/')
def index():
 return 'Hello World'

if __name__ == '__main__':
  app.run(debug=True)