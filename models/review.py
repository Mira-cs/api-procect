from init import db, ma

class Review(db.Model):
  __tablename__ = 'reviews'
  
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50))
  comment = db.Column(db.String())
  rating = db.Column(db.Integer, nullable=False)
  
  # this table is linked to users table via FK user_id, nullable=false,
  # because a review can't be created without a user
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
  material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
  
class ReviewSchema(ma.Schema):
  class Meta:
    # listing the fields we want to include 
    fields = ('title','comment', 'rating', 'user_id', 'store_id', 'material_id')