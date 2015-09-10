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
    dg.typeahead.init = function() {
        var inputElement = $("#typeahead");
        var loadingElement = $("#search .loading");
        inputElement.typeahead(
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
            .keydown(function(event){
                if (event.keyCode == 13) {
                    event.preventDefault();
                    dg.typeahead.navigate();
                } else if (event.keyCode == 27) {
                    dg.typeahead.inputElement.typeahead("close");
                }
            })
            .on("typeahead:asynccancel typeahead:asyncreceive", function(obj, datum) {
                dg.typeahead.loadingElement.addClass("invisible");
            })
            .on("typeahead:asyncrequest", function(obj, datum) {
                dg.typeahead.loadingElement.removeClass("invisible");
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
                dg.typeahead.navigate();
            });
        )
    }
    return dg;
}(dg || {}));