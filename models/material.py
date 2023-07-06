from init import db, ma
from marshmallow import fields

class Material(db.Model):
  __tablename__ = 'materials'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  category = db.Column(db.String(30), nullable=False)
  description = db.Column(db.Text)
  price = db.Column(db.Numeric, nullable=False)
  
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id',ondelete='CASCADE'), nullable=False)
  stores = db.relationship('Store',back_populates='materials',cascade='all, delete')
  reviews = db.relationship('Review',back_populates='materials',cascade='all, delete')
  
class MaterialSchema(ma.Schema):
  class Meta:
    # listing the fields we want to include 
    fields = ('name','category', 'description','price','store_id')