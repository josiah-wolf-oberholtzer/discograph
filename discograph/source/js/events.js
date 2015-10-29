function dg_events_update_start(event) {

}

function dg_events_update_stop(event) {

}

function dg_events_network_request(event) {

}

function dg_events_network_response(event) {

}

function dg_events_random_request(event) {

}

function dg_events_random_response(event) {

}

function dg_events_error(event) {

}

function dg_events_network_select_node(event) {
    dg_network_selectNode(event.payload.key);
}

function dg_events_network_select_page(event) {
    $(event.target).tooltip('hide');
    dg_network_selectPage(event.payload.page);
    dg_network_startForceLayout();
    dg_network_reselectNode();
}

function dg_events_init() {
    $(window).on('discograph:network-request', dg_events_network_request);
    $(window).on('discograph:network-response', dg_events_network_response);
    $(window).on('discograph:random-request', dg_events_random_request);
    $(window).on('discograph:random-response', dg_events_random_response);
    $(window).on('discograph:network-select-node', dg_events_network_select_node);
    $(window).on('discograph:network-select-page', dg_events_network_select_page);
    $(window).on('discograph:update-start', dg_events_update_start);
    $(window).on('discograph:update-stop', dg_events_update_stop);
    $(window).on('popstate', dg_history_onPopState);
}