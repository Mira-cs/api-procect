from flask import Blueprint, request
from blueprints.auth_bp import user_required
from models.review import Review, ReviewSchema
from init import db
from flask_jwt_extended import jwt_required

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

# Create a review
@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_card():
  user_required()
  # Load the incoming POST data via the schema
  review_info = ReviewSchema().load(request.json)
  # Create a new Review instance from the review_info
  review = Review(
    title = review_info['title'],
    comment = review_info['comment'],
    rating = review_info['rating'],
    user_id = review_info['user_id'],
    store_id = review_info['store_id'],
    material_id = review_info['material_id']
  )
  # Add and commit the new review to the session
  db.session.add(review)
  db.session.commit()
  # Send the new review back to the client
  return ReviewSchema().dump(review), 201