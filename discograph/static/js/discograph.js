var dg = (function(dg){

dg.network = {
    centerNodeKey: null,
    dimensions: [0, 0],
    isUpdating: false,
    json: null,
    linkMap: d3.map(),
    links: [],
    newNodeCoords: [0, 0],
    nodeMap: d3.map(),
    nodes: [],
    selectedNodeKey: null,
    maxDistance: 0,
    // selections
    haloSelection: null,
    hullSelection: null,
    nodeSelection: null,
    linkSelection: null,
    textSelection: null,
    // layers
    networkLayer: null,
    haloLayer: null,
    textLayer: null,
    nodeLayer: null,
    linkLayer: null,
};

function dg_network_setupForceLayout() {
    return d3.layout.force()
        .nodes(dg.network.nodes)
        .links(dg.network.links)
        .size(dg.network.dimensions)
        .on("tick", dg_network_tick)
        .linkStrength(1.5)
        .friction(0.9)
        .linkDistance(function(d, i) {
            if (d.isSpline) {
                return 50;
            } else if (d.role != 'Alias') {
                return 100;
            } else {
                return 150;
            }
        })
        .charge(-300)
        .chargeDistance(1000)
        .gravity(0.2)
        .theta(0.1)
        .alpha(0.1);
}

function dg_color_greyscale(d) {
    var hue = 0;
    var saturation = 0;
    var lightness = (d.distance / (dg.network.maxDistance + 1));
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
    if (params) { url += "?" + $.param(params); }
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
    if (params) { url += "?" + $.param(params); }
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
            source: dg_typeahead_bloodhound,
            limit: 20,
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
    //window.history.back();
}

function dg_network_handleAsyncData(json, pushHistory, params) {
    var key = json.center;
    if (pushHistory === true) {
        dg_history_pushState(key, params);
    }
    var name = json.nodes.filter(function(d) { return d.key == key; })
    if (name.length) {
        document.title = "Disco/graph: " + name[0].name;
    }
    $(document).attr("body").id = key;
    dg.network.json = json;
    dg_network_updateForceLayout();
    dg_network_startForceLayout();
    setTimeout(function() { dg.network.isUpdating = false; }, 2000);
    $("#page-loading")
        .removeClass("glyphicon-animate glyphicon-refresh")
        .addClass("glyphicon-random");
}

function dg_network_navigate(key, pushHistory) {
    var entityType = key.split("-")[0];
    var entityId = key.split("-")[1];
    dg.network.isUpdating = true;
    var foundNode = dg.network.nodeSelection
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
    dg.network.networkLayer.transition()
        .duration(250)
        .style("opacity", 0.333);
    $("#page-loading")
        .removeClass("glyphicon-random")
        .addClass("glyphicon-animate glyphicon-refresh")
        ;
    var url = "/api/" + entityType + "/network/" + entityId;
    $.ajax({
        cache: true,
        dataType: 'json',
        error: dg_network_handleAsyncError,
        success: function(data) {
            dg_network_handleAsyncData(data, pushHistory);
            },
        url: url,
    });
}

function dg_network_selectNode(key) {
    dg.network.selectedNodeKey = key;
    if (key !== null) {
        var haloOff = dg.network.haloSelection.filter("*:not(.node-" + key + ")");
        var nodeOff = dg.network.nodeSelection.filter("*:not(.node-" + key + ")");
        var textOff = dg.network.textSelection.filter("*:not(.node-" + key + ")");
        var nodeOn = dg.network.nodeSelection.filter(".node-" + key);
        var linkKeys = nodeOn.data()[0].links;
        var linkOff = dg.network.linkSelection.filter(function(d) {
            return linkKeys.indexOf(d.key) == -1;
        });
    } else {
        var haloOff = dg.network.haloSelection;
        var nodeOff = dg.network.nodeSelection;
        var linkOff = dg.network.linkSelection;
        var textOff = dg.network.textSelection;
    }
    haloOff.select(".halo").style("fill-opacity", 0.);
    linkOff.style("opacity", 0.25);
    nodeOff.select(".more").style("fill", "#fff");
    nodeOff.style("stroke", "#fff");
    textOff.select(".icon").remove();
    if (key === null) {
        $('#entity-link').hide(0);
        return;
    }
    var node = dg.network.nodeMap.get(key);
    var url = 'http://discogs.com/' + node.type + '/' + node.id;
    $('#entity-name').text(node.name);
    $('#entity-link')
        .attr('href', url)
        .removeClass('hidden')
        .show(0);
    var haloOn = dg.network.haloSelection.filter(".node-" + key);
    var linkOn = dg.network.linkSelection.filter(function(d) {
        return 0 <= linkKeys.indexOf(d.key);
    });
    var textOn = dg.network.textSelection.filter(".node-" + key);
    haloOn.select(".halo").style("fill-opacity", 0.1);
    linkOn.style("opacity", 1);
    nodeOn.moveToFront();
    nodeOn.select(".more").style("fill", "#000");
    nodeOn.style("stroke", "#000")
    textOn.moveToFront();
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
        .attr("class", function(d) { return "node node-" + d.key; })
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
        .attr("class", function(d) { return "link link-" + d.key; });
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
        .attr("marker-end", function(d) {
            if (d.role == "Alias") {
                return "none";
            } else if (aggregateRoleNames.indexOf(d.role) != -1) {
                return "url(#aggregate)";
            } else {
                return "url(#arrowhead)";
            }
        })
        .style("stroke-dasharray", function(d) {
            if (d.role == "Alias") {
                return "2, 4";
            } else {
                return "0, 0";
            }
        });
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

function dg_network_onNodeEnter(nodeEnter) {
    var nodeEnter = nodeEnter.append("g")
        //.filter(function(d, i) { return !d.isIntermediate ? this : null })
        .attr("class", function(d) { return "node node-" + d.key; })
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
        .style("stroke-width", 0)
        .style("fill-opacity", 1)
        .style("fill", "#fff")
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
            dg.network.nodes.forEach(function(n) { n.fixed = false; });
            d.fixed = true;
            dg_network_selectNode(d.key);
        }
        d3.event.stopPropagation(); // What is this for?
    });
    nodeEnter.on("mouseover", function(d) {
        var selection = dg.network.nodeSelection.select(function(n) {
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
                dg.network.nodes.forEach(function(n) { n.fixed = false; });
                d.fixed = true;
                dg_network_selectNode(d.key);
            }
        } else if ((thisTime - lastTime) < 500) {
            if (!dg.network.isUpdating) { dg_network_navigate(d.key, true); }
        }
        d3.event.stopPropagation(); // What is this for?
    });
}

function dg_network_onNodeExit(nodeExit) {
    nodeExit.remove();
}

function dg_network_onNodeUpdate(nodeSelection) {
    nodeSelection.transition()
        .duration(1000)
        .style("fill", function(d) {
            if (d.type == 'artist') {
                return dg_color_heatmap(d);
            } else {
                return dg_color_greyscale(d);
            }
        })
    nodeSelection.selectAll(".more")
        .transition()
        .duration(1000)
        .style("opacity", function(d) {return 0 < d.missing ? 1 : 0; });
}

function dg_network_onTextUpdate(textSelection) {
    textSelection.select('.outer').text(dg_network_getNodeText);
    textSelection.select('.inner').text(dg_network_getNodeText);
}

function dg_network_getNodeText(d) { 
    var pages = '[' + d.pages.join(',') + ']';
    var name = d.name;
    if (50 < name.length) {
        name = name.slice(0, 50) + "...";
    }
    return pages + ' ' + name;
    //return name;
}

function dg_network_onTextEnter(textEnter) {
    var textEnter = textEnter.append("g")
        .filter(function(d, i) { return !d.isIntermediate ? this : null })
        .attr("class", function(d) { return "node node-" + d.key; })
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
    dg.network.forceLayout.start();
    dg.network.nodes.forEach(function(n) { n.fixed = false; });
    var keyFunc = function(d) { return d.key }
    var nodes = dg.network.nodes.filter(function(d) { return !d.isIntermediate; })
    var links = dg.network.links.filter(function(d) { return !d.isSpline; })
    dg.network.haloSelection = dg.network.haloSelection.data(nodes, keyFunc);
    dg.network.nodeSelection = dg.network.nodeSelection.data(nodes, keyFunc);
    dg.network.textSelection = dg.network.textSelection.data(nodes, keyFunc);
    dg.network.linkSelection = dg.network.linkSelection.data(links, keyFunc);
    var hullNodes = dg.network.nodeMap.values().filter(function(d) {
            return d.cluster !== undefined;
        });
    var hullData = d3.nest().key(function(d) { return d.cluster; })
        .entries(hullNodes)
        .filter(function(d) { return 1 < d.values.length; });
    dg.network.hullSelection = dg.network.hullSelection.data(hullData);
    dg_network_onHaloEnter(dg.network.haloSelection.enter());
    dg_network_onHaloExit(dg.network.haloSelection.exit());
    dg_network_onHullEnter(dg.network.hullSelection.enter());
    dg_network_onHullExit(dg.network.hullSelection.exit());
    dg_network_onNodeEnter(dg.network.nodeSelection.enter());
    dg_network_onNodeExit(dg.network.nodeSelection.exit());
    dg_network_onNodeUpdate(dg.network.nodeSelection);
    dg_network_onTextEnter(dg.network.textSelection.enter());
    dg_network_onTextExit(dg.network.textSelection.exit());
    dg_network_onTextUpdate(dg.network.textSelection);
    dg_network_onLinkEnter(dg.network.linkSelection.enter());
    dg_network_onLinkExit(dg.network.linkSelection.exit());
    dg.network.networkLayer.transition()
        .duration(1000)
        .style("opacity", 1);
    dg_network_selectNode(dg.network.centerNodeKey);
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

function dg_network_tick(e) {
    var k = e.alpha * 0.5;
    dg.network.nodes.filter(function(d) {
        return d.key == dg.network.centerNodeKey && !d.fixed;
    }).forEach(function(d) {
        var dims = dg.network.dimensions;
        var dx = ((dims[0] / 2) - d.x) * k;
        var dy = ((dims[1] / 2) - d.y) * k;
        d.x += dx;
        d.y += dy;
    });
    dg.network.linkSelection.select(".inner")
        .attr("d", dg_network_spline)
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    dg.network.linkSelection.select(".outer")
        .attr("d", dg_network_spline)
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    dg.network.haloSelection.attr("transform", dg_network_translate);
    dg.network.nodeSelection.attr("transform", dg_network_translate);
    dg.network.textSelection.attr("transform", dg_network_translate);
    dg.network.hullSelection.select("path").attr("d", function(d) {
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

function dg_network_updateForceLayout() {
    var json = dg.network.json;

    var newNodeMap = d3.map();
    json.nodes.forEach(function(node) {
        node.radius = dg_network_getOuterRadius(node);
        newNodeMap.set(node.key, node);
    });

    var newLinkMap = d3.map();
    json.links.forEach(function(link) {
        var source = link.source,
            target = link.target;
        if (link.role != 'Alias') {
            var role = link.role.toLocaleLowerCase().replace(/\s+/g, "-");
            var intermediate = {
                key: link.key,
                isIntermediate: true,
                size: 0,
                };
            var s2iLink = {
                isSpline: true,
                key: source + "-" + role + "-[" + target + "]",
                source: source,
                target: link.key,
            };
            var i2tLink = {
                isSpline: true,
                key: "[" + source + "]-" + role + "-" + target,
                source: link.key,
                target: target,
            };
            link.intermediate = link.key;
            newNodeMap.set(link.key, intermediate);
            newLinkMap.set(s2iLink.key, s2iLink);
            newLinkMap.set(i2tLink.key, i2tLink);
        }
        newLinkMap.set(link.key, link);
    });

    // NODES
    var nodeKeysToRemove = [];
    dg.network.nodeMap.keys().forEach(function(key) {
        if (!newNodeMap.has(key)) {
            nodeKeysToRemove.push(key);
        };
    });
    nodeKeysToRemove.forEach(function(key) {
        dg.network.nodeMap.remove(key);
    });

    // LINKS
    var linkKeysToRemove = [];
    dg.network.linkMap.keys().forEach(function(key) {
        if (!newLinkMap.has(key)) {
            linkKeysToRemove.push(key);
        };
    });
    linkKeysToRemove.forEach(function(key) {
        dg.network.linkMap.remove(key);
    });

    // UPDATE NODE PROPERTIES
    newNodeMap.entries().forEach(function(entry) {
        var key = entry.key;
        var value = entry.value;
        if (dg.network.nodeMap.has(key)) {
            if (!value.isIntermediate) {
                var node = dg.network.nodeMap.get(key);
                node.cluster = value.cluster;
                node.distance = value.distance;
                node.missing = value.missing;
                node.pages = value.pages;
            }
        } else {
            value.x = dg.network.newNodeCoords[0] + (Math.random() * 200) - 100;
            value.y = dg.network.newNodeCoords[1] + (Math.random() * 200) - 100;
            dg.network.nodeMap.set(key, value);
        }
    });

    // UPDATE LINK REFERENCES
    newLinkMap.entries().forEach(function(entry) {
        if (!dg.network.linkMap.has(entry.key)) {
            entry.value.source = dg.network.nodeMap.get(entry.value.source);
            entry.value.target = dg.network.nodeMap.get(entry.value.target);
            if (entry.value.intermediate !== undefined) {
                entry.value.intermediate = dg.network.nodeMap.get(entry.value.intermediate);
            }
            dg.network.linkMap.set(entry.key, entry.value);
        }
    });

    // CALCULATE MAXIMUM DISTANCE
    var distances = []
    dg.network.nodeMap.values().forEach(function(node) {
        if (node.distance !== undefined) {
            distances.push(node.distance);
        }
    })
    dg.network.maxDistance = Math.max.apply(Math, distances);

    // CALCULATE NEIGHBORHOODS
    var linkNeighborhoodMap = d3.map()
    dg.network.linkMap.values().forEach(function(link) {
        if (link.isSpline) { return; }
        if (!linkNeighborhoodMap.has(link.source.key)) {
            linkNeighborhoodMap.set(link.source.key, []);
        }
        linkNeighborhoodMap.get(link.source.key).push(link.key);
        if (!linkNeighborhoodMap.has(link.target.key)) {
            linkNeighborhoodMap.set(link.target.key, []);
        }
        linkNeighborhoodMap.get(link.target.key).push(link.key);
    });
    linkNeighborhoodMap.entries().forEach(function(entry) {
        dg.network.nodeMap.get(entry.key).links = entry.value;
    });

    // PUSH DATA
    dg.network.nodes.length = 0;
    Array.prototype.push.apply(dg.network.nodes, dg.network.nodeMap.values());
    dg.network.links.length = 0;
    Array.prototype.push.apply(dg.network.links, dg.network.linkMap.values());
    dg.network.centerNodeKey = json.center;
}

function dg_network_init() {
    var networkLayer = d3.select("#svg").append("g")
        .attr("id", "networkLayer");
    dg.network.networkLayer = networkLayer;
    d3.select("#svg").on("mousedown", function() {
        dg.network.nodes.forEach(function(n) { n.fixed = false; });
        dg_network_selectNode(null);
    });
    dg.network.haloLayer = networkLayer.append("g").attr("id", "haloLayer");
    dg.network.linkLayer = networkLayer.append("g").attr("id", "linkLayer");
    dg.network.nodeLayer = networkLayer.append("g").attr("id", "nodeLayer");
    dg.network.textLayer = networkLayer.append("g").attr("id", "textLayer");
    dg.network.haloSelection = dg.network.haloLayer.selectAll(".node");
    dg.network.hullSelection = dg.network.haloLayer.selectAll(".hull");
    dg.network.linkSelection = dg.network.linkLayer.selectAll(".link");
    dg.network.nodeSelection = dg.network.nodeLayer.selectAll(".node");
    dg.network.textSelection = dg.network.textLayer.selectAll(".node");
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
    dg_typeahead_init();
    if (dgData) {
        dg_history_replaceState(dgData.center);
        dg_network_handleAsyncData(dgData, false);
    }
    $('[data-toggle="tooltip"]').tooltip();
    (function() {
        var click = $.debounce(300, function() {
            var url = '/api/random?' + Math.floor(Math.random() * 1000000);
            d3.json(url, function(error, json) {
                if (error) { console.warn(error); return; }
                if (!dg.network.isUpdating) {
                    dg_network_navigate(json.center, true);
                }
            });
        });
        $('#brand').on("click touchstart", function(event) {
            click();
            $(this).tooltip('hide');
            event.preventDefault();
        });
    }());
    window.addEventListener("popstate", dg_history_onPopState);
    console.log('discograph initialized.');
});

return dg;

}(dg || {}));