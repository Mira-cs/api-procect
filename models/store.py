from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, Regexp, And

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
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
  
  user = db.relationship('User', back_populates='stores')
  materials = db.relationship('Material',back_populates='store', cascade='all, delete')
  reviews = db.relationship('Review', back_populates='store',cascade='all, delete')

class StoreSchema(ma.Schema):
  name = fields.String(required=True, validate=And(Length(min=5), Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, numbers and spaces are allowed')))
  phone_number = fields.String(required=True, validate=And(Regexp('^[0-9 ]+$', error='Only numbers and spaces are allowed')))
  street_number = fields.Integer(required=True)
  street_name = fields.String(required=True, validate=And(Length(min=5), Regexp('^[a-zA-Z ]+$', error='Only letters and spaces are allowed')))
  suburb = fields.String(required=True, validate=And(Length(min=5), Regexp('^[a-zA-Z ]+$', error='Only letters and spaces are allowed')))
  city = fields.String(required=True, validate=And(Length(min=5), Regexp('^[a-zA-Z ]+$', error='Only letters and spaces are allowed')))
  state = fields.String(required=True, validate=And(Length(min=5), Regexp('^[a-zA-Z ]+$', error='Only letters and spaces are allowed')))
  zip_code = fields.Integer(required=True)
  reviews = fields.List(fields.Nested('ReviewSchema', exclude=['review_id']))
  class Meta:
    # listing the fields we want to include 
    fields = ('name','suburb', 'city', 'state','id','zip_code','street_name', 'street_number','phone_number','reviews')