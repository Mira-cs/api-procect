from flask import Blueprint
from models.user import User
from models.store import Store
from models.material import Material
from models.owner import Owner
from models.review import Review
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
    password = bcrypt.generate_password_hash('password3').decode('utf-8')
    )
  ]

  # Truncate the User table (deleting rows of data)
  db.session.query(User).delete()
  # Add the card to the session (transaction)
  db.session.add_all(users)
  # Commit the changes to the database
  db.session.commit()
  
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
    password = bcrypt.generate_password_hash('password6').decode('utf-8')
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
    phone_number = '91238410',
    owner_id = owners[0].id,
    street_number = 15,
    street_name = 'Jackson Street',
    suburb = 'Merrylands',
    city = 'Sydney',
    state = 'New South Wales',
    zip_code = 2000
    ),
    Store(
    name = 'Supplies Inc',
    phone_number = '54098123',
    owner_id = owners[1].id,
    street_number = 9,
    street_name = 'Grand Street',
    suburb = 'Roscoe',
    city = 'Perth',
    state = 'Western Australia',
    zip_code = 2023
    ),
    Store(
    name = 'Everything you need',
    phone_number = '10235392',
    owner_id = owners[1].id,
    street_number = 3,
    street_name = 'Monroe Street',
    suburb = 'Madeup',
    city = 'Canberra',
    state = 'ACT',
    zip_code = 2121
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
    price = 2000.0,
    store_id = stores[0].id
    ),
    Material(
    name = 'Vinyl Wallpaper',
    category = 'Finishes',
    description = 'Vinyl wallpaper consists of a base and a vinyl film that is layered on top',
    price = 500.0,
    store_id = stores[1].id
    ),
    Material(
    name = 'Granite',
    category = 'Surfaces',
    description = 'A coarse-grained intrusive igneous rock composed mostly of quartz, alkali feldspar, and plagioclase',
    price = 4000.0,
    store_id = stores[0].id
    )
  ]
  
  db.session.query(Material).delete()
  db.session.add_all(materials)
  db.session.commit()

  reviews = [
    Review(
    title = 'Just Okay',
    comment = 'Service could have been better, even though the range of the materials was extensive',
    rating = 3,
    user_id = users[0].id,
    store_id = stores[0].id,
    material_id = materials[0].id
   ), 
    Review(
    title = 'Very happy with the purchase',
    comment = 'The quality of the granite I got from the store is very good',
    rating = 5,
    user_id = users[1].id,
    store_id = stores[1].id,
    material_id = materials[1].id
   ), 
    Review(
    title = 'Highly recommend',
    comment = 'Beautiful marble as well as the quality',
    rating = 5,
    user_id = users[2].id,
    store_id = stores[2].id,
    material_id = materials[2].id
    )
  ]
  
  # Truncate the User table (deleting rows of data)
  db.session.query(Review).delete()
  # Add the card to the session (transaction)
  db.session.add_all(reviews)
  # Commit the changes to the database
  db.session.commit()

  print("Models seeded")
