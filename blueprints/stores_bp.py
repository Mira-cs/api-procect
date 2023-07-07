from flask import Blueprint, request, abort
from models.store import Store, StoreSchema
from models.user import User
from blueprints.auth_bp import owner_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import owner_required,get_access
from init import db

stores_bp = Blueprint('stores', __name__, url_prefix='/stores')

# Return all Stores available in the db
@stores_bp.route('/')
def all_stores():
  # select * from stores;
  stmt = db.select(Store).order_by(Store.name.asc())
  # storing the result in the stores variable (many)
  stores = db.session.scalars(stmt).all()
  # returning all the available stores
  return StoreSchema(many=True).dump(stores)
# route to return one store based on its id
@stores_bp.route('/<int:store_id>')
def one_store(store_id):
  stmt = db.select(Store).filter_by(id=store_id)
  store = db.session.scalar(stmt)
  if store:
    return StoreSchema().dump(store)
  else:
    return {'error': 'Store not found'}, 404

# Create a new store instance in the database
@stores_bp.route('/', methods=['POST'])
@jwt_required()
def create_store():
  user_id = get_jwt_identity()
  stmt = db.select(User).filter_by(id=user_id)
  user = db.session.scalar(stmt)
  if user.is_owner:
    # Load the incoming POST data via the schema
    store_info = StoreSchema().load(request.json)
    # Create a new store instance from the review_info
    store = Store(
      name = store_info['name'],
      phone_number = store_info['phone_number'],
      user_id = get_jwt_identity(),
      street_number = store_info['street_number'],
      street_name = store_info['street_name'],
      suburb = store_info['suburb'],
      city = store_info['city'],
      state = store_info['state'],
      zip_code = store_info['zip_code']
    )
    # Add and commit the new store to the session
    db.session.add(store)
    db.session.commit()
    # Send the new store info back to the client with the success status
    return StoreSchema().dump(store), 201
  else:
    abort(401)
    
# PUT/PATCH, Update a store information
@stores_bp.route('/<int:store_id>', methods=['PUT','PATCH'])
@jwt_required()
def update_store(store_id):
  stmt = db.select(Store).filter_by(id=store_id)
  store = db.session.scalar(stmt)
  store_info = StoreSchema().load(request.json)
  # if store exists
  if store:   
    get_access(store)
    store.name = store_info.get('name',store.name),
    store.phone_number = store_info.get('phone_number',store.phone_number),
    store.street_number = store_info.get('street_number',store.street_number ),
    store.street_name = store_info.get('street_name',store.street_name),
    store.suburb = store_info.get('suburb',store.suburb),
    store.city = store_info.get('city',store.city),
    store.state = store_info.get('state',store.state),
    store.zip_code = store_info.get('zip_code',store.zip_code)
    db.session.commit()
    return StoreSchema().dump(store)
  else:
    return {'error': 'Store not found'}, 404
  
# delete a store
@stores_bp.route('/<int:store_id>', methods=['DELETE'])
@jwt_required()
def delete_store(store_id):
  owner_required()
  stmt = db.select(Store).filter_by(id=store_id)
  store = db.session.scalar(stmt)
  if store:
    get_access(store_id)
    db.session.delete(store)
    db.session.commit()
    return {}, 200
  else:
    return {'error': 'Store not found'}, 404