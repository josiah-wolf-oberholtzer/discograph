var dg = (function(dg){

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
        nodeSelection: null,
        linkSelection: null,
        textSelection: null,
        // layers
        haloLayer: null,
        textLayer: null,
        nodeLayer: null,
        linkLayer: null,
    };

    dg.history = {
        onPopState: function(event) {
            console.log(event, event.state);
            dg.updateGraph(event.state.key);
        },
        pushState: function(entityKey, params) {
            var entityType = entityKey.split("-")[0];
            var entityId = entityKey.split("-")[1];
            var title = document.title;
            var url = "/" + entityType + "/" + entityId;
            if (params) { url += "?" + $.params(params); }
            var state = {key: entityKey, params: params};
            window.history.pushState(state, title, url);
        },
    }

    /* GRAPH METHODS */

    dg.handleNewGraphData = function(error, json) {
        if (error) {
            console.warn("404", error);
            window.history.back();
            return;
        }
        var key = json.center[0];
        if (!dg.graph.cache.has(key)) {
            dg.graph.cache.set(key, JSON.parse(JSON.stringify(json)));
            dg.graph.cacheHistory.push(key);
            if (50 <= dg.graph.cache.size()) {
                dg.graph.cache.remove(dg.graph.cacheHistory.shift());
            }
        }
        var name = json.nodes.filter(function(d) { return d.key == key; })
        if (name.length) {
            document.title = "discoGraph: " + name[0].name;
        }
        $(document).attr("body").id = key;
        dg.graph.json = json;
        dg.updateForceLayout();
        dg.startForceLayout();
        setTimeout(function() {
            dg.graph.isUpdating = false;
        }, 2000);
        $("#brand .loading").addClass("hidden");
    }

    dg.navigateGraph = function(key) {
        dg.history.pushState(key);
        dg.updateGraph(key);
    }

    dg.selectNode = function(key) {
        dg.graph.selectedNodeKey = key;

        if (key !== null) {
            var haloOff = dg.graph.haloSelection.filter("*:not(.node-" + key + ")");
            var nodeOff = dg.graph.nodeSelection.filter("*:not(.node-" + key + ")");
            var nodeOn = dg.graph.nodeSelection.filter(".node-" + key);
            var linkKeys = nodeOn.data()[0].links;
            var linkOff = dg.graph.linkSelection.filter(function(d) { 
                return linkKeys.indexOf(d.key) == -1;
            });
        } else {
            var haloOff = dg.graph.haloSelection;
            var nodeOff = dg.graph.nodeSelection;
            var linkOff = dg.graph.linkSelection;
        }

        haloOff.select(".halo").style("fill-opacity", 0.);
        linkOff.style("opacity", 0.25);
        nodeOff.select(".more").style("fill", "#fff");
        nodeOff.style("stroke", "#fff");

        if (key === null) {
            return;
        }

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

    function getOuterRadius(d) {
        if (0 < d.size) {
            return 12 + (Math.sqrt(d.size) * 2);
        }
        return 9 + (Math.sqrt(d.size) * 2);
    }

    function getInnerRadius(d) {
        return 9 + (Math.sqrt(d.size) * 2);
    }

    function onHaloEnter(haloEnter) {
        var haloEnter = haloEnter.append("g")
            .attr("class", function(d) { return "node node-" + d.key; })
        haloEnter.append("circle")
            .attr("class", "halo")
            .attr("r", function(d) { return getOuterRadius(d) + 40; });
    }

    function onHaloExit(haloExit) {
        haloExit.remove();
    }

    function onLinkEnter(linkEnter) {
        var aggregateRoleNames = [
            "Member Of", "Sublable Of",
            "Released On", "Compiled On",
            ]
        var linkEnter = linkEnter.append("g")
            .attr("class", function(d) { return "link link-" + d.key; });
        linkEnter.append("g:path")
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
        linkEnter.append("g:path")
            .attr("class", "outer")
            //.attr("filter", "url(#blur)")
            .append("title").text(function(d) { 
                var source = d.nodes[0].name,
                    role = d.role,
                    target = d.nodes[2].name;
                if (role == "Alias") {
                    return source + " ↔ (" + role + ") ↔ " + target;
                } else {
                    return source + " → (" + role + ") → " + target;
                }
            });
    }

    function onLinkExit(linkExit) {
        linkExit.remove();
    }

    function onNodeEnter(nodeEnter) {
        var nodeEnter = nodeEnter.append("g")
            //.filter(function(d, i) { return !d.isIntermediate ? this : null })
            .attr("class", function(d) { return "node node-" + d.key; })
            .style("fill", function(d) { 
                if (d.type == 'artist') {
                    return dg.color.heatmap(d); 
                } else {
                    return dg.color.greyscale(d);
                }
            })
            .call(dg.graph.forceLayout.drag);
        nodeEnter.on("mousedown", function(d) {
            if (!dg.graph.isUpdating) {
                dg.graph.nodes.forEach(function(n) { n.fixed = false; });
                d.fixed = true;
                dg.selectNode(d.key);
            }
            d3.event.stopPropagation();
        });
        nodeEnter.on("mouseover", function(d) {
            var selection = dg.graph.nodeSelection.select(function(n) {
                return n.key == d.key ? this : null;
            });
            selection.moveToFront();
        });
        nodeEnter.on("dblclick", function(d) {
            if (!dg.graph.isUpdating) {
                dg.navigateGraph(d.key);
            }
        });
        var artistEnter = nodeEnter.select(function(d) { 
            return d.type == 'artist' ? this : null;
        });
        artistEnter
            .select(function(d, i) {return 0 < d.size ? this : null; })
            .append("circle")
            .attr("class", "outer")
            .attr("r", getOuterRadius);
        artistEnter
            .append("circle")
            .attr("class", "inner")
            .attr("r", getInnerRadius);
        var labelEnter = nodeEnter.select(function(d) { 
            return d.type == 'label' ? this : null;
        });
        labelEnter
            .append("rect")
            .attr("class", "inner")
            .attr("height", function(d) { return 2 * getInnerRadius(d); })
            .attr("width", function(d) { return 2 * getInnerRadius(d); })
            .attr("x", function(d) { return -1 * getInnerRadius(d); })
            .attr("y", function(d) { return -1 * getInnerRadius(d); });
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

    function onNodeExit(nodeExit) {
        nodeExit.remove();
    }

    function onNodeUpdate(nodeSelection) {
        nodeSelection.transition()
            .duration(1000)
            .style("fill", function(d) { 
                if (d.type == 'artist') {
                    return dg.color.heatmap(d); 
                } else {
                    return dg.color.greyscale(d);
                }
            })
        nodeSelection.selectAll(".more")
            .transition()
            .duration(1000)
            .style("opacity", function(d) {return 0 < d.missing ? 1 : 0; });
    }

    function onTextUpdate(textSelection) {
        /*
        textSelection.selectAll('text')
            .transition()
            .duration(1000)
            .style("opacity", 0.1)
        */
    }

    function onTextEnter(textEnter) {
        var textEnter = textEnter.append("g")
            .filter(function(d, i) { return !d.isIntermediate ? this : null })
            .attr("class", function(d) { return "node node-" + d.key; })
        textEnter.append("text")
            .attr("class", "outer")
            .attr("dx", function(d) { return getOuterRadius(d) + 3; })
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
            .attr("dx", function(d) { return getOuterRadius(d) + 3; })
            .attr("dy", ".35em")
            .text(function(d) { 
                var name = d.name;
                if (50 < name.length) {
                    name = name.slice(0, 50) + "...";
                }
                return name;
            })
    }

    function onTextExit(textExit) {
        textExit.remove();
    }

    dg.startForceLayout = function() {
        dg.graph.forceLayout.start();

        dg.graph.nodes.forEach(function(n) { n.fixed = false; });

        var keyFunc = function(d) { return d.key }

        var nodes = dg.graph.nodes.filter(function(d) {
            return !d.isIntermediate;
        })
        var links = dg.graph.links.filter(function(d) {
            return d.isPrimary;
        })

        dg.graph.haloSelection = dg.graph.haloSelection.data(nodes, keyFunc);
        dg.graph.nodeSelection = dg.graph.nodeSelection.data(nodes, keyFunc);
        dg.graph.textSelection = dg.graph.textSelection.data(nodes, keyFunc);
        dg.graph.linkSelection = dg.graph.linkSelection.data(links, keyFunc);

        onHaloEnter(dg.graph.haloSelection.enter());
        onHaloExit(dg.graph.haloSelection.exit());

        onNodeEnter(dg.graph.nodeSelection.enter());
        onNodeExit(dg.graph.nodeSelection.exit());
        onNodeUpdate(dg.graph.nodeSelection);

        onTextEnter(dg.graph.textSelection.enter());
        onTextExit(dg.graph.textSelection.exit());
        onTextUpdate(dg.graph.textSelection);

        onLinkEnter(dg.graph.linkSelection.enter());
        onLinkExit(dg.graph.linkSelection.exit());

        dg.graph.svgSelection.transition()
            .duration(1000)
            .style("opacity", 1);
        dg.selectNode(dg.graph.centerNodeKey);
    }

    function translate(d) { 
        return "translate(" + d.x + "," + d.y + ")"; 
    };

    function splineInner(name, sX, sY, sR, cX, cY) {
        var dX = (sX - cX),
            dY = (sY - cY);
        var angle = Math.atan(dY / dX);
        dX = Math.abs(Math.cos(angle) * sR);
        dY = Math.abs(Math.sin(angle) * sR);
        sX = (sX < cX) ? sX + dX : sX - dX;
        sY = (sY < cY) ? sY + dY : sY - dY;
        return [sX, sY];
    }

    function spline(d) {
        var sR = d.nodes[0].radius;
        var sX = d.nodes[0].x;
        var sY = d.nodes[0].y;
        var tR = d.nodes[2].radius;
        var tX = d.nodes[2].x;
        var tY = d.nodes[2].y;
        var cX = d.nodes[1].x;
        var cY = d.nodes[1].y;
        sXY = splineInner("Source", sX, sY, sR, cX, cY);
        tXY = splineInner("Source", tX, tY, tR, cX, cY);
        return (
            "M " + sXY[0] + "," + sXY[1] + " " +
            "S " + cX + "," + cY + " " +
            " " + tXY[0] + "," + tXY[1] + " "
            );
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
        dg.graph.linkSelection.select(".inner").attr("d", spline);
        dg.graph.linkSelection.select(".outer").attr("d", spline);
        dg.graph.haloSelection.attr("transform", translate);
        dg.graph.nodeSelection.attr("transform", translate);
        dg.graph.textSelection.attr("transform", translate);
    }

    dg.updateForceLayout = function() {
        var json = dg.graph.json;

        var newNodeMap = d3.map();
        json.nodes.forEach(function(node) {
            node.radius = getOuterRadius(node);
            newNodeMap.set(node.key, node);
        });

        var newLinkMap = d3.map();
        json.links.forEach(function(link) {
            var role = link.role.toLocaleLowerCase().replace(/\s+/g, "-");
            var key = link.key;
            var source = link.source,
                target = link.target,
                intermediate = {key: key, isIntermediate: true, size: 0};
            var siLink = {
                isPrimary: true,
                isSpline: true,
                key: "(i)-" + key,
                role: link.role,
                source: source, 
                target: key, 
                nodes: [source, intermediate, target],
            };
            var itLink = {
                isPrimary: false,
                isSpline: true,
                key: key + "-(i)",
                source: key, 
                target: target, 
            };
            link.intermediate = key;
            newNodeMap.set(key, intermediate);
            newLinkMap.set(link.key, link);
            newLinkMap.set(siLink.key, siLink);
            newLinkMap.set(itLink.key, itLink);
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
                if (entry.value.nodes !== undefined) {
                    entry.value.nodes[0] = dg.graph.nodeMap.get(entry.value.nodes[0]);
                    entry.value.nodes[2] = dg.graph.nodeMap.get(entry.value.nodes[2]);
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
            if (link.nodes !== undefined) {
                if (!linkNeighborhoodMap.has(link.nodes[0].key)) {
                    linkNeighborhoodMap.set(link.nodes[0].key, []);
                }
                linkNeighborhoodMap.get(link.nodes[0].key).push(link.key);
                if (!linkNeighborhoodMap.has(link.nodes[2].key)) {
                    linkNeighborhoodMap.set(link.nodes[2].key, []);
                }
                linkNeighborhoodMap.get(link.nodes[2].key).push(link.key);
            }
        });
        linkNeighborhoodMap.entries().forEach(function(entry) {
            dg.graph.nodeMap.get(entry.key).links = entry.value;
        });

        // PUSH DATA
        dg.graph.nodes.length = 0;
        Array.prototype.push.apply(dg.graph.nodes, dg.graph.nodeMap.values());
        dg.graph.links.length = 0;
        Array.prototype.push.apply(dg.graph.links, dg.graph.linkMap.values());
        dg.graph.centerNodeKey = json.center[0];
    }

    dg.updateGraph = function(key) {
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
        $("#brand .loading").removeClass("hidden");
        if (dg.graph.cache.has(key)) {
            var json = JSON.parse(JSON.stringify(dg.graph.cache.get(key)));
            dg.handleNewGraphData(null, json);
        } else {
            var url = "/api/" + entityType + "/network/" + entityId;
            d3.json(url, dg.handleNewGraphData);
        }
    }

    dg.graph.init = function() {
        dg.color.colorFunc = dg.color.heatmap;

        d3.selection.prototype.moveToFront = function() {
            return this.each(function(){ this.parentNode.appendChild(this); });
        };

        window.addEventListener("popstate", dg.history.onPopState);

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

        dg.graph.svgSelection = d3.select("body").append("svg")
            .attr("width", dg.graph.dimensions[0])
            .attr("height", dg.graph.dimensions[1]);

        dg.graph.svgSelection.on("mousedown", function() {
            dg.graph.nodes.forEach(function(n) { n.fixed = false; });
            dg.selectNode(null);
        });

        var defs = dg.graph.svgSelection.append("defs");
        
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
            //.attr("fill", "#666")
            .attr("stroke-linecap", "round")
            .attr("stroke-linejoin", "round")
            ;

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
            .attr("stroke-width", 1.5)
            ;

        /*
        var blur = defs.append("filter")
            .attr("id", "blur")
            .append("feGaussianBlur")
            .attr("in", "SourceGraphic")
            .attr("stdDeviation", 1)
            ;
        */

        dg.graph.haloLayer = dg.graph.svgSelection.append("g")
            .attr("id", "haloLayer");
        dg.graph.linkLayer = dg.graph.svgSelection.append("g")
            .attr("id", "linkLayer");
        dg.graph.nodeLayer = dg.graph.svgSelection.append("g")
            .attr("id", "nodeLayer");
        dg.graph.textLayer = dg.graph.svgSelection.append("g")
            .attr("id", "textLayer");
        dg.graph.haloSelection = dg.graph.haloLayer.selectAll(".node");
        dg.graph.linkSelection = dg.graph.linkLayer.selectAll(".link");
        dg.graph.nodeSelection = dg.graph.nodeLayer.selectAll(".node");
        dg.graph.textSelection = dg.graph.textLayer.selectAll(".node");

        dg.graph.forceLayout = d3.layout.force()
            .nodes(dg.graph.nodes)
            .links(dg.graph.links)
            .size(dg.graph.dimensions)
            .on("tick", dg.tick)
            .linkStrength(2)
            .friction(0.9)
            .linkDistance(function(d, i) {
                return d.isSpline ? 50 : 100; 
            })
            .charge(-300)
            .chargeDistance(500)
            .gravity(0.15)
            .theta(0.1)
            .alpha(0.1)
            ;

    }

    return dg;

}(dg || {}));