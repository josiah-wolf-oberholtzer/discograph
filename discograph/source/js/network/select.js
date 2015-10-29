function dg_network_selectNode(key) {
    dg.network.pageData.selectedNodeKey = key;
    if (key !== null) {
        var nodeOn = dg.network.layers.root.selectAll('.' + key);
        var nodeOff = dg.network.layers.root.selectAll('*:not(.' + key + ')');
        var linkKeys = nodeOn.datum().links;
        var linkOn = dg.network.selections.link.filter(function(d) {
            return 0 <= linkKeys.indexOf(d.key);
        });
        var linkOff = dg.network.selections.link.filter(function(d) {
            return linkKeys.indexOf(d.key) == -1;
        });
        nodeOn.classed('selected', true);
        nodeOff.classed('selected', false);
        linkOn.classed('selected', true);
        linkOff.classed('selected', false);
        var node = dg.network.data.nodeMap.get(key);
        var url = 'http://discogs.com/' + node.type + '/' + node.id;
        $('#entity-name').text(node.name);
        $('#entity-link')
            .attr('href', url)
            .removeClass('hidden')
            .show(0);
        nodeOn.moveToFront();
    } else {
        var nodeOff = dg.network.layers.root.selectAll('.node');
        var linkOff = dg.network.selections.link;
        nodeOff.classed('selected', false);
        linkOff.classed('selected', false);
        $('#entity-link').hide(0);
        return;
    }
}

function dg_network_reselectNode() {
    var selectedNodeKey = dg.network.pageData.selectedNodeKey;
    if (selectedNodeKey !== null) {
        var selectedNode = dg.network.data.nodeMap.get(selectedNodeKey);
        var currentPage = dg.network.pageData.currentPage;
        if (-1 == selectedNode.pages.indexOf(currentPage)) {
            dg.network.pageData.selectedNodeKey = null;
        }
        dg_network_selectNode(dg.network.pageData.selectedNodeKey);
    }
}