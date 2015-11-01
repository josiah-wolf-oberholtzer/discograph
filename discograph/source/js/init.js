$(document).ready(function() {
    dg_svg_init();
    dg_network_init();
    dg_timeline_init();
    dg_loading_init();
    dg_typeahead_init();
    dg_events_init();
    if (dgData) {
        var params = {'roles': $('#filter select').val()};
        dg_history_replaceState(dgData.center.key, params);
        dg_network_handleAsyncData(dgData, false);
    }
    $('[data-toggle="tooltip"]').tooltip();
    $('#brand').on("click touchstart", function(event) {
        event.preventDefault();
        $(this).tooltip('hide');
        $(this).trigger({
            type: 'discograph:random-fetch',
        });
    });
    $('#paging .next a').click(function(event) {
        $(this).trigger({
            type: 'discograph:network-select-page', 
            page: dg_network_getNextPage(),
        });
    });
    $('#paging .previous a').click(function(event) {
        $(this).trigger({
            type: 'discograph:network-select-page',
            page: dg_network_getPrevPage(),
        });
    });
    $('#filter-roles').multiselect({
        buttonWidth: "160px",
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        inheritClass: true,
        enableClickableOptGroups: true,
        maxHeight: 400,
        nonSelectedText: 'Select relationships'
    });
    $('#filter').on('reset', function(event) {
        $('#filter-roles option:selected').each(function() {
            $(this).prop('selected', false);
        });
        $('#filter-roles').multiselect('refresh');
        event.preventDefault();
    });
    $('#filter').submit(function(event) {
        event.preventDefault();
        $(window).trigger({
            type: 'discograph:network-fetch',
            entityKey: dg.network.data.json.center.key,
            pushHistory: true,
        });
    });
    $('#filter').fadeIn(3000);
    console.log('discograph initialized.');
});