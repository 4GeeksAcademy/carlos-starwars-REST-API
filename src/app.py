"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Favoritos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
    usuario_serializado = [ persona.serialize() for persona in users ]
    return jsonify(usuario_serializado), 200

@app.route('/user', methods=['POST'])
def add_user():

    body = request.json

    email = body.get('email', None)
    user_name = body.get('user_name', None)
    user_lastname = body.get('user_lastname', None)
    password = body.get ('password', None)
    date = body.date('date', None)

    if email == None or user_name == None or user_lastname == None or password == None or date == None :
        return jsonify({'msg' : 'Missing fields'}), 400
    
    try:
        new_user = User(email=email, user_name=user_name, user_lastname=user_lastname, date=date)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'msg' : 'Success'}), 201

    except:
        return jsonify({'msg' : 'Something happened unexpectedly'}), 500
    
@app.route('/characters', methods=['GET'])
def get_characters():
    characters  = Characters.query.all()
    char_serializados = [ character.serialize() for character in characters ]
    return jsonify(char_serializados), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planet_serializados = [ planet.serialize() for planet in planets ]
    return jsonify(planet_serializados), 200

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favoritos = Favoritos.query.all()
    fav_serializado = [ favorito.serialize() for favorito in favoritos ]
    return jsonify(fav_serializado), 200

@app.route('/favorites', methods=['POST'])
def add_favorites():
    body = request.json
    user_id = body.get('user_id', None)
    character_id = body.get ('character_id', None)
    planet_id = body.get('planet_id', None)

    if user_id == None or character_id == None or planet_id == None:
        return jsonify({'error' : f'Missing fields'}), 400
    
    user = User.query.get(user_id)
    character = Characters.query.get(character_id)
    planet = Planets. query.get(planet_id)

    if user == None or character == None or planet == None :
        return jsonify({ "error" : f"User with id {user_id} or Character with id {character_id} or Planet with id {planet_id} not found" }), 400

    new_favorite = Favoritos(user, character, planet)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 200
        

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
