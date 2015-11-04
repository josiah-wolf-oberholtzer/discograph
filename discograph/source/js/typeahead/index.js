function dg_typeahead_init() {
    var dg_typeahead_bloodhound = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: "/api/search/%QUERY",
            wildcard: "%QUERY",
            filter: function(response) {
                return response.results;
            },
            rateLimitBy: 'debounce',
            rateLimitWait: 300,
        },
    });
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
            limit: 20,
            source: dg_typeahead_bloodhound,
            templates: {
                suggestion: function(data) {
                    return '<div>' +
                        '<span>' + data.name + '</span>' +
                        ' <em>(' + data.key.split('-')[0] + ')</em></div>';
                },
            },
        })
    .keydown(function(event){
        if (event.keyCode == 13) {
            event.preventDefault();
            dg_typeahead_navigate();
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
        dg_typeahead_navigate();
    });
    $('#search .clear').click(function() {
        $('#typeahead').typeahead('val', '');
    });
}

function dg_typeahead_navigate() {
    var datum = $("#typeahead").data("selectedKey");
    if (datum) {
        $("#typeahead").typeahead("close");
        $("#typeahead").blur();
        $('.navbar-toggle').click();
        $(window).trigger({
            type: 'discograph:request-network',
            entityKey: datum,
            pushHistory: true,
        });
    };
}