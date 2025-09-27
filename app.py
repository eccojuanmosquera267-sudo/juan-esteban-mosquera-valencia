from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['JWT_SECRET_KEY'] = 'un_secreto_largo'
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    description = db.Column(db.String)

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.before_first_request
def create_tables():
    db.create_all()

# Crear
@app.route('/api/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    errors = product_schema.validate(data)
    if errors: return jsonify(errors), 400
    p = Product(**data)
    db.session.add(p)
    db.session.commit()
    return product_schema.jsonify(p), 201

# Leer lista
@app.route('/api/products', methods=['GET'])
def list_products():
    q = request.args.get('q')
    query = Product.query
    if q:
        query = query.filter(Product.name.ilike(f'%{q}%'))
    items = query.all()
    return products_schema.jsonify(items)

# Leer uno
@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    p = Product.query.get_or_404(id)
    return product_schema.jsonify(p)

# Actualizar
@app.route('/api/products/<int:id>', methods=['PATCH','PUT'])
@jwt_required()
def update_product(id):
    p = Product.query.get_or_404(id)
    data = request.get_json()
    for k in ['name','price','stock','description']:
        if k in data: setattr(p, k, data[k])
    db.session.commit()
    return product_schema.jsonify(p)

# Eliminar
@app.route('/api/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    p = Product.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return '', 204

# Auth demo (usuario demo)
@app.route('/login', methods=['POST'])
def login():
    d = request.get_json()
    # demo: aceptar cualquier usuario/password 'test'
    if d.get('username')=='test' and d.get('password')=='test':
        token = create_access_token(identity='test')
        return jsonify(access_token=token)
    return jsonify({"msg":"Bad credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
 