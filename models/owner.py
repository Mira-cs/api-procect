from init import db, ma
from marshmallow import fields

class Owner(db.Model):
  __tablename__ = 'owners'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30))
  last_name = db.Column(db.String(30))
  email = db.Column(db.String, nullable=False, unique=True)
  password = db.Column(db.String, nullable=False)
  contact_number = db.Column(db.Integer)
  
  stores = db.Relationship('Store', back_populates='owner',cascade='all, delete')
  
class OwnerSchema(ma.Schema):
  stores = fields.List(fields.Nested('StoreSchema'))
  class Meta:
    # listing the fields we want to include 
    fields = ('name','last_name','email','password','stores')