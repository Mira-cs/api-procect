from init import db, ma
from marshmallow import fields

class Material(db.Model):
  __tablename__ = 'materials'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  category = db.Column(db.String(30), nullable=False)
  description = db.Column(db.Text)
  price = db.Column(db.Numeric, nullable=False)
  
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
  stores = db.relationship('Store',back_populates='materials')
  
class MaterialSchema(ma.Schema):
  stores = fields.List(fields.Nested('StoreSchema'))
  class Meta:
    # listing the fields we want to include 
    fields = ('name','category', 'description','price','stores')