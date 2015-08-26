var w = window,
    d = document,
    e = d.documentElement,
    g = d.getElementsByTagName('body')[0],
    x = w.innerWidth || e.clientWidth || g.clientWidth,
    y = w.innerHeight|| e.clientHeight|| g.clientHeight;

var svg = d3.select("body").append("svg")
    .attr("width", x)
    .attr("height", y);

var color = d3.scale.category20b();

var force = d3.layout.force()
    .linkStrength(0.1)
    .friction(0.9)
    .linkDistance(10)
    .charge(-200)
    .gravity(0.1)
    .theta(0.8)
    .alpha(0.1)
    .size([x, y])
    .on("tick", tick);

var drag = force.drag()
    .on("dragstart", dragstart);

var link = svg.selectAll(".link");

var node = svg.selectAll(".node");

var url = "/api/cluster/152882"

var dispatcher = d3.dispatch('jsonLoad');

d3.select('#loadData').on('click', function() {
    d3.json(url, callback);
});

dispatcher.on('jsonLoad', function(data) {
    console.log(data);
});

var callback = function(error, graph) {
    if (error) throw error;

    dispatcher.jsonLoad(graph);

    force
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    link = link.data(graph.links)
        .enter().append("line")
        .attr("class", "link")
        .style("stroke-width", 1)
        .style("stroke-dasharray", function(d) {
            if (d.dotted) {
                return "2, 4";
            } else {
                return "";
            }});

    node = node.data(graph.nodes)
        .enter().append("g")
        .attr("class", "node")
        .style("fill", function(d) { return color(d.distance); })
        .on('mousedown', function() {
            var sel = d3.select(this);
            sel.moveToFront();
        })
        .on("dblclick", dblclick)
        .call(drag);

    node.append("circle")
        .attr("r", function(d) { return 5 + (d.member_count / 2) });

    node.append("title")
        .text(function(d) { return d.artist_name; });

    node.append("text")
        .attr("dy", ".35em")
        .attr("dx", function(d) { return 12 + (d.member_count / 2) })
        .text(function(d) { return d.artist_name; });

}

function tick() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });
    node.attr("transform", function(d) { 
        return "translate(" + d.x + "," + d.y + ")";
    });
    //node.attr("cx", function(d) { return d.x; })
    //    .attr("cy", function(d) { return d.y; });
}

function dblclick(d) {
    d3.select(this)
        .classed("fixed", d.fixed = false)
        .style("fill", function(d) { return color(d.distance) });
}

function dragstart(d) {
    d3.select(this)
        .classed("fixed", d.fixed = true)
        .style("fill", function(d) { return "#f00" });
}

function updateWindow(){
    x = w.innerWidth || e.clientWidth || g.clientWidth;
    y = w.innerHeight|| e.clientHeight|| g.clientHeight;
    svg.attr("width", x).attr("height", y);
    force.size([x, y]).start();
}
window.onresize = updateWindow;