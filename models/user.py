from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, Regexp, And

# creating a class User with the table name 'users'
class User(db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  last_name = db.Column(db.String(30),nullable=False)
  email = db.Column(db.String, nullable=False, unique=True)
  password = db.Column(db.String, nullable=False)
  is_owner =db.Column(db.Boolean, default=False)
  
  # defining the attributes that will connect User table to associated tables in the database
  stores = db.relationship('Store', back_populates='user',cascade='all, delete')
  reviews = db.relationship('Review', back_populates='user', cascade='all, delete')
# validating and enforsing some of the constraints on the attributes/fields
class UserSchema(ma.Schema):
  name = fields.String(required=True, validate=And(Length(min=3),Regexp('^[a-zA-Z ]+$', error='Only letters and spaces are allowed')))
  last_name = fields.String(required=True, validate=And(Length(min=3),Regexp('^[a-zA-Z ]+$', error='Only letters and spaces are allowed')))
  email = fields.Email(required=True, validate=Length(min=8))
  password = fields.String(required=True, validate=Length(min=8))

  class Meta:
    # listing the fields we want to include 
    fields = ('name','last_name', 'email','password')