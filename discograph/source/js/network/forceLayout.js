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