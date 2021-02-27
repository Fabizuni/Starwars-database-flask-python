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
from models import db, User, Planets, Character, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/character', methods=['GET'])
def get_character():

    character_query = Character.query.all()
    
    results = list(map(lambda x: x.serialize(), character_query))

    return jsonify(results), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    
    planets_query = Planets.query.all()
    results = list(map(lambda x: x.serialize(), planets_query))
 
    return jsonify(results), 200

@app.route('/users', methods=['GET'])
def get_users():
    
    users_query = User.query.all()
    results = list(map(lambda x: x.serialize(), users_query))
 
    return jsonify(results), 200

@app.route('/character/<int:chaid>', methods=['GET'])
def get_oneCharacter(chaid):

    person = Character.query.get(chaid)    
    return jsonify(person.serialize()), 200

@app.route('/planets/<int:plaid>', methods=['GET'])
def get_onePlanet(plaid):

    planet = Planets.query.get(plaid)    
    return jsonify(planet.serialize()), 200

@app.route('/users/<int:userid>/favorites', methods=['GET'])
def get_favorites(userid):
    favorites = Favorites.query.filter_by(user_userid = userid)
    # favorites = Favorites.query.all()
    # print(favorites)
    results = list(map(lambda x: x.serialize(), favorites))
    # print(results)
    return jsonify(results), 200
    # return jsonify("hola"), 200

@app.route('/favorites', methods=["GET"])
def get_favorite():
    favorites = Favorites.query.all()
    results = list(map(lambda x: x.serialize(), favorites))
    return jsonify(results), 200

@app.route('/users/<int:userid>/favorites', methods=['POST'])
def add_fav(userid):
    
    # recibir info del request
    add_new_fav = request.get_json()
    newFav = Favorites(user_userid=userid, tipo=add_new_fav["tipo"],object_id=add_new_fav["object_id"])
    db.session.add(newFav)
    db.session.commit()

    return jsonify("All good"), 200

@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def del_fav(favorite_id):

    # recibir info del request
    
    delete_favorite = Favorites.query.get(favorite_id)
    if delete_favorite is None:
        raise APIException('Label not found', status_code=404)

    db.session.delete(delete_favorite)
    db.session.commit()

    return jsonify("All good"), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
