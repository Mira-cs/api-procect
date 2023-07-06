from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, OneOf, Regexp, And

VALID_CATEGORIES = ('Flooring', 'Finishes', 'Surfaces', 'Other')

class Material(db.Model):
  __tablename__ = 'materials'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  category = db.Column(db.String(30), nullable=False)
  description = db.Column(db.Text)
  price = db.Column(db.Numeric, nullable=False)
  
  
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id', ondelete='CASCADE'), nullable=False)
  store = db.relationship('Store',back_populates='materials')
  reviews = db.relationship('Review',back_populates='material',cascade='all, delete')
  
class MaterialSchema(ma.Schema):
  store = fields.Nested('StoreSchema', only=['name','suburb','city'] )
  name = fields.String(required=True, validate=And(Length(min=5), Regexp('^[a-zA-Z ]+$', error='Only letters and spaces are allowed')))
  category = fields.String(required=True, validate=OneOf(VALID_CATEGORIES))
  price = fields.Float(required=True)
  store_id = fields.Integer(required=True)
  
  class Meta:
    # listing the fields we want to include 
    fields = ('id','name','category', 'description','price','store','store_id')