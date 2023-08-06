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
from models import db, User, people,Planet,FavoritesPlanet,FavoritesChar
#from models import Person
import random

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
    user_data = [i.serialize() for i in users ]  

    return jsonify(user_data), 200

@app.route("/people", methods =["GET"])
def all_people_getinator():
    people = people.query.all()
    people_data = [i.to_dict() for i in people]
    people_json = jsonify(people_data)

    return(people_json)

@app.route("/people/<int:people_id>", methods = ["GET"])
def one_people_getinator(people_id):
    person = people.query.get(people_id)
    person_dic = person.to_dict()
    return(jsonify(person_dic))

@app.route ( "/planet",methods=["GET"])
def all_planet_getinator():
    planets = Planet.query.all()
    planet_data = [i.to_dict() for i in planets]
    planet_json = jsonify(planet_data)
    return(planet_json)

@app.route ("/planet/<int:planet_id>",methods=["GET"])
def one_planet_getinator(planet_id):
    planet = Planet.query.get(planet_id)
    planet_data = planet.to_dict()
    planet_json=jsonify(planet_data)
    return planet_json

@app.route("/user/favorites",methods =["GET"])
def favorite_getinator():
    id = 1
    peoplefav = FavoritesChar.query.filter(FavoritesChar.user_id == id).all()
    planetfav = FavoritesPlanet.query.filter(FavoritesPlanet.user_id == id).all()

    peoples_id = []
    planets_id = []
    allfav = []
    for i in peoplefav:
        peoples_id.append(i.char_id)
    for i in planetfav:
        planets_id.append(i.planet_id)
    
    for i in peoples_id:
        person = people.query.get(i)
        person_dic = person.to_dict()
        allfav.append(person_dic)
    for i in planets_id:
        planet = Planet.query.get(i)
        planet_dic = planet.to_dict()
        allfav.append(planet_dic)

    return jsonify(allfav)

@app.route ("/favorite/planet/<int:planet_id>", methods =["POST"])
def planet_fav_addinator(planet_id):
    planet = Planet.query.get(planet_id)
    to_add = FavoritesPlanet(planet_id = planet.id, user_id = 1)
    db.session.add(to_add)
    db.session.commit()

    return(jsonify(to_add.to_dict()))

@app.route ("/favorite/people/<int:people_id>", methods =["POST"])
def people_fav_addinator(people_id):
    people = people.query.get(people_id)
    to_add = FavoritesChar(char_id = people.id, user_id = 1)
    db.session.add(to_add)
    db.session.commit()

    return(jsonify(to_add.to_dict()))
@app.route ("/favorite/planet/<int:planet_id>", methods =["DELETE"])
def planet_fav_deletinator(planet_id):
    
    to_delete = FavoritesPlanet.query.filter(FavoritesPlanet.planet_id == planet_id).first()
    db.session.delete(to_delete)
    db.session.commit()

    response_body = {
        "msg": "exito "
    }
    return jsonify(response_body)

@app.route ("/favorite/people/<int:people_id>", methods =["DELETE"])
def people_fav_deletinator(people_id):
    
    to_delete = FavoritesChar.query.filter(FavoritesChar.char_id == people_id).first()
    db.session.delete(to_delete)
    db.session.commit()

    response_body = {
        "msg": "exito "
    }
    return jsonify(response_body)




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)