var dg = (function(dg){
    dg.init = function() {
        dg.graph.init();
        dg.typeahead.init();

        /*
        var entityKey = d3.select("body").attr("id");
        if (entityKey) {
            dg.navigateGraph(d3.select("body").attr("id"));
        }
        */
        if (dgData) {
            dg.history.pushState(dgData.center);
            dg.handleNewGraphData(null, dgData);
        }

        console.log('discograph initialized.')
    }
    return dg;
}(dg || {}));