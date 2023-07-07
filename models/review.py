from init import db, ma
from marshmallow.validate import  Length, Regexp, And
from marshmallow import fields

class Review(db.Model):
  __tablename__ = 'reviews'
  
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50), nullable=False)
  comment = db.Column(db.String(), nullable=False)
  date_created = db.Column(db.Date())
  rating = db.Column(db.Integer, nullable=False)
  
  # this table is linked to users table via FK user_id, nullable=false,
  # because a review can't be created without a user
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
  user = db.relationship('User', back_populates='reviews')
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id', ondelete='CASCADE'), nullable=False)
  store = db.relationship('Store', back_populates='reviews')
  material_id = db.Column(db.Integer, db.ForeignKey('materials.id', ondelete='CASCADE'), nullable=False)
  material = db.relationship('Material', back_populates='reviews')
  
class ReviewSchema(ma.Schema):
  title = fields.String(required=True, validate=And(Length(min=7), Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, numbers and spaces are allowed')))
  comment = fields.String(required=True, validate=Length(min=10))
  rating = fields.Integer(required=True)
  class Meta:
    # listing the fields we want to include 
    fields = ('id','title','comment','rating','date_created','user_id','store_id', 'material_id')