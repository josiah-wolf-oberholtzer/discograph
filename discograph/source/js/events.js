function dg_events_loading_toggle(event) {
    dg_loading_toggle(event.status);
}

function dg_events_network_toggle(event) {
    dg_network_toggle(event.status);
}

function dg_events_error(event) {
    var error = event.error;
    var message = 'Something went wrong!';
    var status = error.status;
    if (status == 0) {
        status = 404;
    } else if (status == 429) {
        message = 'Hey, slow down, buddy. Give it a minute.'
    }
    var text = '<div class="alert alert-danger alert-dismissible" role="alert">';
    text += '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
    text += '<strong>' + status + '!</strong> ' + message;
    text += '</div>';
    $('#flash').append(text);
    dg_network_toggle(true);
    dg_loading_toggle(false);
}

function dg_events_network_select_node(event) {
    dg_network_selectNode(event.key);
}

function dg_events_network_select_page(event) {
    $(event.target).tooltip('hide');
    dg_network_selectPage(event.page);
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
    /*
    $(window).on('discograph:error', dg_events_error);
    $(window).on('discograph:loading-toggle', dg_events_loading_toggle);
    $(window).on('discograph:network-fetch', $.debounce(500, function(event) {
        dg_events_network_fetch(event);
    }));
    $(window).on('discograph:network-select-node', dg_events_network_select_node);
    $(window).on('discograph:network-select-page', dg_events_network_select_page);
    $(window).on('discograph:network-toggle', dg_events_network_toggle);
    $(window).on('discograph:random-fetch', $.debounce(500, function(event) {
        dg_events_random_fetch(event);
    }));
    $(window).on('popstate', function(event) {
        dg_history_onPopState(event.originalEvent);
    });
    $(window).on('resize', $.debounce(100, function(event) { 
        dg_events_window_resize(event);
    }));
    */
}