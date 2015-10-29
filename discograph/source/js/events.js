function dg_events_update_start(event) {

}

function dg_events_update_stop(event) {

}

function dg_events_network_fetch_start(event) {

}

function dg_events_network_fetch_stop(event) {

}

function dg_events_network_fetch_random(event) {

}

function dg_events_network_select_node(event) {

}

function dg_events_network_select_page(event) {
    $(event.target).tooltip('hide');
    dg_network_selectPage(event.payload.page);
    dg_network_startForceLayout();
    dg_network_reselectNode();
}

function dg_events_errored(event) {

}

function dg_events_init() {
    $(window).on('discograph:errored', dg_events_errored);
    $(window).on('discograph:network-fetch-start', dg_events_network_fetch_start);
    $(window).on('discograph:network-fetch-stop', dg_events_network_fetch_stop);
    $(window).on('discograph:network-fetch-random', dg_events_network_fetch_random);
    $(window).on('discograph:network-select-node', dg_events_network_select_node);
    $(window).on('discograph:network-select-page', dg_events_network_select_page);
    $(window).on('discograph:update-start', dg_events_update_start);
    $(window).on('discograph:update-stop', dg_events_update_stop);
}