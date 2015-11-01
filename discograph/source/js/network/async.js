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
    dg_network_toggle(true);
    dg_loading_toggle(false);
}