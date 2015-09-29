var dg = (function(dg){
    var bloodhound = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: "/api/search/%QUERY",
            wildcard: "%QUERY",
            filter: function(response) {
                return response.results;
            },
            rateLimitBy: 'throttle',
            rateLimitWait: 1000,
        },
    });
    var navigate = function() {
        var datum = $("#typeahead").data("selectedKey");
        if (datum) {
            dg.navigateGraph(datum);
            $("#typeahead").typeahead("close");
            $("#typeahead").blur();
            $('.navbar-toggle').click();
        };
    };
    var init = function() {
        var inputElement = $("#typeahead");
        var loadingElement = $("#search .loading");
        inputElement.typeahead(
            {
                hint: true, 
                highlight: true,
                minLength: 2,
            }, {
                name: "results",
                display: "name",
                source: bloodhound,
                limit: 20,
            })
        .keydown(function(event){
            if (event.keyCode == 13) {
                event.preventDefault();
                navigate();
            } else if (event.keyCode == 27) {
                inputElement.typeahead("close");
            }
        })
        .on("typeahead:asynccancel typeahead:asyncreceive", function(obj, datum) {
            loadingElement.addClass("invisible");
        })
        .on("typeahead:asyncrequest", function(obj, datum) {
            loadingElement.removeClass("invisible");
        })
        .on("typeahead:autocomplete", function(obj, datum) {
            $(this).data("selectedKey", datum.key);
        })
        .on("typeahead:render", function(event, suggestion, async, name) {
            if (suggestion !== undefined) {
                $(this).data("selectedKey", suggestion.key);
            } else {
                $(this).data("selectedKey", null);
            }
        })
        .on("typeahead:selected", function(obj, datum) {
            $(this).data("selectedKey", datum.key);
            navigate();
        });
        $('#search .clear').click(function() {
            $('#typeahead').typeahead('val', '');
        });
    };
    dg.typeahead = {
        init: init,
    };
    return dg;
}(dg || {}));