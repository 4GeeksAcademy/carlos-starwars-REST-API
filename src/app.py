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
from models import db, User
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
    response_body = {
        "msg" : "Hello, this is me",
    }

    return jsonify(response_body), 200
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

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
