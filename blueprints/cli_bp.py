from flask import Blueprint
from models.user import User
from models.store import Store
from models.material import Material
from models.address import Address
from models.owner import Owner
from init import db,bcrypt


cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command('create')
def create_db():
  db.drop_all()
  db.create_all()
  print('Tables created successfully')

@cli_bp.cli.command('seed')
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
    email = 'mark_johnson@gmail.com',
    password = bcrypt.generate_password_hash('password3').decode('utf-8'),
    )
  ]

  owners = [
    Owner(
    name = 'John',
    last_name = 'Smith',
    email = 'john_smith@gmail.com',
    password = bcrypt.generate_password_hash('password4').decode('utf-8')
   ), 
    Owner(
    name = 'Megan',
    last_name = 'Murphy',
    email = 'megan_murphy@gmail.com',
    password = bcrypt.generate_password_hash('password5').decode('utf-8')
   ), 
    Owner(
    name = 'Mark',
    last_name = 'Johnson',
    email = 'mark_johnson@gmail.com',
    password = bcrypt.generate_password_hash('password6').decode('utf-8'),
    )
  ]
  
  # Truncate the User table (deleting rows of data)
  db.session.query(Owner).delete()
  # Add the card to the session (transaction)
  db.session.add_all(owners)
  # Commit the changes to the database
  db.session.commit()
  
  stores = [
    Store(
    name = 'Home Depot',
    phone_number = '91238410'
    ),
    Store(
    name = 'Supplies Inc',
    phone_number = '54098123'
    ),
    Store(
    name = 'Everything you need',
    phone_number = '10235392'
    )
  ]
  
  db.session.query(Store).delete()
  db.session.add_all(stores)
  db.session.commit()
  
  materials = [
    Material(
    name = 'Marble',
    category = 'Flooring',
    description = 'Marble is a natural stone that forms through the metamorphosis of limestone',
    price = 2000.0
    ),
    Material(
    name = 'Vinyl Wallpaper',
    category = 'Finishes',
    description = 'Vinyl wallpaper consists of a base and a vinyl film that is layered on top',
    price = 500.0
    ),
    Material(
    name = 'Granite',
    category = 'Surfaces',
    description = 'A coarse-grained intrusive igneous rock composed mostly of quartz, alkali feldspar, and plagioclase',
    price = 4000.0
    )
  ]
  
  db.session.query(Material).delete()
  db.session.add_all(materials)
  db.session.commit()
  
  addresses = [
    Address(
    street_number = 15,
    street_name = 'Jackson Street',
    suburb = 'Merrylands',
    city = 'Sydney',
    state = 'New South Wales',
    zip_code = 2000
    ),
    Address(
    street_number = 3,
    street_name = 'Monroe Street',
    suburb = 'Lidcombe',
    city = 'Sydney',
    state = 'New South Wales',
    zip_code = 2121
    ),
    Address(
    street_number = 9,
    street_name = 'Grand Street',
    suburb = 'Roscoe',
    city = 'Sydney',
    state = 'New South Wales',
    zip_code = 2023
    ),
  ]
  
  db.session.query(Address).delete()
  db.session.add_all(addresses)
  db.session.commit()

 

  print("Models seeded")