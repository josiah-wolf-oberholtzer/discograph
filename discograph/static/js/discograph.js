var dg = (function(dg){

function dg_graph_setupDefs(svgSelection) {
    var defs = svgSelection.append("defs");
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

function dg_graph_setupForceLayout() {
    return d3.layout.force()
        .nodes(dg.graph.nodes)
        .links(dg.graph.links)
        .size(dg.graph.dimensions)
        .on("tick", dg.tick)
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

dg.graph = {
    cache: d3.map(),
    cacheHistory: [],
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
    svgSelection: null,
    haloSelection: null,
    hullSelection: null,
    nodeSelection: null,
    linkSelection: null,
    textSelection: null,
    // layers
    haloLayer: null,
    textLayer: null,
    nodeLayer: null,
    linkLayer: null,
};

function dg_color_greyscale(d) {
    var hue = 0;
    var saturation = 0;
    var lightness = (d.distance / (dg.graph.maxDistance + 1));
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
    dg_graph_update(event.state.key);
}

function dg_history_pushState(entityKey, params) {
    var entityType = entityKey.split("-")[0];
    var entityId = entityKey.split("-")[1];
    var title = document.title;
    var url = "/" + entityType + "/" + entityId;
    if (params) { url += "?" + $.params(params); }
    var state = {key: entityKey, params: params};
    window.history.pushState(state, title, url);
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
        dg_graph_navigate(datum);
        $("#typeahead").typeahead("close");
        $("#typeahead").blur();
        $('.navbar-toggle').click();
    };
}

dg_graph_handleAsyncError = function(error) {
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
    window.history.back();
}

dg_graph_handleAsyncData = function(json) {
    var key = json.center;
    if (!dg.graph.cache.has(key)) {
        dg.graph.cache.set(key, JSON.parse(JSON.stringify(json)));
        dg.graph.cacheHistory.push(key);
        if (50 <= dg.graph.cache.size()) {
            dg.graph.cache.remove(dg.graph.cacheHistory.shift());
        }
    }
    var name = json.nodes.filter(function(d) { return d.key == key; })
    if (name.length) {
        document.title = "Disco/graph: " + name[0].name;
    }
    $(document).attr("body").id = key;
    dg.graph.json = json;
    dg_graph_updateForceLayout();
    dg_graph_startForceLayout();
    setTimeout(function() { dg.graph.isUpdating = false; }, 2000);
    $("#page-loading")
        .removeClass("glyphicon-animate glyphicon-refresh")
        .addClass("glyphicon-random");
}

function dg_graph_navigate(key) {
    dg_history_pushState(key);
    dg_graph_update(key);
}

function dg_graph_selectNode(key) {
    dg.graph.selectedNodeKey = key;
    if (key !== null) {
        var haloOff = dg.graph.haloSelection.filter("*:not(.node-" + key + ")");
        var nodeOff = dg.graph.nodeSelection.filter("*:not(.node-" + key + ")");
        var textOff = dg.graph.textSelection.filter("*:not(.node-" + key + ")");
        var nodeOn = dg.graph.nodeSelection.filter(".node-" + key);
        var linkKeys = nodeOn.data()[0].links;
        var linkOff = dg.graph.linkSelection.filter(function(d) {
            return linkKeys.indexOf(d.key) == -1;
        });
    } else {
        var haloOff = dg.graph.haloSelection;
        var nodeOff = dg.graph.nodeSelection;
        var linkOff = dg.graph.linkSelection;
        var textOff = dg.graph.textSelection;
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
    var node = dg.graph.nodeMap.get(key);
    var url = 'http://discogs.com/' + node.type + '/' + node.id;
    $('#entity-name').text(node.name);
    $('#entity-link')
        .attr('href', url)
        .removeClass('hidden')
        .show(0);
    var haloOn = dg.graph.haloSelection.filter(".node-" + key);
    var linkOn = dg.graph.linkSelection.filter(function(d) {
        return 0 <= linkKeys.indexOf(d.key);
    });
    var textOn = dg.graph.textSelection.filter(".node-" + key);
    haloOn.select(".halo").style("fill-opacity", 0.1);
    linkOn.style("opacity", 1);
    nodeOn.moveToFront();
    nodeOn.select(".more").style("fill", "#000");
    nodeOn.style("stroke", "#000")
    textOn.moveToFront();
}

function dg_graph_getOuterRadius(d) {
    if (0 < d.size) {
        return 12 + (Math.sqrt(d.size) * 2);
    }
    return 9 + (Math.sqrt(d.size) * 2);
}

function dg_graph_getInnerRadius(d) {
    return 9 + (Math.sqrt(d.size) * 2);
}

function dg_graph_onHaloEnter(haloEnter) {
    var haloEnter = haloEnter.append("g")
        .attr("class", function(d) { return "node node-" + d.key; })
    haloEnter.append("circle")
        .attr("class", "halo")
        .attr("r", function(d) { return dg_graph_getOuterRadius(d) + 40; });
}

function dg_graph_onHaloExit(haloExit) { haloExit.remove(); }

function dg_graph_onHullEnter(hullEnter) {
    var hullEnter = hullEnter.append("g")
        .attr("class", function(d) { return "hull hull-" + d.key });
    hullEnter.append("path");
}

function dg_graph_onHullExit(hullExit) { hullExit.remove(); }

function dg_graph_onLinkEnter(linkEnter) {
    var linkEnter = linkEnter.append("g")
        .attr("class", function(d) { return "link link-" + d.key; });
    dg_graph_onLinkEnterElementConstruction(linkEnter);
    dg_graph_onLinkEnterEventBindings(linkEnter);
}

function dg_graph_onLinkEnterElementConstruction(linkEnter) {
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

function dg_graph_onLinkEnterEventBindings(linkEnter) {
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

function dg_graph_onLinkExit(linkExit) { linkExit.remove(); }

function dg_graph_onNodeEnter(nodeEnter) {
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
        .call(dg.graph.forceLayout.drag);
    dg_graph_onNodeEnterElementConstruction(nodeEnter);
    dg_graph_onNodeEnterEventBindings(nodeEnter);
}

function dg_graph_onNodeEnterElementConstruction(nodeEnter) {

    var artistEnter = nodeEnter.select(function(d) {
        return d.type == 'artist' ? this : null;
    });
    artistEnter
        .append("circle")
        .attr("class", "shadow")
        .attr("cx", 5)
        .attr("cy", 5)
        .attr("r", function(d) {
            return 7 + dg_graph_getOuterRadius(d)
        });
    artistEnter
        .select(function(d, i) {return 0 < d.size ? this : null; })
        .append("circle")
        .attr("class", "outer")
        .attr("r", dg_graph_getOuterRadius);
    artistEnter
        .append("circle")
        .attr("class", "inner")
        .attr("r", dg_graph_getInnerRadius);

    var labelEnter = nodeEnter.select(function(d) {
        return d.type == 'label' ? this : null;
    });
    labelEnter
        .append("rect")
        .attr("class", "inner")
        .attr("height", function(d) { return 2 * dg_graph_getInnerRadius(d); })
        .attr("width", function(d) { return 2 * dg_graph_getInnerRadius(d); })
        .attr("x", function(d) { return -1 * dg_graph_getInnerRadius(d); })
        .attr("y", function(d) { return -1 * dg_graph_getInnerRadius(d); });
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

function dg_graph_onNodeEnterEventBindings(nodeEnter) {
    nodeEnter.on("dblclick", function(d) {
        if (!dg.graph.isUpdating) { dg_graph_navigate(d.key); }
    });
    nodeEnter.on("mousedown", function(d) {
        if (!dg.graph.isUpdating) {
            dg.graph.nodes.forEach(function(n) { n.fixed = false; });
            d.fixed = true;
            dg_graph_selectNode(d.key);
        }
        d3.event.stopPropagation(); // What is this for?
    });
    nodeEnter.on("mouseover", function(d) {
        var selection = dg.graph.nodeSelection.select(function(n) {
            return n.key == d.key ? this : null;
        });
        selection.moveToFront();
    });
    nodeEnter.on("touchstart", function(d) {
        var thisTime = $.now();
        var lastTime = d.lastTouchTime;
        d.lastTouchTime = thisTime;
        if (!lastTime || (500 < (thisTime - lastTime))) {
            if (!dg.graph.isUpdating) {
                dg.graph.nodes.forEach(function(n) { n.fixed = false; });
                d.fixed = true;
                dg_graph_selectNode(d.key);
            }
        } else if ((thisTime - lastTime) < 500) {
            if (!dg.graph.isUpdating) { dg_graph_navigate(d.key); }
        }
        d3.event.stopPropagation(); // What is this for?
    });
}

function dg_graph_onNodeExit(nodeExit) { nodeExit.remove(); }

function dg_graph_onNodeUpdate(nodeSelection) {
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

function dg_graph_onTextUpdate(textSelection) { }

function dg_graph_onTextEnter(textEnter) {
    var textEnter = textEnter.append("g")
        .filter(function(d, i) { return !d.isIntermediate ? this : null })
        .attr("class", function(d) { return "node node-" + d.key; })
    textEnter.append("text")
        .attr("class", "outer")
        .attr("dx", function(d) { return dg_graph_getOuterRadius(d) + 3; })
        .attr("dy", ".35em")
        .text(function(d) {
            var name = d.name;
            if (50 < name.length) {
                name = name.slice(0, 50) + "...";
            }
            return name;
        });
    textEnter.append("text")
        .attr("class", "inner")
        .attr("dx", function(d) { return dg_graph_getOuterRadius(d) + 3; })
        .attr("dy", ".35em")
        .text(function(d) {
            var name = d.name;
            if (50 < name.length) {
                name = name.slice(0, 50) + "...";
            }
            return name;
        })
}

function dg_graph_onTextExit(textExit) { textExit.remove(); }

function dg_graph_startForceLayout() {
    dg.graph.forceLayout.start();
    dg.graph.nodes.forEach(function(n) { n.fixed = false; });
    var keyFunc = function(d) { return d.key }
    var nodes = dg.graph.nodes.filter(function(d) { return !d.isIntermediate; })
    var links = dg.graph.links.filter(function(d) { return !d.isSpline; })
    dg.graph.haloSelection = dg.graph.haloSelection.data(nodes, keyFunc);
    dg.graph.nodeSelection = dg.graph.nodeSelection.data(nodes, keyFunc);
    dg.graph.textSelection = dg.graph.textSelection.data(nodes, keyFunc);
    dg.graph.linkSelection = dg.graph.linkSelection.data(links, keyFunc);
    var hullNodes = dg.graph.nodeMap.values().filter(function(d) {
            return d.cluster !== undefined;
        });
    var hullData = d3.nest().key(function(d) { return d.cluster; })
        .entries(hullNodes)
        .filter(function(d) { return 1 < d.values.length; });
    dg.graph.hullSelection = dg.graph.hullSelection.data(hullData);
    dg_graph_onHaloEnter(dg.graph.haloSelection.enter());
    dg_graph_onHaloExit(dg.graph.haloSelection.exit());
    dg_graph_onHullEnter(dg.graph.hullSelection.enter());
    dg_graph_onHullExit(dg.graph.hullSelection.exit());
    dg_graph_onNodeEnter(dg.graph.nodeSelection.enter());
    dg_graph_onNodeExit(dg.graph.nodeSelection.exit());
    dg_graph_onNodeUpdate(dg.graph.nodeSelection);
    dg_graph_onTextEnter(dg.graph.textSelection.enter());
    dg_graph_onTextExit(dg.graph.textSelection.exit());
    dg_graph_onTextUpdate(dg.graph.textSelection);
    dg_graph_onLinkEnter(dg.graph.linkSelection.enter());
    dg_graph_onLinkExit(dg.graph.linkSelection.exit());
    dg.graph.svgSelection.transition()
        .duration(1000)
        .style("opacity", 1);
    dg_graph_selectNode(dg.graph.centerNodeKey);
}

function dg_graph_translate(d) {
    return "translate(" + d.x + "," + d.y + ")";
};

function dg_graph_splineInner(name, sX, sY, sR, cX, cY) {
    var dX = (sX - cX),
        dY = (sY - cY);
    var angle = Math.atan(dY / dX);
    dX = Math.abs(Math.cos(angle) * sR);
    dY = Math.abs(Math.sin(angle) * sR);
    sX = (sX < cX) ? sX + dX : sX - dX;
    sY = (sY < cY) ? sY + dY : sY - dY;
    return [sX, sY];
}

function dg_graph_spline(d) {
    var sX = d.source.x;
    var sY = d.source.y;
    var tX = d.target.x;
    var tY = d.target.y;
    var tR = d.target.radius;
    var sR = d.source.radius;
    if (d.intermediate) {
        var cX = d.intermediate.x;
        var cY = d.intermediate.y;
        sXY = dg_graph_splineInner("Source", sX, sY, sR, cX, cY);
        tXY = dg_graph_splineInner("Source", tX, tY, tR, cX, cY);
        return (
            "M " + sXY[0] + "," + sXY[1] + " " +
            "S " + cX + "," + cY + " " +
            " " + tXY[0] + "," + tXY[1] + " "
            );
    } else {
        return "M " + [sX, sY] + " L " + [tX, tY];
    }
}

dg.tick = function(e) {
    var k = e.alpha * 0.5;
    dg.graph.nodes.filter(function(d) {
        return d.key == dg.graph.centerNodeKey && !d.fixed;
    }).forEach(function(d) {
        var dims = dg.graph.dimensions;
        var dx = ((dims[0] / 2) - d.x) * k;
        var dy = ((dims[1] / 2) - d.y) * k;
        d.x += dx;
        d.y += dy;
    });
    dg.graph.linkSelection.select(".inner")
        .attr("d", dg_graph_spline)
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    dg.graph.linkSelection.select(".outer")
        .attr("d", dg_graph_spline)
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    dg.graph.haloSelection.attr("transform", dg_graph_translate);
    dg.graph.nodeSelection.attr("transform", dg_graph_translate);
    dg.graph.textSelection.attr("transform", dg_graph_translate);
    dg.graph.hullSelection.select("path").attr("d", function(d) {
        return "M" + d3.geom.hull(dg_graph_getHullVertices(d.values)).join("L") + "Z"; });
}

var dg_graph_getHullVertices = function(nodes) {
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

function dg_graph_updateForceLayout() {
    var json = dg.graph.json;

    var newNodeMap = d3.map();
    json.nodes.forEach(function(node) {
        node.radius = dg_graph_getOuterRadius(node);
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
    dg.graph.nodeMap.keys().forEach(function(key) {
        if (!newNodeMap.has(key)) {
            nodeKeysToRemove.push(key);
        };
    });
    nodeKeysToRemove.forEach(function(key) {
        dg.graph.nodeMap.remove(key);
    });

    // LINKS
    var linkKeysToRemove = [];
    dg.graph.linkMap.keys().forEach(function(key) {
        if (!newLinkMap.has(key)) {
            linkKeysToRemove.push(key);
        };
    });
    linkKeysToRemove.forEach(function(key) {
        dg.graph.linkMap.remove(key);
    });

    // UPDATE NODE PROPERTIES
    newNodeMap.entries().forEach(function(entry) {
        var key = entry.key;
        var value = entry.value;
        if (dg.graph.nodeMap.has(key)) {
            if (!value.isIntermediate) {
                var node = dg.graph.nodeMap.get(key);
                node.cluster = value.cluster;
                node.distance = value.distance;
                node.missing = value.missing;
            }
        } else {
            value.x = dg.graph.newNodeCoords[0] + (Math.random() * 200) - 100;
            value.y = dg.graph.newNodeCoords[1] + (Math.random() * 200) - 100;
            dg.graph.nodeMap.set(key, value);
        }
    });

    // UPDATE LINK REFERENCES
    newLinkMap.entries().forEach(function(entry) {
        if (!dg.graph.linkMap.has(entry.key)) {
            entry.value.source = dg.graph.nodeMap.get(entry.value.source);
            entry.value.target = dg.graph.nodeMap.get(entry.value.target);
            if (entry.value.intermediate !== undefined) {
                entry.value.intermediate = dg.graph.nodeMap.get(entry.value.intermediate);
            }
            dg.graph.linkMap.set(entry.key, entry.value);
        }
    });

    // CALCULATE MAXIMUM DISTANCE
    var distances = []
    dg.graph.nodeMap.values().forEach(function(node) {
        if (node.distance !== undefined) {
            distances.push(node.distance);
        }
    })
    dg.graph.maxDistance = Math.max.apply(Math, distances);

    // CALCULATE NEIGHBORHOODS
    var linkNeighborhoodMap = d3.map()
    dg.graph.linkMap.values().forEach(function(link) {
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
        dg.graph.nodeMap.get(entry.key).links = entry.value;
    });

    // PUSH DATA
    dg.graph.nodes.length = 0;
    Array.prototype.push.apply(dg.graph.nodes, dg.graph.nodeMap.values());
    dg.graph.links.length = 0;
    Array.prototype.push.apply(dg.graph.links, dg.graph.linkMap.values());
    dg.graph.centerNodeKey = json.center;
}

function dg_graph_update(key) {
    var entityType = key.split("-")[0];
    var entityId = key.split("-")[1];
    dg.graph.isUpdating = true;
    var foundNode = dg.graph.nodeSelection
        .filter(function(d) { return d.key == key; });
    if (foundNode.length == 1) {
        foundNode.each(function(d) {
            dg.graph.newNodeCoords = [d.x, d.y];
        });
    } else {
        dg.graph.newNodeCoords = [
            dg.graph.dimensions[0] / 2,
            dg.graph.dimensions[1] / 2,
        ];
    }
    dg.graph.svgSelection
        .transition()
        .duration(250)
        .style("opacity", 0.333);
    $("#page-loading")
        .removeClass("glyphicon-random")
        .addClass("glyphicon-animate glyphicon-refresh")
        ;
    if (dg.graph.cache.has(key)) {
        var json = JSON.parse(JSON.stringify(dg.graph.cache.get(key)));
        dg_graph_handleAsyncData(json);
    } else {
        var url = "/api/" + entityType + "/network/" + entityId;
        $.ajax({
            dataType: 'json',
            error: dg_graph_handleAsyncError,
            success: dg_graph_handleAsyncData,
            url: url,
        });
    }
}

function dg_graph_init() {
    d3.selection.prototype.moveToFront = function() {
        return this.each(function(){ this.parentNode.appendChild(this); });
    };
    window.addEventListener("popstate", dg_history_onPopState);
    var w = window,
        d = document,
        e = d.documentElement,
        g = d.getElementsByTagName('body')[0];
    dg.graph.dimensions = [
        w.innerWidth || e.clientWidth || g.clientWidth,
        w.innerHeight|| e.clientHeight|| g.clientHeight,
    ];
    dg.graph.newNodeCoords = [
        dg.graph.dimensions[0] / 2,
        dg.graph.dimensions[1] / 2,
    ];
    window.addEventListener("resize", function() {
        dg.graph.dimensions = [
            w.innerWidth || e.clientWidth || g.clientWidth,
            w.innerHeight|| e.clientHeight|| g.clientHeight,
        ];
        dg.graph.svgSelection
            .attr("width", dg.graph.dimensions[0])
            .attr("height", dg.graph.dimensions[1]);
        dg.graph.forceLayout.size(dg.graph.dimensions).start();
    });
    dg.graph.svgSelection = d3.select("#svg")
        .attr("width", dg.graph.dimensions[0])
        .attr("height", dg.graph.dimensions[1]);
    dg.graph.svgSelection.on("mousedown", function() {
        dg.graph.nodes.forEach(function(n) { n.fixed = false; });
        dg_graph_selectNode(null);
    });
    dg_graph_setupDefs(dg.graph.svgSelection):
    dg.graph.haloLayer = dg.graph.svgSelection.append("g").attr("id", "haloLayer");
    dg.graph.linkLayer = dg.graph.svgSelection.append("g").attr("id", "linkLayer");
    dg.graph.nodeLayer = dg.graph.svgSelection.append("g").attr("id", "nodeLayer");
    dg.graph.textLayer = dg.graph.svgSelection.append("g").attr("id", "textLayer");
    dg.graph.haloSelection = dg.graph.haloLayer.selectAll(".node");
    dg.graph.hullSelection = dg.graph.haloLayer.selectAll(".hull");
    dg.graph.linkSelection = dg.graph.linkLayer.selectAll(".link");
    dg.graph.nodeSelection = dg.graph.nodeLayer.selectAll(".node");
    dg.graph.textSelection = dg.graph.textLayer.selectAll(".node");
    dg.graph.forceLayout = dg_graph_setupForceLayout();
}

function dg_init() {
    dg_graph_init();
    dg_typeahead_init();
    if (dgData) {
        dg_history_pushState(dgData.center);
        dg_graph_handleAsyncData(dgData);
    }
    $('[data-toggle="tooltip"]').tooltip();
    (function() {
        var click = $.debounce(300, function() {
            var url = '/api/random?' + Math.floor(Math.random() * 1000000);
            d3.json(url, function(error, json) {
                if (error) { console.warn(error); return; } 
                if (!dg.graph.isUpdating) { dg_graph_navigate(json.center); }
            });
        });
        $('#brand').on("click touchstart", function(event) {
            click();
            $(this).tooltip('hide');
            event.preventDefault();
        });
    }());
    console.log('discograph initialized.');
}

dg.init = dg_init;

return dg;

}(dg || {}));

$(document).ready(function() {
    dg.init();
});