var x = 0, y = 0;
var nodes = [];
var links = [];
var initialX = 0;
var initialY = 0;

!function(){
    var dg = {};

    dg.graph = {
        APIURL: "/api/artist/network/",
        centerNodeID: null,
        isUpdating: false,
        json: null,
        linkMap: d3.map(),
        nodeMap: d3.map(),
    };

    dg.heatmap = function(d) {
        var hue = ((d.distance / 12) * 360) % 360;
        var variation_a = ((d.id % 5) - 2) / 20;
        var variation_b = ((d.id % 9) - 4) / 80;
        var saturation = 0.67 + variation_a;
        var lightness = 0.5 + variation_b;
        return d3.hsl(hue, saturation, lightness).toString();
    }

    dg.historyOnPopState = function(event) {
        updateGraph(event.state.id);
    }

    dg.historyPushState = function(id) { 
        var title = document.title;
        var url = "/" + id + "/";
        window.history.pushState({id: id}, title, url); 
    }

    dg.init = function() {
        // Monkey-patch D3.
        d3.selection.prototype.moveToFront = function() {
            return this.each(function(){ this.parentNode.appendChild(this); });
        };
        // Setup history listener.
        window.addEventListener("popstate", dg.historyOnPopState);
        // Get window-size and setup resize listener.
        var w = window,
            d = document,
            e = d.documentElement,
            g = d.getElementsByTagName('body')[0];
        x = w.innerWidth || e.clientWidth || g.clientWidth;
        y = w.innerHeight|| e.clientHeight|| g.clientHeight;
        initialX = x / 2;
        initialY = y / 2;
        window.addEventListener("resize", function() {
            x = w.innerWidth || e.clientWidth || g.clientWidth,
            y = w.innerHeight|| e.clientHeight|| g.clientHeight;
            svg.attr("width", x).attr("height", y);
            force.size([x, y]).start();
        });
        // Done initializing.
        console.log('Discograph initialized.')
    }
    this.dg = dg;
    dg.init();
}();

var svg = d3.select("body").append("svg")
    .attr("width", x)
    .attr("height", y);

var force = d3.layout.force()
    .nodes(nodes)
    .links(links)
    .linkStrength(0.5)
    .friction(0.95)
    .linkDistance(function(e, i) {
        // Expand alias bramble bushes.
        if ((e.source.group === null) && (e.target.group === null)) {
            return 40;
        } else if (e.source.group == e.target.group) {
            return 50;
        } else {
            return 20;
        }
    })
    .charge(-400)
    .gravity(0.15)
    .theta(0.1)
    .alpha(0.1)
    .size([x, y])
    .on("tick", tick);

var node = svg.selectAll(".node"),
    link = svg.selectAll(".link");

var startForceLayout = function() {
    force.start();
    link = link.data(force.links(), function(d) {
        var key = d.source.id + "-" + d.target.id;
        if (d.role == 'Alias') {
            key = key + '-dotted';
        }
        return key;
    });
    var linkEnter = link.enter().append("line")
        .attr("class", "link")
        .style("stroke-width", 1)
        .style("stroke-dasharray", function(d) {
            if (d.role == 'Alias') {
                return "2, 4";
            } else {
                return "";
            }});
    link.exit().remove();
    node = node.data(force.nodes(), function(d) { return d.id; });
    var nodeEnter = node
        .enter().append("g")
        .attr("class", "node")
        .attr("id", function(d) { return "node" + d.id; })
        .style("fill", function(d) { return dg.heatmap(d); })
        .call(force.drag);
    nodeEnter.on("mousedown", function(d) {
        if (!dg.graph.isUpdating) { 
            selectNode(d.id);
        }
    });
    nodeEnter.on("dblclick", function(d) {
        if (!dg.graph.isUpdating) { 
            navigateGraph(d.id);
        }
    });
    nodeEnter.append("circle")
        .attr("class", "halo")
        .attr("r", function(d) { return 60 + (Math.sqrt(d.size) * 2) });
    nodeEnter.select(function(d, i) {return 0 < d.size ? this : null; })
        .append("circle")
        .attr("r", function(d) { return 12 + (Math.sqrt(d.size) * 2) });
    nodeEnter.append("circle")
        .attr("r", function(d) { return 9 + (Math.sqrt(d.size) * 2) });
    nodeEnter.append("path")
        .attr("class", "more")
        .attr("d", d3.svg.symbol().type("cross").size(64))
        .style("stroke-width", 0)
        .style("fill-opacity", 1)
        .style("fill", "#fff")
        .style("opacity", function(d) {return 0 < d.missing ? 1 : 0; });
    nodeEnter.append("title")
        .text(function(d) { return d.name; });
    nodeEnter.append("text")
        .attr("class", "outer")
        .attr("dy", ".35em")
        .attr("dx", function(d) {
            var radius = 15 + (Math.sqrt(d.size) * 2);
            if (0 < d.size) {
                radius = radius + 3;
            }
            return radius;
        })
        .text(function(d) { return d.name; });
    nodeEnter.append("text")
        .attr("class", "inner")
        .attr("dy", ".35em")
        .attr("dx", function(d) {
            var radius = 15 + (Math.sqrt(d.size) * 2);
            if (0 < d.size) {
                radius = radius + 3;
            }
            return radius;
        })
        .text(function(d) { return d.name; });
    node.exit().remove();
    node.moveToFront();

    svg.transition()
        .duration(1000)
        .style("opacity", 1);
    node.transition()
        .duration(1000)
        .style("fill", function(d) { return dg.heatmap(d); })
    svg.selectAll(".node .more")
        .transition()
        .duration(1000)
        .style("opacity", function(d) {return 0 < d.missing ? 1 : 0; });

    selectNode(dg.graph.centerNodeID);
}

function selectNode(id) {
    dg.graph.centerNodeID = id;
    node.filter("*:not(#node" + dg.graph.centerNodeID + ")")
        .select(".halo")
        .style("fill-opacity", 0.);
    node.filter("#node" + dg.graph.centerNodeID)
        .select(".halo")
        .style("fill-opacity", 0.05);
}

function tick() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });
    node.attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
    });
}

function buildNodeMap(nodes) {
    var map = d3.map();
    nodes.forEach(function(node) {
        map.set(node.id, node);
    });
    return map;
}

function buildLinkMap(links) {
    var map = d3.map();
    links.forEach(function(link) {
        var key = link.source + "-" + link.target;
        if (link.role == 'Alias') {
            key = key + '-dotted';
        }
        map.set(key, link);
    });
    return map;
}

var fetchData = function(error, json) {
    if (error) return console.warn(error);
    updateForceLayout(json);
    startForceLayout();
    setTimeout(function() {
        dg.graph.isUpdating = false;
    }, 2000);
}

function updateForceLayout(json) {
    var newNodeMap = buildNodeMap(json.nodes);
    var newLinkMap = buildLinkMap(json.links);
    var nodeKeysToRemove = [];
    var linkKeysToRemove = [];
    dg.graph.nodeMap.keys().forEach(function(key) {
        if (!newNodeMap.has(key)) {
            nodeKeysToRemove.push(key);
        };
    });
    dg.graph.linkMap.keys().forEach(function(key) {
        if (!newLinkMap.has(key)) {
            linkKeysToRemove.push(key);
        };
    });
    nodeKeysToRemove.forEach(function(key) { 
        dg.graph.nodeMap.remove(key);
    });
    linkKeysToRemove.forEach(function(key) { 
        dg.graph.linkMap.remove(key);
    });
    newNodeMap.entries().forEach(function(entry) {
        var key = entry.key;
        var value = entry.value;
        if (dg.graph.nodeMap.has(key)) {
            var node = dg.graph.nodeMap.get(key);
            node.distance = value.distance;
            node.missing = value.missing;
        } else {
            value.x = initialX + (Math.random() * 100) - 50;
            value.y = initialY + (Math.random() * 100) - 50;
            dg.graph.nodeMap.set(key, value);
        }
    });
    newLinkMap.entries().forEach(function(entry) {
        if (!dg.graph.linkMap.has(entry.key)) {
            entry.value.source = dg.graph.nodeMap.get(entry.value.source);
            entry.value.target = dg.graph.nodeMap.get(entry.value.target);
            dg.graph.linkMap.set(entry.key, entry.value);
        }
    });
    nodes.length = 0;
    Array.prototype.push.apply(nodes, dg.graph.nodeMap.values());
    links.length = 0;
    Array.prototype.push.apply(links, dg.graph.linkMap.values());
    dg.graph.json = json;
    selectNode(json.center[0]);
}

var updateGraph = function(id) {
    dg.graph.isUpdating = true;
    var foundNode = node.filter(function(d) { return d.id == id; });
    if (foundNode.length == 1) {
        foundNode.each(function(d) {
            initialX = d.x;
            initialY = d.y;
        });
    } else {
        initialX = x / 2;
        initialY = y / 2;
    }
    svg.transition().duration(250).style("opacity", 0.333);
    $(document).attr("body").id = id;
    if (nodes.length) {
        var artistName = nodes.filter(function(d) { 
            return d.id == id; }
        )[0].name
        document.title = "Discograph: " + artistName;
    }
    d3.json(dg.graph.APIURL + id, fetchData);
}

var navigateGraph = function(id) {
    dg.historyPushState(id);
    updateGraph(id);
}

navigateGraph(d3.select("body").attr("id"));