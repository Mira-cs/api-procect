from flask import Blueprint
from models.material import Material, MaterialSchema
from init import db



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