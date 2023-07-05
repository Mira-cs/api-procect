from init import db, ma

class Address(db.Model):
  __tablename__ = 'addresses'
  
  id = db.Column(db.Integer, primary_key=True)
  street_number = db.Column(db.Integer, nullable=False)
  street_name = db.Column(db.String(30), nullable=False) 
  suburb = db.Column(db.String(30), nullable=False)
  city = db.Column(db.String(30), nullable=False)
  state = db.Column(db.String(30), nullable=False)
  zip_code = db.Column(db.Integer, nullable=False)
  
class MaterialSchema(ma.Schema):
  class Meta:
    # listing the fields we want to include 
    fields = ('name','category', 'description','quantity','price')