from init import db, ma


class Store(db.Model):
  __tablename__ = 'stores'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  phone_number = db.Column(db.String(30), nullable=False)  
  
  owner_id = db.Column(db.Integer, db.ForeignKey('owners.id',ondelete='CASCADE'), nullable=False)
  
  
  
class StoreSchema(ma.Schema):
  class Meta:
    # listing the fields we want to include 
    fields = ('name','phone_number','address', 'owner_id')