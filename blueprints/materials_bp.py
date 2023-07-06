from flask import Blueprint, request, abort
from models.material import Material, MaterialSchema
from models.store import Store, StoreSchema
from blueprints.auth_bp import owner_required,get_owner_object,is_owner_of_store
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity



materials_bp = Blueprint('materials', __name__, url_prefix='/materials')

# Return all Materials available
@materials_bp.route('/')
def all_materials():
  # select * from materials;
  stmt = db.select(Material).order_by(Material.name.desc())
  # storing the result in the materials variable (many)
  materials = db.session.scalars(stmt).all()
  return MaterialSchema(many=True).dump(materials)

# Get one specific material by typing in the name
@materials_bp.route('/<string:material_name>')
def material_one(material_name):
  # using stmt to select the material that matches the name (case insensitive)
  stmt = db.select(Material).where(Material.name.ilike(material_name))
  material = db.session.scalar(stmt)
  # if material is found, return it
  if material:
    return MaterialSchema().dump(material)
  else:
    return {'error': 'Material not found'}, 404
  
# Add a new material
@materials_bp.route('/', methods=['POST'])
@jwt_required()
def create_material():
  owner_required()
  # Load the incoming POST data via the schema
  material_info = MaterialSchema().load(request.json)
  # Create a new Card instance from the card_info
  material = Material(
    name = material_info['name'],
    category = material_info['category'],
    description = material_info['description'],
    price = material_info['price'],
    store_id = material_info['store_id']
  )
  # Add and commit the new card to the session
  db.session.add(material)
  db.session.commit()
  # Send the new card back to the client
  return MaterialSchema().dump(material), 201

# update a material
@materials_bp.route('/<int:material_id>', methods=['PUT','PATCH'])
@jwt_required()
def update_material(material_id):
  owner_required()
  stmt = db.select(Material).filter_by(id=material_id)
  material = db.session.scalar(stmt)
  material_info = MaterialSchema().load(request.json)
  if material and is_owner_of_store(material.store_id):
    material.name = material_info.get('name', material.name)
    material.category = material_info.get('category', material.category)
    material.description = material_info.get('description', material.description)
    material.price = material_info.get('price', material.price)
    db.session.commit()
    return MaterialSchema().dump(material), 201
  else:
    return {'error': 'Material not found'}, 404

@materials_bp.route('/<int:material_id>', methods=['DELETE'])
@jwt_required()
def delete_material(material_id):
  owner_required()
  stmt = db.select(Material).filter_by(id=material_id)
  material = db.session.scalar(stmt)
  if material and is_owner_of_store(material.store_id):
    db.session.delete(material)
    db.session.commit()
    return {'Message': 'Material was successfully deleted'}, 200
  else:
    return {'error': 'Store not found'}, 404
