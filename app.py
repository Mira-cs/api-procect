from flask import Flask, request, abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from os import environ
from dotenv import load_dotenv
from models.user import User, UserSchema
from init import db, ma, bcrypt, jwt

load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

db.init_app(app)
ma.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)

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
  try:
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
  except IntegrityError:
    return {'error': 'Email address already in use'}, 409
  
@app.route('/login', methods=['POST'])
def login():
  try:
    # to get the user from the database, where email equals to the email from the user data posted
    stmt = db.select(User).filter_by(email=request.json['email'])
    #  returning one result (scalar method, not scalars)
    user = db.session.scalar(stmt)
    # checking if the user exists (user=True) and password is correct,
    # first parameter is users password from database,
    # the second one is the one retrieved from the POST method)
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
      # generating a token for the user
      token = create_access_token(identity=user.email, expires_delta = timedelta(hours=2))
      return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
    else:
      return {'error': 'Invalid email address or password'}, 401
  except KeyError:
    return{'error': 'Email and password are required'}, 400
  
 
if __name__ == '__main__':
  app.run(debug=True)