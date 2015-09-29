var dg = (function(dg){
    var init = function() {
        $('#filter').submit(function(event) {
            console.log(event);
            event.preventDefault();
        });
    }
    dg.filter = {
        init: init,
    };
    return dg;
}(dg || {}));