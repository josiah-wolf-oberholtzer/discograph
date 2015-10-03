# -*- encoding: utf-8 -*-
import json
from flask import Blueprint
from flask import make_response
from flask import redirect
from flask import request
from flask import render_template

from discograph import exceptions
from discograph import helpers


blueprint = Blueprint('ui', __name__, template_folder='templates')


@blueprint.route('/')
def route__index():
    is_a_return_visitor = request.cookies.get('is_a_return_visitor')
    initial_json = 'var dgData = null;'
    rendered_template = render_template(
        'index.html',
        application_url=helpers.discograph_api.application_url,
        initial_json=initial_json,
        is_a_return_visitor=is_a_return_visitor,
        og_title='Disco/graph: visualizing music as a social graph',
        og_url='/',
        on_mobile=request.MOBILE,
        title='Disco/graph: Visualizing music as a social graph',
        )
    response = make_response(rendered_template)
    response.set_cookie('is_a_return_visitor', 'true')
    return response


@blueprint.route('/<entity_type>/<int:entity_id>')
def route__entity_type__entity_id(entity_type, entity_id):
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
        raise exceptions.APIError(
            message='No Data',
            status_code=500,
            )
    initial_json = json.dumps(
        data,
        sort_keys=True,
        indent=4,
        separators=(',', ': '),
        )
    initial_json = 'var dgData = {};'.format(initial_json)
    entity_name = [_['name'] for _ in data['nodes']
        if _['key'] == data['center']][0]
    is_a_return_visitor = request.cookies.get('is_a_return_visitor')
    key = '{}-{}'.format(entity_type, entity_id)
    url = '/{}/{}'.format(entity_type, entity_id)
    title = 'Disco/graph: {}'.format(entity_name)
    rendered_template = render_template(
        'index.html',
        application_url=helpers.discograph_api.application_url,
        initial_json=initial_json,
        is_a_return_visitor=is_a_return_visitor,
        key=key,
        og_title='Disco/graph: The "{}" network'.format(entity_name),
        og_url=url,
        on_mobile=on_mobile,
        title=title,
        )
    response = make_response(rendered_template)
    response.set_cookie('is_a_return_visitor', 'true')
    return response


@blueprint.route('/random')
def route__random():
    entity_type, entity_id = helpers.discograph_api.get_random_entity()
    if entity_type == 1:
        return redirect('/artist/{}'.format(entity_id), status_code=302)
    return redirect('/label/{}'.format(entity_id), status_code=302)