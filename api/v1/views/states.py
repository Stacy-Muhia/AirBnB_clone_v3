#!/usr/bin/python3
"""This script updated objects prior States objects"""

from flask import Flask
from flask import Flask, abort
from api.v1.views import app_views
from os import name
from models.state import State
from flask import request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Function retrieves all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def gets_objects():
    """Function gets objects"""
    objects = storage.all('State')
    lista = []
    for state in objects.values():
        lista.append(state.to_dict())
    return jsonify(lista)


@app_views.route('/states/<string:stateid>', methods=['GET'],
                 strict_slashes=False)
def update_state():
    """Function updates State object id"""
    objects = storage.get('State', 'state_id')
    if objects is None:
        abort(404)
    return jsonify(objects.to_dict()), 'OK'


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Function creates a State object"""
    response = request.get_json()
    if response is None:
        abort(400, {'Not a JSON'})
    if "name" not in response:
        abort(400, {'Missing name'})
    stateObject = State(name=response['name'])
    storage.new(stateObject)
    storage.save()
    return jsonify(stateObject.to_dict()), '201'


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def retrieve_state():
    """Function retrieves states"""
    response = request.get_json()
    if response is None:
        abort(400, {'Not a JSON'})
    stateObject = storage.get(State, state_id)
    if stateObject is None:
        abort(404)
    ignoreKeys = ['id', 'created_at', 'updated_at']
    for key in response.items():
        if key not in ignoreKeys:
            setattr(stateObject, key)
    storage.save()
    return jsonify(stateObject.to_dict()), '200'


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state():
    """Function deletes an object"""
    stateObject = storage.get(State, state_id)
    if stateObject is None:
        abort(404)
    storage.delete(stateObject)
    storage.save()
    return jsonify({}), '200'
