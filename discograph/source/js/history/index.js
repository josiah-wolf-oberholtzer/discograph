function dg_history_onPopState(event) {
    if (!event || !event.state || !event.state.key) {
        return;
    }
    var entityKey = event.state.key;
    var entityType = entityKey.split("-")[0];
    var entityId = entityKey.split("-")[1];
    var url = "/" + entityType + "/" + entityId;
    ga('send', 'pageview', url);
    ga('set', 'page', url);
    $(window).trigger({
        type: 'discograph:request-network',
        entityKey: event.state.key,
        pushHistory: false,
    });
}

function dg_history_pushState(entityKey, params) {
    var entityType = entityKey.split("-")[0];
    var entityId = entityKey.split("-")[1];
    var title = document.title;
    var url = "/" + entityType + "/" + entityId;
    if (params) {
        url += "?" + decodeURIComponent($.param(params));
    }
    var state = {key: entityKey, params: params};
    window.history.pushState(state, title, url);
    ga('send', 'pageview', url);
    ga('set', 'page', url);
}

function dg_history_replaceState(entityKey, params) {
    var entityType = entityKey.split("-")[0];
    var entityId = entityKey.split("-")[1];
    var title = document.title;
    var url = "/" + entityType + "/" + entityId;
    if (params) {
        url += "?" + decodeURIComponent($.param(params));
    }
    var state = {key: entityKey, params: params};
    window.history.replaceState(state, title, url);
    ga('send', 'pageview', url);
    ga('set', 'page', url);
}