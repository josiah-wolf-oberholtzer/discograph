var color = d3.scale.category20b();
var can_load_new_data = false;
var base_url = "/api/cluster/"

var w = window,
    d = document,
    e = d.documentElement,
    g = d.getElementsByTagName('body')[0],
    x = w.innerWidth || e.clientWidth || g.clientWidth,
    y = w.innerHeight|| e.clientHeight|| g.clientHeight;

var svg = d3.select("body").append("svg")
    .attr("width", x)
    .attr("height", y);

var nodes = [];
var links = [];
var nodeMap = d3.map();
var linkMap = d3.map();

var force = d3.layout.force()
    .nodes(nodes)
    .links(links)
    .linkStrength(0.2)
    .friction(0.9)
    .linkDistance(20)
    .charge(-300)
    .gravity(0.1)
    .theta(0.8)
    .alpha(0.1)
    .size([x, y])
    .on("tick", tick);

var node = svg.selectAll(".node"),
    link = svg.selectAll(".link");

var startForceLayout = function() {

    link = link.data(force.links(), function(d) { 
        var key = d.source.id + "-" + d.target.id;
        if (d.dotted) {
            key = key + '-dotted';
        }
        return key;
    });

    var linkEnter = link.enter().append("line")
        .attr("class", "link")
        .style("stroke-width", 1)
        .style("stroke-dasharray", function(d) {
            if (d.dotted) {
                return "2, 4";
            } else {
                return "";
            }});

    link.exit().remove();

    node = node.data(force.nodes(), function(d) { 
        return d.id;
    });

    var nodeEnter = node
        .enter().append("g")
        .attr("class", "node")
        .style("fill", function(d) { return color(d.distance); })
        .call(force.drag)
        .on("dblclick", function(d) {
            if (can_load_new_data) {
                can_load_new_data = false;
                d3.json(base_url + d.id, loadData);
            } else {
                alert('Not yet!');
            }
        });

    nodeEnter.append("circle")
        .attr("r", function(d) { return 5 + (d.size / 2) });

    nodeEnter.append("title")
        .text(function(d) { return d.name; });

    nodeEnter.append("text")
        .attr("dy", ".35em")
        .attr("dx", function(d) { return 12 + (d.size / 2) })
        .text(function(d) { return d.name; });

    node.exit().remove();

    force.start();
    
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

function updateWindow(){
    x = w.innerWidth || e.clientWidth || g.clientWidth;
    y = w.innerHeight|| e.clientHeight|| g.clientHeight;
    svg.attr("width", x).attr("height", y);
    force.size([x, y]).start();
}
window.onresize = updateWindow;

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
        if (link.dotted) {
            key = key + '-dotted';
        }
        map.set(key, link);
    });
    return map;
}

function updateData(json) {
    var newNodeMap = buildNodeMap(json.nodes);
    var newLinkMap = buildLinkMap(json.links);
    var nodeKeysToRemove = [];
    var linkKeysToRemove = [];
    // Find keys for nodes to be removed.
    nodeMap.keys().forEach(function(key) {
        if (!newNodeMap.has(key)) {
            nodeKeysToRemove.push(key);
        };
    });
    // Find keys for links to be removed;
    linkMap.keys().forEach(function(key) {
        if (!newLinkMap.has(key)) {
            linkKeysToRemove.push(key);
        };
    });
    // Remove each old node matching each to-remove key.
    nodeKeysToRemove.forEach(function(key) {
        nodeMap.remove(key);
    });
    // Remove each old link matching each to-remove key.
    linkKeysToRemove.forEach(function(key) {
        linkMap.remove(key);
    });
    // Add in non-existent new nodes.
    newNodeMap.entries().forEach(function(entry) {
        console.log(entry);
        if (!nodeMap.has(entry.key)) {
            nodeMap.set(entry.key, entry.value);
        }
    });
    // Add in non-existent new links, setting their source/target as needed.
    newLinkMap.entries().forEach(function(entry) {
        console.log(entry);
        if (!linkMap.has(entry.key)) {
            entry.value.source = nodeMap.get(entry.value.source);
            entry.value.target = nodeMap.get(entry.value.target);
            linkMap.set(entry.key, entry.value);
        }
    });
    // Replace array contents with map values.
    nodes.length = 0;
    Array.prototype.push.apply(nodes, nodeMap.values());
    links.length = 0;
    Array.prototype.push.apply(links, linkMap.values());
}

var data = null;

var loadData = function(error, json) {
    if (error) return console.warn(error);
    setTimeout(function() {
        can_load_new_data = true;
    }, 2000);
    data = json;
    updateData(json);
    startForceLayout();
}

d3.json(base_url + 152882, loadData);