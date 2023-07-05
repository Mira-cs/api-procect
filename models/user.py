from init import db, ma

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