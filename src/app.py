"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body =  members
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_member():
    body= request.get_json(silent=True)
    if body is None:
        return jsonify({'msg':'Debe enviar informacion en el body'}), 400
    if 'id' not in body:
        return jsonify({'msg':'El campo id es obligatorio'}), 400
    if 'first_name' not in body:
        return jsonify({'msg':'El campo first_name es obligatorio'}), 400
    if 'age' not in body:
        return jsonify({'msg':'El campo age es obligatorio'}), 400
    if 'lucky_numbers' not in body:
        return jsonify({'msg':'El campo lucky_numbers es obligatorio'}), 400
    new_member={
        'id': body['id'],
        'first_name': body['first_name'],
        'last_name': jackson_family.last_name,
        'age': body['age'],
        'lucky_numbers': body['lucky_numbers']
    }
    print (new_member)
    new_members=jackson_family.add_member(new_member)
    return jsonify({'msg':'ok','members':new_members}),200

@app.route('/member/<int:id>',methods=['GET'])
def get_single_member(id):
    print (f'Buscando miembro con id {id}')
    member=jackson_family.get_member(id)
    if member is None:
        print ('Miembro no encontrado')
        return jsonify({'msg':'Miembro no encontrado'}),404
    print(f'Miembro encontrado:{member}')
    result={
        'first_name':member['first_name'],
        'id':member['id'],
        'age':member['age'],
        'lucky_numbers':member['lucky_numbers']
    }
    return jsonify(result), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    print (f'Buscando miembro con id {id} para eliminar')
    if jackson_family.delete_member(id):
        return jsonify({'done':True}),200
    else:
        return jsonify({'msg':'Miembro no encontrado'}),400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
