var dg = (function(dg){
    dg.init = function() {
        dg.graph.init();
        dg.typeahead.init();
        if (dgData) {
            dg.history.pushState(dgData.center);
            dg.handleNewGraphData(dgData);
        }
        console.log('discograph initialized.')
    }
    return dg;
}(dg || {}));