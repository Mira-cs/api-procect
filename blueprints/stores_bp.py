from flask import Blueprint, request
from models.store import Store, StoreSchema
from blueprints.auth_bp import owner_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db

stores_bp = Blueprint('stores', __name__, url_prefix='/stores')

# Return all Stores available
@stores_bp.route('/')
def all_stores():
  # select * from stores;
  stmt = db.select(Store).order_by(Store.name.desc())
  # storing the result in the stores variable (many)
  stores = db.session.scalars(stmt).all()
  return StoreSchema(many=True).dump(stores)

@stores_bp.route('/<int:store_id>')
def one_store(store_id):
  stmt = db.select(Store).filter_by(id=store_id)
  store = db.session.scalar(stmt)
  if store:
    return StoreSchema().dump(store)
  else:
    return {'error': 'Store not found'}, 404

# Create a store instance
@stores_bp.route('/', methods=['POST'])
@jwt_required()
def create_store():
  owner_required()
  # Load the incoming POST data via the schema
  store_info = StoreSchema().load(request.json)
  # Create a new store instance from the review_info
  store = Store(
    name = store_info['name'],
    phone_number = store_info['phone_number'],
    owner_id = get_jwt_identity()
  )
  # Add and commit the new store to the session
  db.session.add(store)
  db.session.commit()
  # Send the new store info back to the client with the success status
  return StoreSchema().dump(store), 201
