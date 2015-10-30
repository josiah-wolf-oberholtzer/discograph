dg.loading = {};

function dg_loading_init() {
    var layer = d3.select('#svg').append('g')
        .attr('id', 'loadingLayer')
        .attr('class', 'centered')
        .attr('transform', 'translate(' +
            dg.network.dimensions[0] / 2 +
            ',' +
            dg.network.dimensions[1] / 2 +
            ')'
            );
    dg.loading.arc = d3.svg.arc()
        .startAngle(function(d) { return d.startAngle; })
        .endAngle(function(d) { return d.endAngle; })
        .innerRadius(function(d) { return d.innerRadius; })
        .outerRadius(function(d) { return d.outerRadius; });
    dg.loading.barHeight = 200;
    dg.loading.isLoading = false;
    dg.loading.layer = layer; 
    dg.loading.selection = layer.selectAll('path');
}

function dg_loading_toggle(status) {
    if (status) {
        dg.loading.isLoading = true;
        var input = dg_loading_makeArray();
        var data = input[0], extent = input[1];
    } else {
        dg.loading.isLoading = false;
        var data = [], extent = [0, 0];
    }
    dg_loading_update(data, extent);
}

function dg_loading_makeArray() {
    var values = [];
    for (var i = 0; i < 9; i++) {
        values.push(Math.random());
    }
    values.sort();
    var extent = d3.extent(values);
    var data = [];
    for (var i = 0; i < values.length - 1; i++) {
        data.push({
            targetInnerRadius: values[i],
            targetOuterRadius: values[i + 1],
        });
    }
    return [data, extent];
}

function dg_loading_update(data, extent) {
    var barScale = d3.scale.linear()
        .domain(extent)
        .range([
            dg.loading.barHeight / 4, 
            dg.loading.barHeight
        ]);
    dg.loading.selection = dg.loading.selection.data(data);
    var selectionEnter = dg.loading.selection.enter()
        .append('path')
        .attr('class', 'arc')
        .attr('d', dg.loading.arc)
        .each(function(d, i) { 
            d.startAngle = 2 * Math.PI * Math.random();
            d.endAngle = 2 * Math.PI * Math.random();
            d.rotationRate = Math.random() * 10;
            d.innerRadius = 0;
            d.outerRadius = 0;
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
        .delay(function(d, i) { return (selection.length - i) * 100; })
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
        .delay(function(d, i) { return (selection.length - i) * 100; })
        .attrTween('d', function(d, i) {
            var inner = d3.interpolate(d.innerRadius, 0);
            var outer = d3.interpolate(d.outerRadius, 0);
            return function(t) {
                d.innerRadius = inner(t);
                d.outerRadius = outer(t);
                return dg.loading.arc(d, i);
            };
        });
}

function dg_loading_rotate(selection) {
    var start = Date.now();
    d3.timer(function() {
        if (!dg.loading.isLoading) {
            return true;
        }
        selection.attr('transform', function(d) {
            var angle = (Date.now() - start) * d.rotationRate;
            if (0 < d.outerRadius) {
                angle = angle / d.outerRadius;
            }
            return 'rotate(' + angle + ')';
        });
    });
}