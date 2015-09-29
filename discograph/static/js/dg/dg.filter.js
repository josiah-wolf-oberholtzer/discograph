var dg = (function(dg){
    var init = function() {
        $('#filter').submit(function(event) {
            dg.navigateGraph(dg.graph.centerNodeKey);
            event.preventDefault();
        });
    }
    dg.filter = {
        init: init,
    };
    return dg;
}(dg || {}));