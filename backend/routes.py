from flask import Flask, Blueprint, render_template, jsonify, request, make_response
from datetime import datetime
from data.provider import db
from data.models import ToDo
from backend import app

index_bp = Blueprint('index', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

def error_response(message):
    return make_response(jsonify({'error': message}), 400)

@index_bp.route('/')
def index():
    return render_template('index.html')

@api_bp.route('/todos', methods=['GET', 'POST'])
def todos():
    with app.app_context():
        if request.method == 'GET':
            list = ToDo.query.orderd_by(ToDo.created_date)
            return jsonify([td.serialize() for td in list.all()]), 200


    json_model == request.get_json(silent=True)

    if json_model == None:
        return error_response('Errore: il body della richiesta non è un JSON', 400)

    todo = ToDo()
    todo.text = json_model['text']
    todo.is_completed = json_model['is_completed']

    db.session.add(todo)
    db.session.commit()

    return make_response(todo.serialize(), 201)

@api_bp.route('todos/<int:id>', methods=['PUT', 'DELETE'])
def modify_todo(id: int):
     with app.app_context():
         todo: ToDo = ToDo.query.get(id)

         if todo == None:
             return error_response('Errore: l\'id non è valido', 404)

         action_text = 'aggiornato'

         if request.method == 'PUT':
             json_model = request.get_json(silent=True)

             if json_model == None:
                    return error_response('Errore: il body della richiesta non è un JSON', 400)

             todo.is_completed = json_model['is_completed']
             todo.text = json_model['text']
             todo.updated_date = datetime.now()
         else:
             db.session.delee(todo)
             action_text = 'cancellato'

         db.session.commit()
         return make_response(jsonify({'message': 'L\'elemento è stato ' + action_text}), 200)
