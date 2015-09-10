var dg = (function(dg){
    dg.init = function() {
        dg.graph.init();
        dg.typeahead.init();
        var entityKey = d3.select("body").attr("id");
        if (entityKey) {
            dg.navigateGraph(d3.select("body").attr("id"));
        }
        console.log('discoGraph initialized.')
    }
    return dg;
}(dg || {}));