var dg = (function(dg){

dg.timeline = {
    layers: {
        root: null,
        },
    };

function dg_timeline_init() {
    dg.timeline.layers.root = d3.select("#svg").append("g")
        .attr("id", "timelineLayer");
}

dg.network = {
    dimensions: [0, 0],
    forceLayout: null,
    isUpdating: false,
    newNodeCoords: [0, 0],
    data: {
        json: null,
        nodeMap: d3.map(),
        linkMap: d3.map(),
        maxDistance: 0,
        pageCount: 1,
        },
    pageData: {
        currentPage: 1,
        links: [],
        nodes: [],
        selectedNodeKey: null,
        },
    selections: {
        halo: null,
        hull: null,
        node: null,
        link: null,
        text: null,
        },
    layers: {
        root: null,
        halo: null,
        text: null,
        node: null,
        link: null,
        },
    };

function dg_network_nextPage() {
    var page = dg.network.pageData.currentPage + 1;
    if (dg.network.data.pageCount < page) {
        page = 1;
    }
    dg_network_selectPage(page);
    dg_network_startForceLayout();
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

function dg_network_prevPage() {
    var page = dg.network.pageData.currentPage - 1;
    if (page == 0) {
        page = dg.network.data.pageCount;
    }
    dg_network_selectPage(page);
    dg_network_startForceLayout();
    dg_network_reselectNode();
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

function dg_warn() { 
}

function dg_network_setupForceLayout() {
    return d3.layout.force()
        .nodes(dg.network.pageData.nodes)
        .links(dg.network.pageData.links)
        .size(dg.network.dimensions)
        .on("tick", dg_network_tick)
        .linkStrength(1.5)
        .friction(0.9)
        .linkDistance(function(d, i) {
            if (d.isSpline) {
                if (d.role == 'Released On') {
                    return 100;
                }
                return 50;
            } else if (d.role == 'Alias') {
                return 100;
            } else if (d.role == 'Released On') {
                return 200;
            } else {
                return 90 + (Math.random() * 20);
            }
        })
        .charge(-300)
        //.chargeDistance(1000)
        .gravity(0.2)
        .theta(0.8)
        .alpha(0.1);
}

function dg_color_greyscale(d) {
    var hue = 0;
    var saturation = 0;
    var lightness = (d.distance / (dg.network.data.maxDistance + 1));
    return d3.hsl(hue, saturation, lightness).toString();
}

function dg_color_heatmap(d) {
    var hue = ((d.distance / 12) * 360) % 360;
    var variation_a = ((d.id % 5) - 2) / 20;
    var variation_b = ((d.id % 9) - 4) / 80;
    var saturation = 0.67 + variation_a;
    var lightness = 0.5 + variation_b;
    return d3.hsl(hue, saturation, lightness).toString();
}

function dg_history_onPopState(event) {
    if (!event || !event.state || !event.state.key) {
        return;
    }
    var entityKey = event.state.key;
    var entityType = entityKey.split("-")[0];
    var entityId = entityKey.split("-")[1];
    var url = "/" + entityType + "/" + entityId;
    ga('send', 'pageview', url);
    ga('set', 'page', url);
    dg_network_navigate(event.state.key, false);
}

function dg_history_pushState(entityKey, params) {
    var entityType = entityKey.split("-")[0];
    var entityId = entityKey.split("-")[1];
    var title = document.title;
    var url = "/" + entityType + "/" + entityId;
    if (params) { 
        url += "?" + decodeURIComponent($.param(params));
    }
    var state = {key: entityKey, params: params};
    window.history.pushState(state, title, url);
    ga('send', 'pageview', url);
    ga('set', 'page', url);
}

function dg_history_replaceState(entityKey, params) {
    var entityType = entityKey.split("-")[0];
    var entityId = entityKey.split("-")[1];
    var title = document.title;
    var url = "/" + entityType + "/" + entityId;
    if (params) {
        url += "?" + decodeURIComponent($.param(params));
    }
    var state = {key: entityKey, params: params};
    window.history.replaceState(state, title, url);
    ga('send', 'pageview', url);
    ga('set', 'page', url);
}

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

function dg_typeahead_init() {
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
        dg_network_navigate(datum, true);
        $("#typeahead").typeahead("close");
        $("#typeahead").blur();
        $('.navbar-toggle').click();
    };
}

function dg_network_handleAsyncError(error) {
    var message = 'Something went wrong!';
    var status = error.status;
    if (status == 0) {
        status = 404;
    }
    if (status == 429) {
        message = 'Hey, slow down, buddy. Give it a minute.'
    }
    var text = '<div class="alert alert-danger alert-dismissible" role="alert">';
    text += '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
    text += '<strong>' + status + '!</strong> ' + message;
    text += '</div>';
    $('#flash').append(text);
    setTimeout(function() { dg.network.isUpdating = false; }, 2000);
    dg_style_loading(false);
}

function dg_network_handleAsyncData(json, pushHistory, params) {
    dg.network.data.json = JSON.parse(JSON.stringify(json));
    var key = json.center.key;
    document.title = "Disco/graph: " + json.center.name;
    $(document).attr("body").id = key;
    if (pushHistory === true) {
        dg_history_pushState(key, params);
    }
    dg.network.data.pageCount = json.pages;
    dg.network.pageData.currentPage = 1;
    if (1 < json.pages) {
        $('#paging').fadeIn();
    } else {
        $('#paging').fadeOut();
    }
    dg_network_processJson(json);
    dg_network_selectPage(1);
    dg_network_startForceLayout();
    dg_network_selectNode(dg.network.data.json.center.key);
    setTimeout(function() { dg.network.isUpdating = false; }, 2000);
    dg_style_loading(false);
}

function dg_style_loading(state) {
    if (state) {
        dg.network.layers.root.transition()
            .duration(250)
            .style("opacity", 0.333);
        $("#page-loading")
            .removeClass("glyphicon-random")
            .addClass("glyphicon-animate glyphicon-refresh");
    } else {
        dg.network.layers.root.transition()
            .delay(250)
            .duration(1000)
            .style("opacity", 1);
        $("#page-loading")
            .removeClass("glyphicon-animate glyphicon-refresh")
            .addClass("glyphicon-random");
    }
}

function dg_network_navigate(key, pushHistory) {
    var entityType = key.split("-")[0];
    var entityId = key.split("-")[1];
    dg.network.isUpdating = true;
    var foundNode = dg.network.selections.node
        .filter(function(d) { return d.key == key; });
    if (foundNode.length == 1) {
        foundNode.each(function(d) {
            dg.network.newNodeCoords = [d.x, d.y];
        });
    } else {
        dg.network.newNodeCoords = [
            dg.network.dimensions[0] / 2,
            dg.network.dimensions[1] / 2,
        ];
    }
    dg_style_loading(true);
    var url = "/api/" + entityType + "/network/" + entityId;
    var params = {'roles': $('#filter select').val()};
    if (params.roles) { 
        url += '?' + decodeURIComponent($.param(params));
    }
    $.ajax({
        cache: true,
        dataType: 'json',
        error: dg_network_handleAsyncError,
        success: function(data) {
            dg_network_handleAsyncData(data, pushHistory, params);
            },
        url: url,
    });
}

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

function dg_network_getOuterRadius(d) {
    if (0 < d.size) {
        return 12 + (Math.sqrt(d.size) * 2);
    }
    return 9 + (Math.sqrt(d.size) * 2);
}

function dg_network_getInnerRadius(d) {
    return 9 + (Math.sqrt(d.size) * 2);
}

function dg_network_onHaloEnter(haloEnter) {
    var haloEnter = haloEnter.append("g")
        .attr("class", function(d) { 
            var classes = [
                "node",
                d.key,
                d.key.split('-')[0],
                ];
            return classes.join(" ");
        })
    haloEnter.append("circle")
        .attr("class", "halo")
        .attr("r", function(d) { return dg_network_getOuterRadius(d) + 40; });
}

function dg_network_onHaloExit(haloExit) {
    haloExit.remove();
}

function dg_network_onHullEnter(hullEnter) {
    var hullEnter = hullEnter.append("g")
        .attr("class", function(d) { return "hull hull-" + d.key });
    hullEnter.append("path");
}

function dg_network_onHullExit(hullExit) {
    hullExit.remove();
}

function dg_network_onLinkEnter(linkEnter) {
    var linkEnter = linkEnter.append("g")
        .attr("class", function(d) { 
            var parts = d.key.split('-');
            var role = parts.slice(2, 2 + parts.length - 4).join('-')
            var classes = [
                "link",
                "link-" + d.key,
                role,
                ];
            return classes.join(" ");
        });
    dg_network_onLinkEnterElementConstruction(linkEnter);
    dg_network_onLinkEnterEventBindings(linkEnter);
}

function dg_network_onLinkEnterElementConstruction(linkEnter) {
    var aggregateRoleNames = [
        "Member Of", "Sublable Of",
        "Released On", "Compiled On",
        ]
    linkEnter.append("path")
        .attr("class", "inner")
    linkEnter.append("path")
        .attr("class", "outer")
        .append("title").text(function(d) {
            var source = d.source.name,
                role = d.role,
                target = d.target.name;
            if (role == "Alias") {
                return source + " ↔ (" + role + ") ↔ " + target;
            } else {
                return source + " → (" + role + ") → " + target;
            }
        });
    linkEnter.append("text")
        .attr('class', 'outer')
        .text(function(d) {
            if (['Alias', 'Member Of', 'Sublabel Of'].indexOf(d.role) != -1) {
                return null;
            } else {
                return d.role.split(' ').map(function(x) { 
                    return x[0]; 
                }).join('');
            }
        });
    linkEnter.append("text")
        .attr('class', 'inner')
        .text(function(d) {
            if (['Alias', 'Member Of', 'Sublabel Of'].indexOf(d.role) != -1) {
                return null;
            } else {
                return d.role.split(' ').map(function(x) { 
                    return x[0]; 
                }).join('');
            }
        });
}

function dg_network_onLinkEnterEventBindings(linkEnter) {
    linkEnter.on("mouseover", function(d) {
        d3.select(this).select(".inner")
            .transition()
            .style("stroke-width", 3);
        });
    linkEnter.on("mouseout", function(d) {
        d3.select(this).select(".inner")
            .transition()
            .duration(500)
            .style("stroke-width", 1);
    });
}

function dg_network_onLinkExit(linkExit) {
    linkExit.remove();
}

function dg_network_onLinkUpdate(linkSelection) {
    if (dg.debug) {
        linkSelection.select('text').text(function(d) {
            return "[" + d.pages + "]";
        });
    }
}

function dg_network_onNodeEnter(nodeEnter) {
    var nodeEnter = nodeEnter.append("g")
        .attr("class", function(d) { 
            var classes = [
                "node",
                d.key,
                d.key.split('-')[0],
                ];
            return classes.join(" ");
        })
        .style("fill", function(d) {
            if (d.type == 'artist') {
                return dg_color_heatmap(d);
            } else {
                return dg_color_greyscale(d);
            }
        })
        .call(dg.network.forceLayout.drag);
    dg_network_onNodeEnterElementConstruction(nodeEnter);
    dg_network_onNodeEnterEventBindings(nodeEnter);
}

function dg_network_onNodeEnterElementConstruction(nodeEnter) {

    var artistEnter = nodeEnter.select(function(d) {
        return d.type == 'artist' ? this : null;
    });
    artistEnter
        .append("circle")
        .attr("class", "shadow")
        .attr("cx", 5)
        .attr("cy", 5)
        .attr("r", function(d) {
            return 7 + dg_network_getOuterRadius(d)
        });
    artistEnter
        .select(function(d, i) {return 0 < d.size ? this : null; })
        .append("circle")
        .attr("class", "outer")
        .attr("r", dg_network_getOuterRadius);
    artistEnter
        .append("circle")
        .attr("class", "inner")
        .attr("r", dg_network_getInnerRadius);

    var labelEnter = nodeEnter.select(function(d) {
        return d.type == 'label' ? this : null;
    });
    labelEnter
        .append("rect")
        .attr("class", "inner")
        .attr("height", function(d) { return 2 * dg_network_getInnerRadius(d); })
        .attr("width", function(d) { return 2 * dg_network_getInnerRadius(d); })
        .attr("x", function(d) { return -1 * dg_network_getInnerRadius(d); })
        .attr("y", function(d) { return -1 * dg_network_getInnerRadius(d); });
    nodeEnter.append("path")
        .attr("class", "more")
        .attr("d", d3.svg.symbol().type("cross").size(64))
        .style("opacity", function(d) {return 0 < d.missing ? 1 : 0; });
    nodeEnter.append("title")
        .text(function(d) { return d.name; });
}

function dg_network_onNodeEnterEventBindings(nodeEnter) {
    nodeEnter.on("dblclick", function(d) {
        if (!dg.network.isUpdating) { dg_network_navigate(d.key, true); }
    });
    nodeEnter.on("mousedown", function(d) {
        if (!dg.network.isUpdating) {
            dg.network.pageData.nodes.forEach(function(n) { n.fixed = false; });
            d.fixed = true;
            dg_network_selectNode(d.key);
        }
        d3.event.stopPropagation(); // Prevents propagation to #svg element.
    });
    nodeEnter.on("mouseover", function(d) {
        var selection = dg.network.selections.node.select(function(n) {
            return n.key == d.key ? this : null;
        });
        selection.moveToFront();
    });
    nodeEnter.on("touchstart", function(d) {
        var thisTime = $.now();
        var lastTime = d.lastTouchTime;
        d.lastTouchTime = thisTime;
        if (!lastTime || (500 < (thisTime - lastTime))) {
            if (!dg.network.isUpdating) {
                dg.network.pageData.nodes.forEach(function(n) { n.fixed = false; });
                d.fixed = true;
                dg_network_selectNode(d.key);
            }
        } else if ((thisTime - lastTime) < 500) {
            if (!dg.network.isUpdating) { dg_network_navigate(d.key, true); }
        }
        d3.event.stopPropagation(); // Prevents propagation to #svg element.
    });
}

function dg_network_onNodeExit(nodeExit) {
    nodeExit.remove();
}

function dg_network_onNodeUpdate(nodeUpdate) {
    nodeUpdate.transition()
        .duration(1000)
        .style("fill", function(d) {
            if (d.type == 'artist') {
                return dg_color_heatmap(d);
            } else {
                return dg_color_greyscale(d);
            }
        })
    nodeUpdate.selectAll(".more").each(function(d, i) {
        var prevMissing = Boolean(d.hasMissing);
        var prevMissingByPage = Boolean(d.hasMissingByPage);
        var currMissing = Boolean(d.missing); 
        if (!d.missingByPage) {
            var currMissingByPage = false;
        } else {
            var currMissingByPage = Boolean(
                d.missingByPage[dg.network.pageData.currentPage]
                );
        }
        d3.select(this).transition().duration(1000)
            .style('opacity', function(d) {
                return (currMissing || currMissingByPage) ? 1 : 0;
                })
            .attrTween('transform', function(d) {
                var start = prevMissingByPage ? 45 : 0;
                var stop = currMissingByPage ? 45 : 0;
                return d3.interpolateString(
                    "rotate(" + start + ")",
                    "rotate(" + stop + ")"
                    );
                });
        d.hasMissing = currMissing;
        d.hasMissingByPage = currMissingByPage;
    });
}

function dg_network_onTextUpdate(textUpdate) {
    textUpdate.select('.outer').text(dg_network_getNodeText);
    textUpdate.select('.inner').text(dg_network_getNodeText);
}

function dg_network_getNodeText(d) { 
    var name = d.name;
    if (50 < name.length) {
        name = name.slice(0, 50) + "...";
    }
    if (dg.debug) { 
        var pages = '[' + d.pages + ']';
        return pages + ' ' + name;
    }
    return name;
}

function dg_network_onTextEnter(textEnter) {
    var textEnter = textEnter.append("g")
        .attr("class", function(d) { 
            var classes = [
                "node",
                d.key,
                d.key.split('-')[0],
                ];
            return classes.join(" ");
        })
    textEnter.append("text")
        .attr("class", "outer")
        .attr("dx", function(d) { return dg_network_getOuterRadius(d) + 3; })
        .attr("dy", ".35em")
        .text(dg_network_getNodeText);
    textEnter.append("text")
        .attr("class", "inner")
        .attr("dx", function(d) { return dg_network_getOuterRadius(d) + 3; })
        .attr("dy", ".35em")
        .text(dg_network_getNodeText);
}

function dg_network_onTextExit(textExit) {
    textExit.remove();
}

function dg_network_startForceLayout() {
    var keyFunc = function(d) { return d.key }
    var nodes = dg.network.pageData.nodes.filter(function(d) { 
        return (!d.isIntermediate) && 
            (-1 != d.pages.indexOf(dg.network.pageData.currentPage));
    })
    var links = dg.network.pageData.links.filter(function(d) { 
        return (!d.isSpline) &&
            (-1 != d.pages.indexOf(dg.network.pageData.currentPage));
    })
    dg.network.selections.halo = dg.network.selections.halo.data(nodes, keyFunc);
    dg.network.selections.node = dg.network.selections.node.data(nodes, keyFunc);
    dg.network.selections.text = dg.network.selections.text.data(nodes, keyFunc);
    dg.network.selections.link = dg.network.selections.link.data(links, keyFunc);
    var hullNodes = dg.network.pageData.nodes.filter(function(d) {
            return d.cluster !== undefined;
        });
    var hullData = d3.nest().key(function(d) { return d.cluster; })
        .entries(hullNodes)
        .filter(function(d) { return 1 < d.values.length; });
    dg.network.selections.hull = dg.network.selections.hull.data(hullData);
    dg_network_onHaloEnter(dg.network.selections.halo.enter());
    dg_network_onHaloExit(dg.network.selections.halo.exit());
    dg_network_onHullEnter(dg.network.selections.hull.enter());
    dg_network_onHullExit(dg.network.selections.hull.exit());
    dg_network_onNodeEnter(dg.network.selections.node.enter());
    dg_network_onNodeExit(dg.network.selections.node.exit());
    dg_network_onNodeUpdate(dg.network.selections.node);
    dg_network_onTextEnter(dg.network.selections.text.enter());
    dg_network_onTextExit(dg.network.selections.text.exit());
    dg_network_onTextUpdate(dg.network.selections.text);
    dg_network_onLinkEnter(dg.network.selections.link.enter());
    dg_network_onLinkExit(dg.network.selections.link.exit());
    dg_network_onLinkUpdate(dg.network.selections.link);
    dg.network.pageData.nodes.forEach(function(n) { n.fixed = false; });
    dg.network.forceLayout.start();
}

function dg_network_translate(d) {
    return "translate(" + d.x + "," + d.y + ")";
}

function dg_network_splineInner(name, sX, sY, sR, cX, cY) {
    var dX = (sX - cX),
        dY = (sY - cY);
    var angle = Math.atan(dY / dX);
    dX = Math.abs(Math.cos(angle) * sR);
    dY = Math.abs(Math.sin(angle) * sR);
    sX = (sX < cX) ? sX + dX : sX - dX;
    sY = (sY < cY) ? sY + dY : sY - dY;
    return [sX, sY];
}

function dg_network_spline(d) {
    //console.log(d);
    var sX = d.source.x;
    var sY = d.source.y;
    var tX = d.target.x;
    var tY = d.target.y;
    var tR = d.target.radius;
    var sR = d.source.radius;
    if (d.intermediate) {
        var cX = d.intermediate.x;
        var cY = d.intermediate.y;
        sXY = dg_network_splineInner("Source", sX, sY, sR, cX, cY);
        tXY = dg_network_splineInner("Source", tX, tY, tR, cX, cY);
        return (
            "M " + sXY[0] + "," + sXY[1] + " " +
            "S " + cX + "," + cY + " " +
            " " + tXY[0] + "," + tXY[1] + " "
            );
    } else {
        return "M " + [sX, sY] + " L " + [tX, tY];
    }
}

function dg_network_tick_link(d, i) {
    var group = d3.select(this);
    var spline = dg_network_spline(d);
    var x1 = d.source.x;
    var y1 = d.source.y;
    var x2 = d.target.x;
    var y2 = d.target.y;
    group.selectAll('path')
        .attr("d", spline)
        .attr("x1", x1)
        .attr("y1", y1)
        .attr("x2", x2)
        .attr("y2", y2);
    var path = group.select('path').node();
    var point = path.getPointAtLength(path.getTotalLength() / 2);
    var x = point.x, y = point.y;
    var angle = Math.atan2((y2 - y1), (x2 - x1)) * (180 / Math.PI);
    var text = group.selectAll('text')
        .attr('dx', point.x)
        .attr('dy', point.y)
        .attr('transform', 'rotate(' + angle + ' ' + x + ' ' + y + ')');
}

function dg_network_tick(e) {
    var k = e.alpha * 0.5;
    dg.network.pageData.nodes.filter(function(d) {
        return d.key == dg.network.data.json.center.key && !d.fixed;
    }).forEach(function(d) {
        var dims = dg.network.dimensions;
        var dx = ((dims[0] / 2) - d.x) * k;
        var dy = ((dims[1] / 2) - d.y) * k;
        d.x += dx;
        d.y += dy;
    });
    dg.network.selections.link.each(dg_network_tick_link);
    dg.network.selections.halo.attr("transform", dg_network_translate);
    dg.network.selections.node.attr("transform", dg_network_translate);
    dg.network.selections.text.attr("transform", dg_network_translate);
    dg.network.selections.hull.select("path").attr("d", function(d) {
        return "M" + d3.geom.hull(dg_network_getHullVertices(d.values)).join("L") + "Z"; });
}

function dg_network_getHullVertices(nodes) {
    var vertices = [];
    nodes.forEach(function(d) {
        var radius = d.radius;
        vertices.push([d.x + radius, d.y + radius]);
        vertices.push([d.x + radius, d.y - radius]);
        vertices.push([d.x - radius, d.y + radius]);
        vertices.push([d.x - radius, d.y - radius]);
    });
    return vertices;
}

function dg_network_processJson(json) {
    var newNodeMap = d3.map();
    var newLinkMap = d3.map();
    json.nodes.forEach(function(node) {
        node.radius = dg_network_getOuterRadius(node);
        newNodeMap.set(node.key, node);
    });
    json.links.forEach(function(link) {
        var source = link.source,
            target = link.target;
        if (link.role != 'Alias') {
            var role = link.role.toLocaleLowerCase().replace(/\s+/g, "-");
            var intermediateNode = {
                key: link.key,
                isIntermediate: true,
                pages: link.pages,
                size: 0,
                };
            var s2iSplineLink = {
                isSpline: true,
                key: source + "-" + role + "-[" + target + "]",
                pages: link.pages,
                source: source,
                target: link.key,
            };
            var i2tSplineLink = {
                isSpline: true,
                key: "[" + source + "]-" + role + "-" + target,
                pages: link.pages,
                source: link.key,
                target: target,
            };
            link.intermediate = link.key;
            newNodeMap.set(link.key, intermediateNode);
            newLinkMap.set(s2iSplineLink.key, s2iSplineLink);
            newLinkMap.set(i2tSplineLink.key, i2tSplineLink);
        }
        newLinkMap.set(link.key, link);
    });
    var nodeKeysToRemove = [];
    dg.network.data.nodeMap.keys().forEach(function(key) {
        if (!newNodeMap.has(key)) {
            nodeKeysToRemove.push(key);
        };
    });
    nodeKeysToRemove.forEach(function(key) {
        dg.network.data.nodeMap.remove(key);
    });
    var linkKeysToRemove = [];
    dg.network.data.linkMap.keys().forEach(function(key) {
        if (!newLinkMap.has(key)) {
            linkKeysToRemove.push(key);
        };
    });
    linkKeysToRemove.forEach(function(key) {
        dg.network.data.linkMap.remove(key);
    });
    newNodeMap.entries().forEach(function(entry) {
        var key = entry.key;
        var newNode = entry.value;
        if (dg.network.data.nodeMap.has(key)) {
            var oldNode = dg.network.data.nodeMap.get(key);
            oldNode.cluster = newNode.cluster;
            oldNode.distance = newNode.distance;
            oldNode.links = newNode.links;
            oldNode.missing = newNode.missing;
            oldNode.missingByPage = newNode.missingByPage;
            oldNode.pages = newNode.pages;
        } else {
            newNode.x = dg.network.newNodeCoords[0] + (Math.random() * 200) - 100;
            newNode.y = dg.network.newNodeCoords[1] + (Math.random() * 200) - 100;
            dg.network.data.nodeMap.set(key, newNode);
        }
    });
    newLinkMap.entries().forEach(function(entry) {
        var key = entry.key;
        var newLink = entry.value;
        if (dg.network.data.linkMap.has(key)) {
            var oldLink = dg.network.data.linkMap.get(key);
            oldLink.pages = newLink.pages; 
        } else {
            newLink.source = dg.network.data.nodeMap.get(newLink.source);
            newLink.target = dg.network.data.nodeMap.get(newLink.target);
            if (newLink.intermediate !== undefined) {
                newLink.intermediate = dg.network.data.nodeMap.get(newLink.intermediate);
            }
            dg.network.data.linkMap.set(key, newLink);
        }
    });
    var distances = []
    dg.network.data.nodeMap.values().forEach(function(node) {
        if (node.distance !== undefined) {
            distances.push(node.distance);
        }
    })
    dg.network.data.maxDistance = Math.max.apply(Math, distances);
}

function dg_network_init() {
    var root = d3.select("#svg").append("g")
        .attr("id", "networkLayer");
    dg.network.layers.root = root;
    d3.select("#svg").on("mousedown", function() {
        dg.network.pageData.nodes.forEach(function(n) { n.fixed = false; });
        dg_network_selectNode(null);
    });
    dg.network.layers.halo = root.append("g").attr("id", "haloLayer");
    dg.network.layers.link = root.append("g").attr("id", "linkLayer");
    dg.network.layers.node = root.append("g").attr("id", "nodeLayer");
    dg.network.layers.text = root.append("g").attr("id", "textLayer");
    dg.network.selections.halo = dg.network.layers.halo.selectAll(".node");
    dg.network.selections.hull = dg.network.layers.halo.selectAll(".hull");
    dg.network.selections.link = dg.network.layers.link.selectAll(".link");
    dg.network.selections.node = dg.network.layers.node.selectAll(".node");
    dg.network.selections.text = dg.network.layers.text.selectAll(".node");
    dg.network.forceLayout = dg_network_setupForceLayout();
}

function dg_svg_init() {
    d3.selection.prototype.moveToFront = function() {
        return this.each(function(){ this.parentNode.appendChild(this); });
    };
    var w = window,
        d = document,
        e = d.documentElement,
        g = d.getElementsByTagName('body')[0];
    dg.network.dimensions = [
        w.innerWidth || e.clientWidth || g.clientWidth,
        w.innerHeight|| e.clientHeight|| g.clientHeight,
    ];
    dg.network.newNodeCoords = [
        dg.network.dimensions[0] / 2,
        dg.network.dimensions[1] / 2,
    ];
    window.addEventListener("resize", function() {
        dg.network.dimensions = [
            w.innerWidth || e.clientWidth || g.clientWidth,
            w.innerHeight|| e.clientHeight|| g.clientHeight,
        ];
        d3.select("#svg")
            .attr("width", dg.network.dimensions[0])
            .attr("height", dg.network.dimensions[1]);
        dg.network.forceLayout.size(dg.network.dimensions).start();
    });
    d3.select("#svg")
        .attr("width", dg.network.dimensions[0])
        .attr("height", dg.network.dimensions[1]);
    dg_svg_setupDefs();
}

function dg_svg_setupDefs() {
    var defs = d3.select("#svg").append("defs");
    // ARROWHEAD
    defs.append("marker")
        .attr("id", "arrowhead")
        .attr("viewBox", "-5 -5 10 10")
        .attr("refX", 4)
        .attr("refY", 0)
        .attr("markerWidth", 8)
        .attr("markerHeight", 8)
        .attr("markerUnits", "strokeWidth")
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M 0,0 m -5,-5 L 5,0 L -5,5 L -2.5,0 L -5,-5 Z")
        .attr("stroke-linecap", "round")
        .attr("stroke-linejoin", "round");
    // AGGREGATE
    defs.append("marker")
        .attr("id", "aggregate")
        .attr("viewBox", "-5 -5 10 10")
        .attr("refX", 5)
        .attr("refY", 0)
        .attr("markerWidth", 8)
        .attr("markerHeight", 8)
        .attr("markerUnits", "strokeWidth")
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M 0,0 m 5,0 L 0,-3 L -5,0 L 0,3 L 5,0 Z")
        .attr("fill", "#fff")
        .attr("stroke", "#000")
        .attr("stroke-linecap", "round")
        .attr("stroke-linejoin", "round")
        .attr("stroke-width", 1.5);
    // GAUSSIAN BLUR
    var filter = defs.append("filter")
        .attr("id", "drop-shadow")
        .attr("y", "-50%")
        .attr("x", "-50%")
        .attr("height", "300%")
        .attr("width", "300%");
    filter.append("feGaussianBlur")
        .attr("in", "SourceAlpha")
        .attr("stdDeviation", 3)
        .attr("result", "blur");
    filter.append("feOffset")
        .attr("in", "blur")
        .attr("dx", 4)
        .attr("dy", 4)
        .attr("result", "offsetBlur");
    var feComponentTransfer = filter.append("feComponentTransfer")
        .attr("in", "offsetBlur")
        .attr("result", "lightenedBlur");
    feComponentTransfer.append("feFuncA")
        .attr("type", "linear")
        .attr("slope", 0.25)
        .attr("intercept", 0);
    var feMerge = filter.append("feMerge");
    feMerge.append("feMergeNode")
        .attr("in", "lightenedBlur")
    feMerge.append("feMergeNode")
        .attr("in", "SourceGraphic");
    // RADIAL GRADIENT
    var gradient = defs.append('radialGradient')
        .attr('id', 'radial-gradient');
    gradient.append('stop')
        .attr('offset', '0%')
        .attr('stop-color', '#333')
        .attr('stop-opacity', '100%');
    gradient.append('stop')
        .attr('offset', '50%')
        .attr('stop-color', '#333')
        .attr('stop-opacity', '33%');
    gradient.append('stop')
        .attr('offset', '75%')
        .attr('stop-color', '#333')
        .attr('stop-opacity', '11%');
    gradient.append('stop')
        .attr('offset', '100%')
        .attr('stop-color', '#333')
        .attr('stop-opacity', '0%');
}

$(document).ready(function() {
    dg_svg_init();
    dg_network_init();
    dg_timeline_init();
    dg_typeahead_init();
    if (dgData) {
        var params = {'roles': $('#filter select').val()};
        dg_history_replaceState(dgData.center.key, params);
        dg_network_handleAsyncData(dgData, false);
    }
    $('[data-toggle="tooltip"]').tooltip();
    (function() {
        var click = $.debounce(300, function() {
            var url = '/api/random?' + Math.floor(Math.random() * 1000000);
            if (!dg.network.isUpdating) {
                dg.network.layers.root.transition()
                    .style("opacity", 0.333);
                $("#page-loading")
                    .removeClass("glyphicon-random")
                    .addClass("glyphicon-animate glyphicon-refresh");
                d3.json(url, function(error, json) {
                    if (error) { dg_network_handleAsyncError(error); return; }
                    dg_network_navigate(json.center, true);
                });
            } else {
                dg_warn();                 
            }
        });
        $('#brand').on("click touchstart", function(event) {
            click();
            $(this).tooltip('hide');
            event.preventDefault();
        });
    }());
    $('#paging .previous a').click(function(event) {
        dg_network_prevPage();
        $(this).tooltip('hide');
        event.preventDefault();
    });
    $('#paging .next a').click(function(event) {
        dg_network_nextPage();
        $(this).tooltip('hide');
        event.preventDefault();
    });
    $('#filter-roles').multiselect({
        buttonWidth: "160px",
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        //includeSelectAllOption: true,
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
        dg_network_navigate(dg.network.data.json.center.key, true);
        event.preventDefault();
    });
    $('#filter').fadeIn(3000);
    window.addEventListener("popstate", dg_history_onPopState);
    console.log('discograph initialized.');
});

dg.selectPage = function(page) {
    dg_network_selectPage(page);
    dg_network_startForceLayout();
}

return dg;

}(dg || {}));

function loadMorris() {
    var url = '/api/artist/timeline/32550';
    d3.json(url, function(error, json) {
        if (error) { console.warn(error); return; }
        dg.timeline.json = json;
        dg.timeline.nested = d3.nest()
            .key(function(d) { return d.year; })
            .key(function(d) { return d.category; })
            .entries(json.results);
        var years = dg.timeline.nested.map(function(d) { return parseInt(d.key); })
        var extent = d3.extent(years);
        console.log(extent);
        var scale = d3.scale.linear().domain(extent).range([100, dg.network.dimensions[0] - 100]);
        var axis = d3.svg.axis()
            .orient("bottom")
            .scale(scale)
            .ticks(years.length)
            .tickFormat(d3.format('0000'));
        dg.timeline.layers.root.append("g")
            .attr("class", "x axis")
            .attr("transform", 'translate(0, 100)')
            .call(axis)
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(45)")
            .style("text-anchor", "start");
        console.log(json);
    });
}