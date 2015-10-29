function dg_network_nextPage() {
    var page = dg.network.pageData.currentPage + 1;
    if (dg.network.data.pageCount < page) {
        page = 1;
    }
    dg_network_selectPage(page);
    dg_network_startForceLayout();
    dg_network_reselectNode();
}

function dg_network_prevPage() {
    var page = dg.network.pageData.currentPage - 1;
    if (page == 0) {
        page = dg.network.data.pageCount;
    }
    dg_network_selectPage(page);
    dg_network_startForceLayout();
    dg_network_reselectNode();
}

function dg_network_selectPage(page) {
    if ((1 <= page) && (page <= dg.network.data.pageCount)) {
        dg.network.pageData.currentPage = page;
    } else {
        dg.network.pageData.currentPage = 1;
    }
    var currentPage = dg.network.pageData.currentPage;
    var pageCount = dg.network.data.pageCount;
    if (currentPage == 1) {
        var prevPage = pageCount;
    } else {
        var prevPage = currentPage - 1;
    }
    var prevText = prevPage + ' / ' + pageCount;
    if (currentPage == pageCount) {
        var nextPage = 1;
    } else {
        var nextPage = currentPage + 1;
    }
    var nextText = nextPage + ' / ' + pageCount;
    $('#paging .previous-text').text(prevText);
    $('#paging .next-text').text(nextText);
    var filteredNodes = dg.network.data.nodeMap.values().filter(function(d) {
        return (-1 != d.pages.indexOf(currentPage));
    });
    var filteredLinks = dg.network.data.linkMap.values().filter(function(d) {
        return (-1 != d.pages.indexOf(currentPage));
    });
    dg.network.pageData.nodes.length = 0;
    dg.network.pageData.links.length = 0;
    Array.prototype.push.apply(dg.network.pageData.nodes, filteredNodes);
    Array.prototype.push.apply(dg.network.pageData.links, filteredLinks);
    dg.network.forceLayout.nodes(filteredNodes);
    dg.network.forceLayout.links(filteredLinks);
}