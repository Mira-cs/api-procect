from init import db, ma
from marshmallow import fields

class Store(db.Model):
  __tablename__ = 'stores'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  phone_number = db.Column(db.String(30), nullable=False)  
  street_number = db.Column(db.Integer, nullable=False)
  street_name = db.Column(db.String(30), nullable=False) 
  suburb = db.Column(db.String(30), nullable=False)
  city = db.Column(db.String(30), nullable=False)
  state = db.Column(db.String(30), nullable=False)
  zip_code = db.Column(db.Integer, nullable=False)
  
  owner_id = db.Column(db.Integer, db.ForeignKey('owners.id', ondelete='CASCADE'), nullable=False)
  
  owner = db.relationship('Owner', back_populates='stores')
  materials = db.relationship('Material',back_populates='stores', cascade='all, delete')
  reviews = db.relationship('Review', back_populates='store',cascade='all, delete')

class StoreSchema(ma.Schema):
  class Meta:
    # listing the fields we want to include 
    fields = ('name','suburb', 'city', 'state','id','zip_code','street_name', 'street_number','phone_number')