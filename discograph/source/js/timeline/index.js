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
        if (error) { console.warn(error); return; }
        dg.timeline.json = json;
        dg.timeline.byYear = d3.nest()
            .key(function(d) { return d.year; })
            .key(function(d) { return d.category; })
            .entries(json.results);
        dg.timeline.byRole = d3.nest()
            .key(function(d) { return d.role; })
            .rollup(function(leaves) { return leaves.length; })
            .entries(dg.timeline.json.results);
    })
}

function dg_timeline_chartTimeline() {
    var years = dg.timeline.nested.map(function(d) { return parseInt(d.key); })
    var extent = d3.extent(years);
    console.log(extent);
    var scale = d3.scale.linear()
        .domain(extent)
        .range([100, dg.network.dimensions[0] - 100]);
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
    var barHeight = d3.min(dg.network.dimensions) / 2;
    var data = dg.timeline.byRole;
    var extent = d3.extent(data, function(d) { return d.values; });
    var barScale = d3.scale.sqrt()
        .exponent(0.25)
        .domain(extent)
        .range([barHeight / 4, barHeight]);
    var keys = data.map(function(d, i) { return d.key; });
    var numBars = keys.length;
    var arc = d3.svg.arc()
        .startAngle(function(d,i) { return (i * 2 * Math.PI) / numBars; })
        .endAngle(function(d,i) { return ((i + 1) * 2 * Math.PI) / numBars; })
        .innerRadius(0);
    var group = dg.timeline.layers.root.append('g')
        .attr('class', 'radial')
        .attr('transform', "translate(" +
            dg.network.dimensions[0] / 2 +
            "," +
            dg.network.dimensions[1] / 2 +
            ")"
            );
    var segments = group.selectAll('path')
        .data(data)
        .enter().append("path")
        .attr('class', 'arc')
        .each(function(d) { d.outerRadius = 0; })
        .attr("d", arc);
    segments.transition()
        .ease("elastic")
        .duration(500)
        .delay(function(d, i) { return (numBars - i) * 25; })
        .attrTween("d", function(d, index) {
            var i = d3.interpolate(d.outerRadius, barScale(+ d.values));
            return function(t) {
                d.outerRadius = i(t);
                return arc(d, index);
            };
        });
    var labels = group.selectAll('text')
        .data(data)
        .enter().append('text')
        .text(function(d) { return d.key; });
}