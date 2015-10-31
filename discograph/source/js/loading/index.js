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
        function(d) { return Math.random(); });
    var scale = d3.scale.category10();
    var selectionEnter = dg.loading.selection.enter()
        .append('path')
        .attr('class', 'arc')
        .attr('d', dg.loading.arc)
        .attr('fill', function(d, i) { 
            console.log('FILL', i, scale(i), scale(i + 1));
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
            console.log('SKIPPING', d);
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
                //console.log(d, now, start);
                return 'rotate(' + angle + ')';
            });
        });
    });
}