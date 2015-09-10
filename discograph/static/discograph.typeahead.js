var dg = (function(dg){

    dg.typeahead = {};

    dg.typeahead.bloodhound = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: "/api/search/%QUERY",
            wildcard: "%QUERY",
            filter: function(response) {
                return response.results;
            },
        },
    });

    dg.typeahead.navigate = function() {
        var datum = $("#typeahead").data("selectedKey");
        if (datum) {
            dg.navigateGraph(datum);
            $("#typeahead").typeahead("close");
            $("#typeahead").blur();
        };
    }

    return dg;

}(dg || {}));

dg.typeahead.inputElement = $("#typeahead");

dg.typeahead.loadingElement = $("#search .loading");

dg.typeahead.inputElement.typeahead(
    {
        hint: true, 
        highlight: true,
        minLength: 1,
    }, {
        name: "results",
        display: "name",
        source: dg.typeahead.bloodhound,
        limit: 20,
    }
);

dg.typeahead.inputElement.on("typeahead:render", function(event, suggestion, async, name) {
    if (suggestion !== undefined) {
        $(this).data("selectedKey", suggestion.key);
    } else {
        $(this).data("selectedKey", null);
    }
});

dg.typeahead.inputElement.on("typeahead:selected", function(obj, datum) {
    $(this).data("selectedKey", datum.key);
    dg.typeahead.navigate();
});

dg.typeahead.inputElement.on("typeahead:autocomplete", function(obj, datum) {
    $(this).data("selectedKey", datum.key);
})

dg.typeahead.inputElement.on("typeahead:asyncrequest", function(obj, datum) {
    dg.typeahead.loadingElement.removeClass("invisible");
})

dg.typeahead.inputElement.on("typeahead:asynccancel typeahead:asyncreceive", function(obj, datum) {
    dg.typeahead.loadingElement.addClass("invisible");
})

dg.typeahead.inputElement.on("typeahead:asyncreceive", function(obj, datum) {
    dg.typeahead.loadingElement.addClass("invisible");
})

dg.typeahead.inputElement.keydown(function(event){
    if (event.keyCode == 13) {
        event.preventDefault();
        dg.typeahead.navigate();
    } else if (event.keyCode == 27) {
        dg.typeahead.inputElement.typeahead("close");
    }
});