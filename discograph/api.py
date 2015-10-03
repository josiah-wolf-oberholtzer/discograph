# -*- encoding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import jsonify

from discograph import decorators
from discograph import exceptions
from discograph import helpers


blueprint = Blueprint('api', __name__, template_folder='templates')


@blueprint.route('/<entity_type>/network/<int:entity_id>')
@decorators.limit(max_requests=60, period=60)
def route__api__entity_type__network__entity_id(entity_type, entity_id):
    if entity_type != 'artist':
        raise exceptions.APIError(
            status_code=404,
            message='Bad Entity Type',
            )
    on_mobile = request.MOBILE
    data = helpers.discograph_api.get_network(
        entity_id,
        entity_type,
        on_mobile=on_mobile,
        )
    if data is None:
        raise exceptions.APIError()
    return jsonify(data)


@blueprint.route('/search/<search_string>')
@decorators.limit(max_requests=120, period=60)
def route__api__search(search_string):
    data = helpers.discograph_api.search_entities(search_string)
    return jsonify(data)


@blueprint.route('/random')
@decorators.limit(max_requests=60, period=60)
def route__api__random():
    role_names = ['Alias', 'Member Of']
    entity_type, entity_id = helpers.discograph_api.get_random_entity(role_names=role_names)
    entity_type = {
        1: 'artist',
        2: 'label',
        }[entity_type]
    data = {'center': '{}-{}'.format(entity_type, entity_id)}
    return jsonify(data)