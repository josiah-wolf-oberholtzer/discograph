$(document).ready(function() {
    dg_svg_init();
    dg_network_init();
    dg_relations_init();
    dg_loading_init();
    dg_typeahead_init();
    $('[data-toggle="tooltip"]').tooltip();
    $('#brand').on("click touchstart", function(event) {
        event.preventDefault();
        $(this).tooltip('hide');
        $(this).trigger({
            type: 'discograph:request-random',
        });
    });
    $('#paging .next a').click(function(event) {
        $(this).trigger({
            type: 'discograph:select-next-page', 
        });
        $(this).tooltip('hide');
    });
    $('#paging .previous a').click(function(event) {
        $(this).trigger({
            type: 'discograph:select-previous-page',
        });
        $(this).tooltip('hide');
    });
    $('#filter-roles').select2().on('select2:select', function(event) {
        $(window).trigger({
            type: 'discograph:request-network',
            entityKey: dg.network.data.json.center.key,
            pushHistory: true,
        });
    });
    $('#filter-roles').select2().on('select2:unselect', function(event) {
        $(window).trigger({
            type: 'discograph:request-network',
            entityKey: dg.network.data.json.center.key,
            pushHistory: true,
        });
    });
    $('#filter').fadeIn(3000);
    dg.fsm = new DiscographFsm();
    console.log('discograph initialized.');
});