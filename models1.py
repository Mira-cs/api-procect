   
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
# # select * from users;
#   stmt = db.select(User).order_by(User.name)
#   users = db.session.scalars(stmt).all()
#   return UserSchema(many=True).dumps(users)

# modularizing 
def admin_required():
  user_email = get_jwt_identity()
  stmt = db.select(Modelname).filter_by(email=user_email)
  user = db.session.scalar(stmt)
  if not (user and user.is_shop_owner):
    abort(401)  

# the abort 401 will be picked up by this error handler function
@app.errorhandler(401)
def unauthorized(err):
  return {'error': 'You must be an admin'}, 401
  
@app.route()
@jwt_required()
def all_cards():
  admin_required()
  stmt = db.select(Card).order_by(Card.status.desc())
  cards = db.session.scalars(stmt).all()
  return CardSchema(many=True).dump(cards)
  