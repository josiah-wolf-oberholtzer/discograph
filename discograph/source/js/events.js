function dg_events_loading_toggle(event) {
    dg_loading_toggle(event.status);
}

function dg_events_network_toggle(event) {

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

function dg_events_window_resize(event) {
    var w = window,
        d = document,
        e = d.documentElement,
        g = d.getElementsByTagName('body')[0];
    dg.dimensions = [
        w.innerWidth || e.clientWidth || g.clientWidth,
        w.innerHeight|| e.clientHeight|| g.clientHeight,
    ];
    d3.select("#svg")
        .attr("width", dg.dimensions[0])
        .attr("height", dg.dimensions[1]);
    d3.selectAll('.centered')
        .attr('transform', "translate(" +
            dg.dimensions[0] / 2 + "," +
            dg.dimensions[1] / 2 + ")");
    dg.network.forceLayout.size(dg.dimensions).start();
}

function dg_events_init() {
    $(window).on('discograph:loading-toggle', dg_events_loading_toggle);
    $(window).on('discograph:network-toggle', dg_events_network_toggle);
    $(window).on('discograph:network-request', dg_events_network_request);
    $(window).on('discograph:network-response', dg_events_network_response);
    $(window).on('discograph:random-request', dg_events_random_request);
    $(window).on('discograph:random-response', dg_events_random_response);
    $(window).on('discograph:network-select-node', dg_events_network_select_node);
    $(window).on('discograph:network-select-page', dg_events_network_select_page);
    $(window).on('popstate', dg_history_onPopState);
    $(window).on('resize', $.debounce(100, function(event) { 
        console.log(event);
        dg_events_window_resize(event);
    }));
}