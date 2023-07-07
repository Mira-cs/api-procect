from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length,ValidationError, Regexp, And


class User(db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  last_name = db.Column(db.String(30),nullable=False)
  email = db.Column(db.String, nullable=False, unique=True)
  password = db.Column(db.String, nullable=False)
  is_owner =db.Column(db.Boolean, default=False)
  
  stores = db.Relationship('Store', back_populates='user',cascade='all, delete')
  reviews = db.relationship('Review', back_populates='user', cascade='all, delete')
  
class UserSchema(ma.Schema):
  name = fields.String(required=True, validate=And(Length(min=3),Regexp('^[a-zA-Z ]+$', error='Only letters and spaces are allowed')))
  last_name = fields.String(required=True, validate=And(Length(min=3),Regexp('^[a-zA-Z ]+$', error='Only letters and spaces are allowed')))
  email = fields.Email(required=True, validate=Length(min=8))
  password = fields.String(required=True, validate=Length(min=8))
  
  @validates('email')
  def validate_email(self, email):
    if '@' not in email:
      raise ValidationError('Invalid email address')
    
  class Meta:
    # listing the fields we want to include 
    fields = ('name','last_name', 'email','password')