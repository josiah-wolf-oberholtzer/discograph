dg.relations = {
    layers: {
        root: null,
        },
    };

function dg_relations_init() {
    dg.relations.layers.root = d3.select('#svg').append('g')
        .attr('id', 'relationsLayer');
}

function dg_relations_chartrelations() {
    var years = dg.relations.nested.map(function(d) { return parseInt(d.key); })
    var extent = d3.extent(years);
    var scale = d3.scale.linear()
        .domain(extent)
        .range([100, dg.dimensions[0] - 100]);
    var axis = d3.svg.axis()
        .orient('bottom')
        .scale(scale)
        .ticks(years.length)
        .tickFormat(d3.format('0000'));
    dg.relations.layers.root.append('g')
        .attr('class', 'x axis')
        .attr('transform', 'translate(0, 100)')
        .call(axis)
        .selectAll('text')
        .attr('y', 0)
        .attr('x', 9)
        .attr('dy', '.35em')
        .attr('transform', 'rotate(45)')
        .style('text-anchor', 'start');
}

function dg_relations_chartRadial() {
    dg.relations.layers.root = d3.select('#svg')
        .append('g')
        .attr('id', 'relationsLayer');
    var barHeight = d3.min(dg.dimensions) / 4;
    var data = dg.relations.byRole;
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
    dg.arc = arc;
    var group = dg.relations.layers.root.append('g')
        .attr('class', 'radial centered')
        .attr('transform', 'translate(' +
            (dg.dimensions[0] / 2) +
            ',' +
            (dg.dimensions[1] / 2) +
            ')'
            );
    var segments = group.selectAll('path')
        .data(data)
        .enter().append('path')
        .attr('class', 'arc')
        .each(function(d) { d.outerRadius = 0; })
        .attr('d', arc)
        .on('mousedown', function(d) {
            $('#filter-roles').multiselect('select', d.key); 
            dg.fsm.requestNetwork(dg.network.data.json.center.key, true);
            d3.event.stopPropagation();
        });
    segments.transition()
        .ease('elastic')
        .duration(500)
        .delay(function(d, i) { return (numBars - i) * 25; })
        .attrTween('d', function(d, index) {
            var i = d3.interpolate(d.outerRadius, barScale(+ d.values));
            return function(t) {
                d.outerRadius = i(t);
                return arc(d, index);
            };
        });
    var textAnchor = function(d, i) {
        var angle = (i + 0.5) / numBars;
        if (angle < 0.5) {
            return 'start';
        } else {
            return 'end';
        }
    };
    var transform = function(d, i) {
        var hypotenuse = barScale(d.values) + 5;
        var angle = (i + 0.5) / numBars;
        var degrees = (angle * 360);
        if (180 <= degrees) {
            degrees -= 180;
        }
        degrees -= 90;
        var radians = angle * 2 * Math.PI;
        var x = Math.sin(radians) * hypotenuse;
        var y = - Math.cos(radians) * hypotenuse;
        return [
            'rotate(' + degrees + ',' + x + ',' + y + ')',
            'translate(' + x +',' + y + ')'
            ].join(' ');
    }
    var outerLabels = group.selectAll('text.outer')
        .data(data)
        .enter().append('text')
        .attr('class', 'outer')
        .attr('text-anchor', textAnchor)
        .attr('transform', transform)
        .text(function(d) { return d.key; });
    var innerLabels = group.selectAll('text.inner')
        .data(data)
        .enter().append('text')
        .attr('class', 'inner')
        .attr('text-anchor', textAnchor)
        .attr('transform', transform)
        .text(function(d) { return d.key; });
}