! function() {
    var dg = {
        version: "0.1"
    };

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
        $(window).trigger({
            type: 'discograph:network-fetch',
            entityKey: event.state.key,
            pushHistory: false,
        });
    }

    function dg_history_pushState(entityKey, params) {
        var entityType = entityKey.split("-")[0];
        var entityId = entityKey.split("-")[1];
        var title = document.title;
        var url = "/" + entityType + "/" + entityId;
        if (params) {
            url += "?" + decodeURIComponent($.param(params));
        }
        var state = {
            key: entityKey,
            params: params
        };
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
        var state = {
            key: entityKey,
            params: params
        };
        window.history.replaceState(state, title, url);
        ga('send', 'pageview', url);
        ga('set', 'page', url);
    }
    dg.loading = {};

    function dg_loading_init() {
        var layer = d3.select('#svg').append('g')
            .attr('id', 'loadingLayer')
            .attr('class', 'centered')
            .attr('transform', 'translate(' +
                dg.dimensions[0] / 2 +
                ',' +
                dg.dimensions[1] / 2 +
                ')'
            );
        dg.loading.arc = d3.svg.arc()
            .startAngle(function(d) {
                return d.startAngle;
            })
            .endAngle(function(d) {
                return d.endAngle;
            })
            .innerRadius(function(d) {
                return d.innerRadius;
            })
            .outerRadius(function(d) {
                return d.outerRadius;
            });
        dg.loading.barHeight = 200;
        dg.loading.isLoading = false;
        dg.loading.layer = layer;
        dg.loading.selection = layer.selectAll('path');
    }

    function dg_loading_toggle(status) {
        if (status) {
            dg.loading.isLoading = true;
            var input = dg_loading_makeArray();
            var data = input[0],
                extent = input[1];
            $("#page-loading")
                .removeClass("glyphicon-random")
                .addClass("glyphicon-animate glyphicon-refresh");
        } else {
            dg.loading.isLoading = false;
            var data = [],
                extent = [0, 0];
            $("#page-loading")
                .removeClass("glyphicon-animate glyphicon-refresh")
                .addClass("glyphicon-random");
        }
        dg_loading_update(data, extent);
    }

    function dg_loading_makeArray() {
        var count = 10;
        var values = [];
        var data = [];
        for (var i = 0; i < count; i++) {
            var pair = [Math.random(), Math.random()];
            pair.sort();
            values.push(pair[0]);
            values.push(pair[1]);
            data.push({
                active: true,
                startAngle: 2 * Math.PI * Math.random(),
                endAngle: 2 * Math.PI * Math.random(),
                rotationRate: Math.random() * 10,
                targetInnerRadius: pair[0],
                targetOuterRadius: pair[1],
            });
        }
        return [data, d3.extent(values)];
    }

    function dg_loading_update(data, extent) {
        var barScale = d3.scale.linear()
            .domain(extent)
            .range([
                dg.loading.barHeight / 4,
                dg.loading.barHeight
            ]);
        dg.loading.selection = dg.loading.selection.data(
            data,
            function(d) {
                return Math.random();
            });
        var scale = d3.scale.category10();
        var selectionEnter = dg.loading.selection.enter()
            .append('path')
            .attr('class', 'arc')
            .attr('d', dg.loading.arc)
            .attr('fill', function(d, i) {
                return scale(i);
            })
            .each(function(d, i) {
                d.innerRadius = 0;
                d.outerRadius = 0;
                d.hasTimer = false;
            });
        var selectionExit = dg.loading.selection.exit();
        dg_loading_transition_update(selectionEnter, barScale);
        dg_loading_transition_exit(selectionExit);
        if (dg.loading.selection.length) {
            dg_loading_rotate(dg.loading.selection);
        }
    }

    function dg_loading_transition_update(selection, barScale) {
        selection.transition()
            .duration(1000)
            .delay(function(d, i) {
                return (selection.length - i) * 100;
            })
            .attrTween('d', function(d, i) {
                var inner = d3.interpolate(d.innerRadius, barScale(d.targetInnerRadius));
                var outer = d3.interpolate(d.outerRadius, barScale(d.targetOuterRadius));
                return function(t) {
                    d.innerRadius = inner(t);
                    d.outerRadius = outer(t);
                    return dg.loading.arc(d, i);
                };
            });
    }

    function dg_loading_transition_exit(selection) {
        selection.transition()
            .duration(1000)
            .delay(function(d, i) {
                return (selection.length - i) * 100;
            })
            .attrTween('d', function(d, i) {
                var inner = d3.interpolate(d.innerRadius, 0);
                var outer = d3.interpolate(d.outerRadius, 0);
                return function(t) {
                    d.innerRadius = inner(t);
                    d.outerRadius = outer(t);
                    return dg.loading.arc(d, i);
                };
            })
            .each('end', function(d) {
                d.active = false;
                this.remove();
            });
    }

    function dg_loading_rotate(selection) {
        var start = Date.now();
        selection.each(function(d) {
            if (d.hasTimer) {
                return;
            }
            d.hasTimer = true;
            d3.timer(function() {
                if (!d.active) {
                    return true;
                }
                selection.attr('transform', function(d) {
                    var now = Date.now();
                    var angle = (now - start) * d.rotationRate;
                    if (0 < d.outerRadius) {
                        angle = angle / d.outerRadius;
                    }
                    return 'rotate(' + angle + ')';
                });
            });
        });
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
        dg_network_toggle(true);
        dg_loading_toggle(false);
    }

    function dg_network_setupForceLayout() {
        return d3.layout.force()
            .nodes(dg.network.pageData.nodes)
            .links(dg.network.pageData.links)
            .size(dg.dimensions)
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
            .gravity(0.2)
            .theta(1)
            .alpha(0.1);
    }

    function dg_network_startForceLayout() {
        var keyFunc = function(d) {
            return d.key
        }
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
        var hullData = d3.nest().key(function(d) {
                return d.cluster;
            })
            .entries(hullNodes)
            .filter(function(d) {
                return 1 < d.values.length;
            });
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
        dg.network.pageData.nodes.forEach(function(n) {
            n.fixed = false;
        });
        dg.network.forceLayout.start();
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
            .attr("r", function(d) {
                return dg_network_getOuterRadius(d) + 40;
            });
    }

    function dg_network_onHaloExit(haloExit) {
        haloExit.remove();
    }

    function dg_network_onHullEnter(hullEnter) {
        var hullEnter = hullEnter.append("g")
            .attr("class", function(d) {
                return "hull hull-" + d.key
            });
        hullEnter.append("path");
    }

    function dg_network_onHullExit(hullExit) {
        hullExit.remove();
    }

    function dg_network_init() {
        var root = d3.select("#svg").append("g")
            .attr("id", "networkLayer");
        dg.network.layers.root = root;
        d3.select("#svg").on("mousedown", function() {
            dg.network.pageData.nodes.forEach(function(n) {
                n.fixed = false;
            });
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
    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .direction('e')
        .offset([0, 20])
        .html(dg_network_tooltip);

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
        linkEnter.append("path")
            .attr("class", "inner");
        linkEnter.append("text")
            .attr('class', 'outer')
            .text(dg_network_linkAnnotation);
        linkEnter.append("text")
            .attr('class', 'inner')
            .text(dg_network_linkAnnotation);
    }

    function dg_network_onLinkEnterEventBindings(linkEnter) {
        var debounce = $.debounce(250, function(self, d, status) {
            if (status) {
                tip.show(d, d3.select(self).select('text').node());
            } else {
                tip.hide(d);
            }
        });
        linkEnter.on("mouseover", function(d) {
            d3.select(this).select(".inner")
                .transition()
                .style("stroke-width", 3);
            debounce(this, d, true);
        });
        linkEnter.on("mouseout", function(d) {
            d3.select(this).select(".inner")
                .transition()
                .duration(500)
                .style("stroke-width", 1);
            debounce(this, d, false);
        });
    }

    function dg_network_tooltip(d) {
        var parts = [
            '<p>' + d.source.name + '</p>',
            '<p><strong>&laquo; ' + d.role + ' &raquo;</strong></p>',
            '<p>' + d.target.name + '</p>',
        ];
        return parts.join('');
    }

    function dg_network_linkAnnotation(d) {
        return d.role.split(' ').map(function(x) {
            return x[0];
        }).join('');
    }

    function dg_network_onLinkExit(linkExit) {
        linkExit.remove();
    }

    function dg_network_onLinkUpdate(linkSelection) {}

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
            .select(function(d, i) {
                return 0 < d.size ? this : null;
            })
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
            .attr("height", function(d) {
                return 2 * dg_network_getInnerRadius(d);
            })
            .attr("width", function(d) {
                return 2 * dg_network_getInnerRadius(d);
            })
            .attr("x", function(d) {
                return -1 * dg_network_getInnerRadius(d);
            })
            .attr("y", function(d) {
                return -1 * dg_network_getInnerRadius(d);
            });
        nodeEnter.append("path")
            .attr("class", "more")
            .attr("d", d3.svg.symbol().type("cross").size(64))
            .style("opacity", function(d) {
                return 0 < d.missing ? 1 : 0;
            });
        nodeEnter.append("title")
            .text(function(d) {
                return d.name;
            });
    }

    function dg_network_onNodeEnterEventBindings(nodeEnter) {
        nodeEnter.on("dblclick", function(d) {
            $(window).trigger({
                type: 'discograph:network-fetch',
                entityKey: d.key,
                pushHistory: true,
            });
        });
        nodeEnter.on("mousedown", function(d) {
            if (!dg.network.isUpdating) {
                dg.network.pageData.nodes.forEach(function(n) {
                    n.fixed = false;
                });
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
                    dg.network.pageData.nodes.forEach(function(n) {
                        n.fixed = false;
                    });
                    d.fixed = true;
                    dg_network_selectNode(d.key);
                }
            } else if ((thisTime - lastTime) < 500) {
                $(window).trigger({
                    type: 'discograph:network-fetch',
                    entityKey: d.key,
                    pushHistory: true,
                });
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
        var page = dg_network_getNextPage();
        dg_network_selectPage(page);
        dg_network_startForceLayout();
        dg_network_reselectNode();
    }

    function dg_network_prevPage() {
        var page = dg_network_getPrevPage();
        dg_network_selectPage(page);
        dg_network_startForceLayout();
        dg_network_reselectNode();
    }

    function dg_network_getNextPage() {
        var page = dg.network.pageData.currentPage + 1;
        if (dg.network.data.pageCount < page) {
            page = 1;
        }
        return page;
    }

    function dg_network_getPrevPage() {
        var page = dg.network.pageData.currentPage - 1;
        if (page == 0) {
            page = dg.network.data.pageCount;
        }
        return page;
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
            .attr("dx", function(d) {
                return dg_network_getOuterRadius(d) + 3;
            })
            .attr("dy", ".35em")
            .text(dg_network_getNodeText);
        textEnter.append("text")
            .attr("class", "inner")
            .attr("dx", function(d) {
                return dg_network_getOuterRadius(d) + 3;
            })
            .attr("dy", ".35em")
            .text(dg_network_getNodeText);
    }

    function dg_network_onTextExit(textExit) {
        textExit.remove();
    }

    function dg_network_onTextUpdate(textUpdate) {
        textUpdate.select('.outer').text(dg_network_getNodeText);
        textUpdate.select('.inner').text(dg_network_getNodeText);
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

    function dg_network_splineInner(sX, sY, sR, cX, cY) {
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
            sXY = dg_network_splineInner(sX, sY, sR, cX, cY);
            tXY = dg_network_splineInner(tX, tY, tR, cX, cY);
            return (
                "M " + sXY[0] + "," + sXY[1] + " " +
                "S " + cX + "," + cY + " " +
                " " + tXY[0] + "," + tXY[1] + " "
            );
        } else {
            return "M " + [sX, sY] + " L " + [tX, tY];
        }
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

    var unlabeled_roles = [
        'Alias',
        'Member Of',
        'Sublabel Of',
    ];

    function dg_network_tick_link(d, i) {
        var group = d3.select(this);
        var path = group.select('path');
        path.attr('d', dg_network_spline(d));
        var x1 = d.source.x,
            y1 = d.source.y,
            x2 = d.target.x,
            y2 = d.target.y;
        var node = path.node();
        var point = node.getPointAtLength(node.getTotalLength() / 2);
        var x = point.x,
            y = point.y;
        d.x = x;
        d.y = y;
        var angle = Math.atan2((y2 - y1), (x2 - x1)) * (180 / Math.PI);
        var text = group.selectAll('text')
            .attr('x', point.x)
            .attr('y', point.y)
            .attr('transform', 'rotate(' + angle + ' ' + x + ' ' + y + ')');
    }

    function dg_network_translate(d) {
        return "translate(" + d.x + "," + d.y + ")";
    }

    function dg_network_tick(e) {
        var k = e.alpha * 5;
        if (dg.network.data.json) {
            var centerNode = dg.network.data.nodeMap.get(dg.network.data.json.center.key);
            if (!centerNode.fixed) {
                var dims = dg.dimensions;
                var dx = ((dims[0] / 2) - centerNode.x) * k;
                var dy = ((dims[1] / 2) - centerNode.y) * k;
                centerNode.x += dx;
                centerNode.y += dy;
            }
        }
        dg.network.selections.link.each(dg_network_tick_link);
        dg.network.selections.halo.attr("transform", dg_network_translate);
        dg.network.selections.node.attr("transform", dg_network_translate);
        dg.network.selections.text.attr("transform", dg_network_translate);
        dg.network.selections.hull.select("path").attr("d", function(d) {
            var vertices = d3.geom.hull(dg_network_getHullVertices(d.values));
            return "M" + vertices.join("L") + "Z";
        });
    }

    function dg_network_toggle(status) {
        if (status) {
            dg.network.layers.root.transition()
                .delay(250)
                .duration(1000)
                .style("opacity", 1)
                .each('end', function(d, i) {
                    dg.network.isUpdating = false;
                    dg.network.layers.link.selectAll('.link')
                        .classed('noninteractive', false);
                    dg.network.layers.node.selectAll('.node')
                        .classed('noninteractive', false);
                });
        } else {
            dg.network.forceLayout.stop()
            dg.network.isUpdating = true;
            dg.network.layers.root.transition()
                .duration(250)
                .style("opacity", 0.333);
            dg.network.layers.link.selectAll('.link')
                .classed('noninteractive', true);
            dg.network.layers.node.selectAll('.node')
                .classed('noninteractive', true);
        }
    }

    function dg_svg_init() {
        d3.selection.prototype.moveToFront = function() {
            return this.each(function() {
                this.parentNode.appendChild(this);
            });
        };
        var w = window,
            d = document,
            e = d.documentElement,
            g = d.getElementsByTagName('body')[0];
        dg.dimensions = [
            w.innerWidth || e.clientWidth || g.clientWidth,
            w.innerHeight || e.clientHeight || g.clientHeight,
        ];
        dg.network.newNodeCoords = [
            dg.dimensions[0] / 2,
            dg.dimensions[1] / 2,
        ];
        d3.select("#svg")
            .attr("width", dg.dimensions[0])
            .attr("height", dg.dimensions[1]);
        dg_svg_setupDefs();
        d3.select('#svg').call(tip);
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
    dg.timeline = {
        layers: {
            root: null,
        },
    };

    function dg_timeline_init() {
        dg.timeline.layers.root = d3.select("#svg").append("g")
            .attr("id", "timelineLayer");
    }

    function dg_timeline_fetch(id) {
        var url = '/api/artist/timeline/' + id;
        d3.json(url, function(error, json) {
            if (error) {
                console.warn(error);
                return;
            }
            dg.timeline.json = json;
            dg.timeline.byYear = d3.nest()
                .key(function(d) {
                    return d.year;
                })
                .key(function(d) {
                    return d.category;
                })
                .entries(json.results);
            dg.timeline.byRole = d3.nest()
                .key(function(d) {
                    return d.role;
                })
                .rollup(function(leaves) {
                    return leaves.length;
                })
                .entries(dg.timeline.json.results);
        })
    }

    function dg_timeline_chartTimeline() {
        var years = dg.timeline.nested.map(function(d) {
            return parseInt(d.key);
        })
        var extent = d3.extent(years);
        var scale = d3.scale.linear()
            .domain(extent)
            .range([100, dg.dimensions[0] - 100]);
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
    }

    function dg_timeline_chartRadial() {
        var barHeight = d3.min(dg.dimensions) / 2;
        var data = dg.timeline.byRole;
        var extent = d3.extent(data, function(d) {
            return d.values;
        });
        var barScale = d3.scale.sqrt()
            .exponent(0.25)
            .domain(extent)
            .range([barHeight / 4, barHeight]);
        var keys = data.map(function(d, i) {
            return d.key;
        });
        var numBars = keys.length;
        var arc = d3.svg.arc()
            .startAngle(function(d, i) {
                return (i * 2 * Math.PI) / numBars;
            })
            .endAngle(function(d, i) {
                return ((i + 1) * 2 * Math.PI) / numBars;
            })
            .innerRadius(0);
        var group = dg.timeline.layers.root.append('g')
            .attr('class', 'radial')
            .attr('transform', "translate(" +
                dg.dimensions[0] / 2 +
                "," +
                dg.dimensions[1] / 2 +
                ")"
            );
        var segments = group.selectAll('path')
            .data(data)
            .enter().append("path")
            .attr('class', 'arc')
            .each(function(d) {
                d.outerRadius = 0;
            })
            .attr("d", arc);
        segments.transition()
            .ease("elastic")
            .duration(500)
            .delay(function(d, i) {
                return (numBars - i) * 25;
            })
            .attrTween("d", function(d, index) {
                var i = d3.interpolate(d.outerRadius, barScale(+d.values));
                return function(t) {
                    d.outerRadius = i(t);
                    return arc(d, index);
                };
            });
        var labels = group.selectAll('text')
            .data(data)
            .enter().append('text')
            .text(function(d) {
                return d.key;
            });
    }

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
        inputElement.typeahead({
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
            .keydown(function(event) {
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
                type: 'discograph:network-fetch',
                entityKey: datum,
                pushHistory: true,
            });
        };
    }

    function dg_events_loading_toggle(event) {
        dg_loading_toggle(event.status);
    }

    function dg_events_network_toggle(event) {
        dg_network_toggle(event.status);
    }

    function dg_events_network_fetch(event) {
        dg_network_toggle(false);
        dg_loading_toggle(true);
        var entityKey = event.entityKey;
        var entityType = entityKey.split("-")[0];
        var entityId = entityKey.split("-")[1];
        var pushHistory = event.pushHistory;
        var url = "/api/" + entityType + "/network/" + entityId;
        var params = {
            'roles': $('#filter select').val()
        };
        if (params.roles) {
            url += '?' + decodeURIComponent($.param(params));
        }
        d3.json(url, function(error, json) {
            if (error) {
                $(window).trigger({
                    type: 'discograph:error',
                    error: error,
                });
            } else {
                dg_network_handleAsyncData(json, pushHistory, params);
            }
        });
    }

    function dg_events_random_fetch(event) {
        dg_network_toggle(false);
        dg_loading_toggle(true);
        var url = '/api/random?' + Math.floor(Math.random() * 1000000);
        d3.json(url, function(error, json) {
            if (error) {
                $(window).trigger({
                    type: 'discograph:error',
                    error: error,
                });
            } else {
                $(window).trigger({
                    type: 'discograph:network-fetch',
                    entityKey: json.center,
                    pushHistory: true,
                });
            }
        });
    }

    function dg_events_error(event) {
        var error = event.error;
        var message = 'Something went wrong!';
        var status = error.status;
        if (status == 0) {
            status = 404;
        } else if (status == 429) {
            message = 'Hey, slow down, buddy. Give it a minute.'
        }
        var text = '<div class="alert alert-danger alert-dismissible" role="alert">';
        text += '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
        text += '<strong>' + status + '!</strong> ' + message;
        text += '</div>';
        $('#flash').append(text);
        dg_network_toggle(true);
        dg_loading_toggle(false);
    }

    function dg_events_network_select_node(event) {
        dg_network_selectNode(event.key);
    }

    function dg_events_network_select_page(event) {
        $(event.target).tooltip('hide');
        dg_network_selectPage(event.page);
        dg_network_startForceLayout();
        dg_network_reselectNode();
    }

    function dg_events_window_resize(event) {
        var w = window,
            d = document,
            e = d.documentElement,
            g = d.getElementsByTagName('body')[0];
        dg.dimensions = [
            w.innerWidth || e.clientWidth || g.clientWidth,
            w.innerHeight || e.clientHeight || g.clientHeight,
        ];
        d3.select("#svg")
            .attr("width", dg.dimensions[0])
            .attr("height", dg.dimensions[1]);
        d3.selectAll('.centered')
            .attr('transform', "translate(" +
                dg.dimensions[0] / 2 + "," +
                dg.dimensions[1] / 2 + ")");
        dg.network.forceLayout.size(dg.dimensions).start();
    }

    function dg_events_init() {
        $(window).on('discograph:error', dg_events_error);
        $(window).on('discograph:loading-toggle', dg_events_loading_toggle);
        $(window).on('discograph:network-fetch', $.debounce(500, function(event) {
            dg_events_network_fetch(event);
        }));
        $(window).on('discograph:network-select-node', dg_events_network_select_node);
        $(window).on('discograph:network-select-page', dg_events_network_select_page);
        $(window).on('discograph:network-toggle', dg_events_network_toggle);
        $(window).on('discograph:random-fetch', $.debounce(500, function(event) {
            dg_events_random_fetch(event);
        }));
        $(window).on('popstate', function(event) {
            dg_history_onPopState(event.originalEvent);
        });
        $(window).on('resize', $.debounce(100, function(event) {
            dg_events_window_resize(event);
        }));
    }
    $(document).ready(function() {
        dg_svg_init();
        dg_network_init();
        dg_timeline_init();
        dg_loading_init();
        dg_typeahead_init();
        dg_events_init();
        if (dgData) {
            var params = {
                'roles': $('#filter select').val()
            };
            dg.network.data.json = dgData;
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
    if (typeof define === "function" && define.amd) define(dg);
    else if (typeof module === "object" && module.exports) module.exports = dg;
    this.dg = dg;
}();
