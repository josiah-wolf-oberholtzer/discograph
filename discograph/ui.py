# -*- encoding: utf-8 -*-
import json
from flask import Blueprint
from flask import current_app
from flask import make_response
from flask import request
from flask import render_template

from discograph import exceptions
from discograph import helpers


blueprint = Blueprint('ui', __name__, template_folder='templates')


@blueprint.route('/')
def route__index():
    import discograph
    app = current_app._get_current_object()
    is_a_return_visitor = request.cookies.get('is_a_return_visitor')
    initial_json = 'var dgData = null;'
    on_mobile = request.MOBILE
    parsed_args = helpers.parse_request_args(request.args)
    original_roles, original_year = parsed_args
    multiselect_mapping = discograph.CreditRole.get_multiselect_mapping()
    rendered_template = render_template(
        'index.html',
        application_url=app.config['APPLICATION_ROOT'],
        initial_json=initial_json,
        is_a_return_visitor=is_a_return_visitor,
        multiselect_mapping=multiselect_mapping,
        og_title='Disco/graph: visualizing music as a social graph',
        og_url='/',
        on_mobile=on_mobile,
        original_roles=original_roles,
        original_year=original_year,
        title='Disco/graph: Visualizing music as a social graph',
        )
    response = make_response(rendered_template)
    response.set_cookie('is_a_return_visitor', 'true')
    return response


@blueprint.route('/<entity_type>/<int:entity_id>')
def route__entity_type__entity_id(entity_type, entity_id):
    import discograph
    app = current_app._get_current_object()
    parsed_args = helpers.parse_request_args(request.args)
    original_roles, original_year = parsed_args
    if entity_type not in ('artist', 'label'):
        raise exceptions.APIError(message='Bad Entity Type', status_code=404)
    on_mobile = request.MOBILE
    data = helpers.get_network(
        entity_id,
        entity_type,
        on_mobile=on_mobile,
        cache=True,
        )
    if data is None:
        raise exceptions.APIError(message='No Data', status_code=500)
    initial_json = json.dumps(
        data,
        sort_keys=True,
        indent=4,
        separators=(',', ': '),
        )
    initial_json = 'var dgData = {};'.format(initial_json)
    entity_name = data['center']['name']
    is_a_return_visitor = request.cookies.get('is_a_return_visitor')
    key = '{}-{}'.format(entity_type, entity_id)
    url = '/{}/{}'.format(entity_type, entity_id)
    title = 'Disco/graph: {}'.format(entity_name)
    multiselect_mapping = discograph.CreditRole.get_multiselect_mapping()
    rendered_template = render_template(
        'index.html',
        application_url=app.config['APPLICATION_ROOT'],
        initial_json=initial_json,
        is_a_return_visitor=is_a_return_visitor,
        key=key,
        multiselect_mapping=multiselect_mapping,
        og_title='Disco/graph: The "{}" network'.format(entity_name),
        og_url=url,
        on_mobile=on_mobile,
        original_roles=original_roles,
        original_year=original_year,
        title=title,
        )
    response = make_response(rendered_template)
    response.set_cookie('is_a_return_visitor', 'true')
    return response