var dg = (function(dg){
    dg.init = function() {
        dg.filter.init();
        dg.graph.init();
        dg.typeahead.init();
        if (dgData) {
            dg.history.pushState(dgData.center);
            dg.handleNewGraphData(null, dgData);
        }
        console.log('discograph initialized.')
    }
    return dg;
}(dg || {}));