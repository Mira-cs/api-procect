from flask import Blueprint, request
from blueprints.auth_bp import user_required, author_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.review import Review, ReviewSchema
from init import db
from flask_jwt_extended import jwt_required

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

# get a list of all the reviews created by the user
@reviews_bp.route('/', methods=['GET'])
@jwt_required()
def all_reviews_by_user():
  # get users id
  user_id = get_jwt_identity()
  # select the review that was created by the user (that matches users id in the review)
  stmt = db.select(Review).filter_by(id=user_id)
  reviews = db.session.scalars(stmt).all()
  # return the reviews to the user
  return ReviewSchema(many=True).dump(reviews)

# Create a review
@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
  user_required()
  # Load the incoming POST data via the schema
  review_info = ReviewSchema().load(request.json)
  # Create a new Review instance from the review_info
  review = Review(
    title = review_info['title'],
    comment = review_info['comment'],
    rating = review_info['rating'],
    user_id = get_jwt_identity(),
    store_id = review_info['store_id'],
    material_id = review_info['material_id']
  )
  # Add and commit the new review to the session
  db.session.add(review)
  db.session.commit()
  # Send the new review back to the client
  return ReviewSchema().dump(review), 201

# Update a review
@reviews_bp.route('/<int:review_id>', methods=['PUT','PATCH'])
@jwt_required()
def update_review(review_id):
  stmt = db.select(Review).filter_by(id=review_id)
  review = db.session.scalar(stmt)
  review_info = ReviewSchema().load(request.json)
  if review:
    author_required(review.user_id)
    review.title = review_info.get('title', review.title)
    review.comment = review_info.get('comment', review.comment)
    review.rating = review_info.get('rating', review.rating)
    db.session.commit()
    return ReviewSchema().dump(review)
  else:
    return {'error': 'Review not found'}, 404
  
# Delete a review
@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
  stmt = db.select(Review).filter_by(id=review_id)
  review = db.session.scalar(stmt)
  if review:
    author_required(review.user_id)
    db.session.delete(review)
    db.session.commit()
    return {}, 200
  else:
    return {'error': 'Review not found'}, 404