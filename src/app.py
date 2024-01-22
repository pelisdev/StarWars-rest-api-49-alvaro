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
from models import db, Personajes, Planetas, Usuarios, Favoritos
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
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/personajes', methods=['GET'])
def get_personajes():

    resultados = Personajes.query.all()
    if resultados ==[] :
        return jsonify({"msj":"No existen personajes"}), 400
    results = list(map(lambda personaje:personaje.serialize(),resultados))

    return jsonify(results), 200

@app.route('/planetas', methods=['GET'])
def get_planetas():

    resultados = Planetas.query.all()
    if resultados ==[] :
        return jsonify({"msj":"No existen planetas"}), 400
    results = list(map(lambda planeta:planeta.serialize(),resultados))

    return jsonify(results), 200

@app.route('/usuarios', methods=['GET'])
def get_usuarios():

    resultados = Usuarios.query.all()
    if resultados ==[] :
        return jsonify({"msj":"No existen Usuarios"}), 400
    results = list(map(lambda usuario:usuario.serialize(),resultados))

    return jsonify(results), 200

@app.route('/favoritos', methods=['GET'])
def get_favoritos():

    resultados = Favoritos.query.all()
    if resultados ==[] :
        return jsonify({"msj":"No existen favoritos"}), 400
    results = list(map(lambda favorito:favorito.serialize(),resultados))

    return jsonify(results), 200







# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)