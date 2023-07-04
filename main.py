from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

print(app.config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://renovations_app_dev:codernewapp2023@localhost:5432/renovation_materials'

db = SQLAlchemy(app)
print(db.__dict__)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30))
  last_name = db.Column(db.String(30))
  email = 
  password = 
  phone_number = db.Column(db.Integer)
  

@app.cli.command('create')
def create_db():
  db.drop_all()
  db.create_all()
  print('Tables created successfully')

@app.cli.command('seed')
def seed_db():
  # Create an instance of the User model in memory
  user = User(
    name = 'Celeste'
    last_name = 'Adams'
    
  )

# Truncate the User table
  db.session.query(User).delete

# Add the card to the session (transaction)
  db.session.add(user)
  
# Commit the transaction to the database
  db.session.commit()
  print("Models seeded")

@app.route('/')
def index():
 return 'Hello World'

if __name__ == '__main__':
  app.run(debug=True)