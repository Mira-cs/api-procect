   
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