# -*- encoding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import jsonify

from discograph import decorators
from discograph import exceptions
from discograph import helpers


blueprint = Blueprint('api', __name__, template_folder='templates')


@blueprint.route('/<entity_type>/timeline/<int:entity_id>')
@decorators.limit(max_requests=60, period=60)
def route__api__entity_type__timeline__entity_id(entity_type, entity_id):
    if entity_type != 'artist':
        raise exceptions.APIError(message='Bad Entity Type', status_code=404)
    data = helpers.get_timeline(
        entity_id,
        entity_type,
        )
    if data is None:
        raise exceptions.APIError(message='No Data', status_code=400)
    return jsonify(data)


@blueprint.route('/<entity_type>/network/<int:entity_id>')
@decorators.limit(max_requests=60, period=60)
def route__api__entity_type__network__entity_id(entity_type, entity_id):
    if entity_type not in ('artist', 'label'):
        raise exceptions.APIError(message='Bad Entity Type', status_code=404)
    parsed_args = helpers.parse_request_args(request.args)
    original_roles, original_year = parsed_args
    on_mobile = request.MOBILE
    data = helpers.get_network(
        entity_id,
        entity_type,
        on_mobile=on_mobile,
        cache=True,
        roles=original_roles,
        )
    if data is None:
        raise exceptions.APIError(message='No Data', status_code=400)
    return jsonify(data)


@blueprint.route('/search/<search_string>')
@decorators.limit(max_requests=120, period=60)
def route__api__search(search_string):
    data = helpers.search_entities(search_string)
    return jsonify(data)


@blueprint.route('/random')
@decorators.limit(max_requests=60, period=60)
def route__api__random():
    roles = ['Alias', 'Member Of']
    entity_type, entity_id = helpers.get_random_entity(
        roles=roles,
        )
    entity_type = {
        1: 'artist',
        2: 'label',
        }[entity_type]
    data = {'center': '{}-{}'.format(entity_type, entity_id)}
    return jsonify(data)