from flask import Blueprint, request,abort
from models.material import Material, MaterialSchema
from models.store import Store, StoreSchema
from models.user import User
from blueprints.auth_bp import owner_required
from init import db
from flask_jwt_extended import jwt_required,get_jwt_identity



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
  
@materials_bp.route('/<string:material_name>/<string:location>')
def material_by_location(material_name,location):
  stmt = db.select(Material).where(Material.name.ilike(material_name))
  material = db.session.scalar(stmt)
  get_store = db.select(Store).where(Store.city.ilike(location))
  store = db.session.scalar(get_store)
  # if material is found, return it
  if material and store:
        if material in store.materials:
            return StoreSchema().dump(store)
        else:
            return {'error': 'Material not found in the specified store'}, 404
  else:
      return {'error': 'Material or store not found'}, 404
  
# Add a new material
@materials_bp.route('/', methods=['POST'])
@jwt_required()
def create_material():
  owner_id = get_jwt_identity()
  stmt = db.select(User).filter_by(id=owner_id)
  owner = db.session.scalar(stmt)
  if not owner.is_owner:
    abort(401)
  material_info = MaterialSchema().load(request.json)
  material = Material(
  name=material_info['name'],
  category=material_info['category'],
  description=material_info['description'],
  price=material_info['price'],
  store_id=material_info['store_id']
  )
  db.session.add(material)
  db.session.commit()
  return MaterialSchema().dump(material), 201


# update a material
@materials_bp.route('/<int:material_id>', methods=['PUT','PATCH'])
@jwt_required()
def update_material(material_id):
  stmt = db.select(Material).filter_by(id=material_id)
  material_object = db.session.scalar(stmt)
  material_new = MaterialSchema().load(request.json)
  if material_object:
    owner_required()
    material_object.name = material_new.get('name', material_object.name)
    material_object.category = material_new.get('category', material_object.category)
    material_object.description = material_new.get('description', material_object.description)
    material_object.price = material_new.get('price', material_object.price)
    db.session.commit()
    return MaterialSchema().dump(material_new), 201
  else:
    return {'error': 'Material not found'}, 404

@materials_bp.route('/<int:material_id>', methods=['DELETE'])
@jwt_required()
def delete_material(material_id):
  stmt = db.select(Material).filter_by(id=material_id)
  material_object = db.session.scalar(stmt)
  if not material_object:
    return {'error': 'Material not found'}, 404   
  user_id = get_jwt_identity()
  stmt = db.select(User).filter_by(id=user_id)
  user_object = db.session.scalar(stmt)
  if user_object.is_owner:
    return {'Message': 'Material was successfully deleted'}, 200  
  db.session.delete(material_object)
  db.session.commit()   
  return {'error': 'Unauthorized'}, 401 








