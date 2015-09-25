var dg = (function(dg){ 

    dg.history = {
        onPopState: function(event) {
            if (!event || !event.state || !event.state.key) {
                return;
            }
            var entityKey = event.state.key;
            var entityType = entityKey.split("-")[0];
            var entityId = entityKey.split("-")[1];
            var url = "/" + entityType + "/" + entityId;
            ga('send', 'pageview', url);
            ga('set', 'page', url);
            dg.updateGraph(event.state.key);
        },
        pushState: function(entityKey, params) {
            var entityType = entityKey.split("-")[0];
            var entityId = entityKey.split("-")[1];
            var title = document.title;
            var url = "/" + entityType + "/" + entityId;
            if (params) { url += "?" + $.params(params); }
            var state = {key: entityKey, params: params};
            window.history.pushState(state, title, url);
            ga('send', 'pageview', url);
            ga('set', 'page', url);
        },
    }

    return dg;

}(dg || {}));