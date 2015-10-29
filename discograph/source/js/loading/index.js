function loadingAnimation() {
    var start = Date.now();
    var data = [
        {value: 1}, {value: 2}, {value: 3}, {value: 4},
        {value: 5}, {value: 6}, {value: 7}, {value: 8},
        ];
    dg.timeline.layers.root.selectAll('g').remove();
    var group = dg.timeline.layers.root.append('g')
        .attr('class', 'radial')
        .attr('transform', 'translate(' +
            dg.network.dimensions[0] / 2 +
            ',' +
            dg.network.dimensions[1] / 2 +
            ')'
            );
    var arc = d3.svg.arc()
        .startAngle(function(d) { return d.startAngle; })
        .endAngle(function(d) { return d.endAngle; })
        .innerRadius(function(d) { return d.innerRadius; })
        .outerRadius(function(d) { return d.outerRadius; });
    var barHeight = 200;
    var barScale = d3.scale.linear()
        .domain([1, 8])
        .range([barHeight / 4, barHeight]);
    var segments = group.selectAll('path')
        .data(data)
        .enter().append('path')
        .attr('class', 'arc')
        .each(function(d, i) { 
            d.startAngle = 2 * Math.PI * Math.random();
            d.endAngle = 2 * Math.PI * Math.random();
            d.rotationRate = Math.random() * 10;
            d.innerRadius = 0;
            d.outerRadius = 0;
        })
        .attr('d', arc);
    segments.transition()
        .ease("elastic")
        .duration(500)
        .delay(function(d, i) { return (data.length - i) * 50; })
        .attrTween('d', function(d, i) {
            var inner = d3.interpolate(d.innerRadius, barScale(d.value - 1));
            var outer = d3.interpolate(d.outerRadius, barScale(d.value));
            return function(t) {
                d.innerRadius = inner(t);
                d.outerRadius = outer(t);
                return arc(d, i);
            };
        });
    d3.timer(function() {
        if (dg.network.isUpdating) {
            return true;
        }
        segments.attr('transform', function(d) {
            var angle = (Date.now() - start) * d.rotationRate;
            if (0 < d.outerRadius) {
                angle = angle / d.outerRadius;
            }
            return 'rotate(' + angle + ')';
        });
    });
}
