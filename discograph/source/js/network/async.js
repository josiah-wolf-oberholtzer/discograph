function dg_network_navigate(key, pushHistory) {
    var entityType = key.split("-")[0];
    var entityId = key.split("-")[1];
    dg.network.isUpdating = true;
    var foundNode = dg.network.selections.node
        .filter(function(d) { return d.key == key; });
    if (foundNode.length == 1) {
        foundNode.each(function(d) {
            dg.network.newNodeCoords = [d.x, d.y];
        });
    } else {
        dg.network.newNodeCoords = [
            dg.network.dimensions[0] / 2,
            dg.network.dimensions[1] / 2,
        ];
    }
    dg_style_loading(true);
    var url = "/api/" + entityType + "/network/" + entityId;
    var params = {'roles': $('#filter select').val()};
    if (params.roles) {
        url += '?' + decodeURIComponent($.param(params));
    }
    $.ajax({
        cache: true,
        dataType: 'json',
        error: dg_network_handleAsyncError,
        success: function(data) {
            dg_network_handleAsyncData(data, pushHistory, params);
            },
        url: url,
    });
}

function dg_network_handleAsyncError(error) {
    var message = 'Something went wrong!';
    var status = error.status;
    if (status == 0) {
        status = 404;
    }
    if (status == 429) {
        message = 'Hey, slow down, buddy. Give it a minute.'
    }
    var text = '<div class="alert alert-danger alert-dismissible" role="alert">';
    text += '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
    text += '<strong>' + status + '!</strong> ' + message;
    text += '</div>';
    $('#flash').append(text);
    setTimeout(function() { dg.network.isUpdating = false; }, 2000);
    dg_style_loading(false);
}

function dg_network_handleAsyncData(json, pushHistory, params) {
    dg.network.data.json = JSON.parse(JSON.stringify(json));
    var key = json.center.key;
    document.title = "Disco/graph: " + json.center.name;
    $(document).attr("body").id = key;
    if (pushHistory === true) {
        dg_history_pushState(key, params);
    }
    dg.network.data.pageCount = json.pages;
    dg.network.pageData.currentPage = 1;
    if (1 < json.pages) {
        $('#paging').fadeIn();
    } else {
        $('#paging').fadeOut();
    }
    dg_network_processJson(json);
    dg_network_selectPage(1);
    dg_network_startForceLayout();
    dg_network_selectNode(dg.network.data.json.center.key);
    setTimeout(function() { dg.network.isUpdating = false; }, 2000);
    dg_style_loading(false);
}