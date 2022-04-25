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
from models import db, User, People, Planets, Fav_people, Fav_planets
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

#PEOPLE GET
@app.route('/people', methods=['GET'])
def getPeople():
    #funcion query all de alquemy
    all_people = People.query.all()#retorna arreglo de clases
    #traigo todos los personajes y le aplico un serialize
    arr_people = list(map(lambda x:x.serialize(), all_people))
    return jsonify({"People": arr_people})

#PEOPLE_ID GET
@app.route('/people/<int:people_id>', methods=['GET'])
def getPeopleID(people_id):
    one_people = People.query.get(people_id)
    if one_people:
        return jsonify({"Person": one_people.serialize()})
    else:
        return "error!"

#PLANETS GET
@app.route('/planets', methods=['GET'])
def getPlanets():
    all_planets = Planets.query.all()
    arr_planets = list(map(lambda x:x.serialize(), all_planets))
    return jsonify({"Planetas": arr_planets})

#PLANETS_ID GET
@app.route('/planets/<int:planets_id>', methods=['GET'])
def getPlanetsID(planets_id):
    one_planet = Planets.query.get(planets_id)
    if one_planet:
        return jsonify({"Planets": one_planet.serialize()})
    else:
        return "error!"

#USERS GET
@app.route('/users', methods=['GET'])
def getUser():
    all_User = User.query.all()
    arr_user = list(map(lambda x:x.serialize(), all_User))
    return jsonify({"Users": arr_user})

#USER_FAV GET
@app.route('/favPeople', methods=['GET'])
def getPeopleFav():
    all_favPeople = Fav_people.query.all()
    arr_fav = list(map(lambda x:x.serialize(), all_favPeople))
    return jsonify({"People Favs": arr_fav})

#USER_FAV GET
@app.route('/favPlanets', methods=['GET'])
def getPlanetsFav():
    all_favPlanets = Fav_planets.query.all()
    arr_fav = list(map(lambda x:x.serialize(), all_favPlanets))
    return jsonify({"Planets Favs": arr_fav})

#FAV_PEOPLE POST
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def addFavPeople(people_id):
    user = request.get_json()
    #validar si existe usuario
    checkUser = User.query.get(user['id'])
    if checkUser:
    #instanciar nuevo fav
        newFav = Fav_people()
        newFav.id_user = user['id']
        newFav.id_people = people_id

        db.session.add(newFav)
        db.session.commit()
        return("ok")
    else:
        return ("user doesn't exist")

#FAV_PLANETS POST
@app.route('/favorite/planets/<int:planets_id>', methods=['POST'])
def addFavPlanets(planets_id):
    user = request.get_json()
    #validar si existe usuario
    checkUser = User.query.get(user['id'])
    if checkUser:
    #instanciar nuevo fav
        newFav = Fav_planets()
        newFav.id_user = user['id']
        newFav.id_planets = planets_id

        db.session.add(newFav)
        db.session.commit()
        return("ok")
    else:
        return ("user doesn't exist")

#FAV_PEOPLE DELETE
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def deleteFavPeople(people_id):
    user = request.get_json() #{id:1}
    allFavs = Fav_people.query.filter_by(id_user=user['id'],id_people=people_id).all()
    for i in allFavs:
        db.session.delete(i)
    db.session.commit()

    return('deleted character')

#FAV_PLANETS DELETE
@app.route('/favorite/planets/<int:planets_id>', methods=['DELETE'])
def deleteFavPlanets(planets_id):
    user = request.get_json() #{id:1}
    allFavs = Fav_planets.query.filter_by(id_user=user['id'],id_planets=planets_id).all()
    for i in allFavs:
        db.session.delete(i)
    db.session.commit()

    return('deleted planet')
    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
