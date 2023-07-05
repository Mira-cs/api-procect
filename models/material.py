from init import db, ma

class Material(db.Model):
  __tablename__ = 'materials'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  category = db.Column(db.String(30), nullable=False)
  description = db.Column(db.Text)
  price = db.Column(db.Numeric, nullable=False)
  
class MaterialSchema(ma.Schema):
  class Meta:
    # listing the fields we want to include 
    fields = ('name','category', 'description','price')