dg.relations = {
    layers: {
        root: null,
        },
    };

function dg_relations_init() {
    dg.relations.layers.root = d3.select('#svg').append('g')
        .attr('id', 'relationsLayer');
}

function dg_relations_chartRadial() {
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
    dg.relations.layers.root = d3.select('#svg')
        .append('g')
        .attr('id', 'relationsLayer');
    var barHeight = d3.min(dg.dimensions) / 3;
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
    var radialGroup = dg.relations.layers.root.append('g')
        .attr('class', 'radial centered')
        .attr('transform', 'translate(' +
            (dg.dimensions[0] / 2) +
            ',' +
            (dg.dimensions[1] / 2) +
            ')'
            );
    var selectedRoles = $('#filter select').val();
    var segments = radialGroup.selectAll('g')
        .data(data)
        .enter().append('g')
        .attr('class', 'segment')
        .classed('selected', function(d) {
            return selectedRoles.indexOf(d.key) != -1;
        })
        .on('mouseover', function() { d3.select(this).moveToFront(); });
    var arcs = segments.append('path')
        .attr('class', 'arc')
        .attr('d', arc)
        .each(function(d) { d.outerRadius = 0; })
        .on('mousedown', function(d) {
            var values = $('#filter-roles').val();
            values.push(d.key);
            $('#filter-roles').val(values).trigger('change');
            dg.fsm.requestNetwork(dg.network.data.json.center.key, true);
            d3.event.stopPropagation();
        })
        .transition()
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
    var outerLabels = segments.append('text')
        .attr('class', 'outer')
        .attr('text-anchor', textAnchor)
        .attr('transform', transform)
        .text(function(d) { return d.key; });
    var innerLabels = segments.append('text')
        .attr('class', 'inner')
        .attr('text-anchor', textAnchor)
        .attr('transform', transform)
        .text(function(d) { return d.key; });
}